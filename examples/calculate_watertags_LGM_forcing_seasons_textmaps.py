####################################################################################################################
#
# Calculate and plot rainfall and d18Op results from water tagged iCESM simulation(s)
#
# *** This script produces TEXT MAPS (tag region values printed at their lat/lon location) for: ***
#
# Forcings (each differenced against 0ka):
#   1. Full forcing  (21ka - 0ka)
#   2. GHG           (21kaGHG - 0ka)
#   3. Glacial       (21kaGlac - 0ka)
#   4. Sea level     (21kaSL - 0ka)
#
# Seasons:
#   ANN, DJF, MAM, JJA, SON
#
# This is the text-map counterpart to calculate_watertags_LGM_forcing_seasons.py (which makes global
# contour maps via plot_tagged_precip_and_d18Op). Here we use watertagging_values_on_map instead, so no
# wind/IVT vector overlay machinery is needed.
#
###################################################################################################################

import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cmaps
from matplotlib import colors
from ESMplot.watertagging.print_watertag_values import print_watertag_values, monthly_watertag_values_to_excel
from ESMplot.watertagging.watertag_plots_cenlon_LGMregions import watertagging_values_on_map
from ESMplot.watertagging.seas_avg_LL_watertags import seasavg_watertagging_vars
from ESMplot.climate_analysis import seas_avg_LL as seasavg
from ESMplot.climate_analysis.coordinate_functions import lat_lon_index_array

#########################################################
#
# Specifications for plots are made here
#
#########################################################

#------------------------------------------------
# Which outputs to include
#------------------------------------------------

# Text maps with values for precip and d18Op at each tag region (this script's main output)
TEXT_MAPS = True

# Print values for each tag region to screen
PRINT_VAL = False

# Excel sheet with monthly values for each tagged region by month (written once, not per season/forcing)
MAKE_EXCEL = False

# Difference plots are always made here (each forcing vs. 0ka control)
DIFF = True

#------------------------------------------------
# Specify data path variables
#------------------------------------------------

dir   = '/paleonas/ajthompson/postproc/'
model = 'cam'

# 0ka control (index 0 — always the reference case)
# Forcing experiments (indices 1-4): Full, GHG, Glac, SL
CASES = [
    dir + 'f.e12.F_1850_CAM5.wiso.f19.0ka.002.watertags.2.'                                          + model + '.h0.0006-0025.climo.nc',
    dir + 'f.e12.F_1850_CAM5.wiso.f19.21ka.fullforcing.modern.d18Osw.001.watertags.'                 + model + '.h0.0006-0025.climo.nc',
    dir + 'f.e12.F_1850_CAM5.wiso.f19.21kaGHG.001.watertags.2.'                                      + model + '.h0.0006-0025.climo.nc',
    dir + 'f.e12.F_1850_CAM5.wiso.f19.21kaGlac.001.watertags.2.'                                     + model + '.h0.0006-0025.climo.nc',
    dir + 'f.e12.F_1850_CAM5.wiso.f19.21kaSL.002.watertags.'                                         + model + '.h0.0006-0025.climo.nc',
]
cases = [
    '0ka',
    '$21ka$',
    '$21ka_{GHG}$',
    '$21ka_{GLAC}$',
    '$21ka_{SL}$',
]

# Plain-text forcing labels (index-aligned with cases[1:], i.e. skipping the 0ka control)
# used to build readable text-map titles like "ANN 21ka(GHG)-0ka precip (mm/day)"
forcing_labels = ['Full', 'GHG', 'GLAC', 'SL']

# Anything extra to add to output file names? (season name is appended automatically below)
extra_name = ''

#----------------------------------------------------------------------------------
# Water tagging region definitions
#----------------------------------------------------------------------------------

# Long-form name of each tag (in order)
tagnames = ['Antarctica','North America/Greenland','South America (-Amazon)','Eurasia','Africa (-Congo)','Sundaland NW',
            'SundalandNE','Sundaland SW','Sundaland SE','Sahulland','Australia/Oceania','Amazon','Congo','North Pacific',
            'North Atlantic','North Barents/Arctic Sea','Tropical Pacific NE','Caribbean','Tropical Atlantic NW',
            'Tropical Atlantic NE','Mediterranean','Indian Ocean NW/Arabian Sea','Indian Ocean NE/Bay of Bengal',
            'Sundaland NW ocean','Sundaland NE ocean/South China Sea','Sundaland SW ocean','Sundaland SE ocean',
            'Tropical Pacific NW','Tropical Pacific North Central','Tropical Pacific SE','Tropical Atlantic SW',
            'Tropical Atlantic SE','Tropical Indian SW','Tropical Indian South Central','Tropical Indian SE',
            'Sahul region ocean','Tropical Pacific South Central','South Pacific','South Atlantic','South Indian']

# Code name of each tag (in order)
tagcodes = ['ANTA','NAMG','SAME','ERAS','AFRI','SLNW','SLNE','SLSW','SLSE','SAHL','AUST','AMAZ','CONG','NPAC','NATL',
            'ARCT','TPNE','CARB','TANW','TANE','MEDI','ARAB','BOFB','SONW','SONE','SOSW','SOSE','TPNW','TPNC','TPSE',
            'TASW','TASE','TISW','TISC','TISE','SAHO','TPSC','SPAC','SATL','SIND']

num_landtags  = 13
num_oceantags = 27

# Lat/lon text label positions for tag region text maps
landlat  = [-81,  38, -20, 58, 22, 11,  11, -2,  -2,  -7, -26,   0,  5]
landlon  = [ 180,-100, -58, 55,  10, 95, 116, 95, 116, 135, 135, -61, 22]
oceanlat = [  36, 36,58,   8, 37, 18, 18,44,10,25, 11, 11, -2, -2, 18,   8,  -8,-13,-13,-5,-10,-17,-20,  -8, -40,-40,-40]
oceanlon = [-150,-50,50,-120,-88,-45,-20,22,63,85, 95,116, 95,116,138,-165,-120,-25,  10,57, 83,107,134,-165,-135,-15, 90]

#------------------------------------------------------------------------------------------
# Define region for which water tagging results will be calculated (for regional averages)
#------------------------------------------------------------------------------------------

reg_name = 'SEAMonsoon'

# EastAfrica
southlat = 10
northlat =  20
westlon  = 90
eastlon  = 130

#------------------------------------------------------------
# Map extent
#------------------------------------------------------------

World = True

if World:
    LatMin = -90;  LatMax = 90
    LonMin = -180; LonMax = 180
else:
    LatMin = -40.;  LatMax = 40.
    LonMin = -180.; LonMax = 180.

# Pacific-centered projection
central_lon_180 = True

#-------------------------------------------------
# Plotting specifications
#-------------------------------------------------

proj       = ccrs.PlateCarree(central_longitude=180.) if central_lon_180 else ccrs.PlateCarree()
folderpath = 'pdfs'
filesuf    = '.pdf'

kwargs_mapvals = dict(tag_fs=3.0, bckgrnd_col='w', bckgrnd_pad=0.08, tag_zorder=1)

#----------------------------------------------------------------------------------
# Monthly weights (same for all LGM-era cases)
#----------------------------------------------------------------------------------

wgt_vals = np.array([0.084931507, 0.076712329, 0.084931507, 0.082191781,
                     0.084931507, 0.082191781, 0.084931507, 0.084931507,
                     0.082191781, 0.084931507, 0.082191781, 0.084931507])

#----------------------------------------------------------------------------------
# Season definitions: name -> month indices
#----------------------------------------------------------------------------------

SEASONS = {
    'ANN': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'DJF': [11, 0, 1],
    'MAM': [2, 3, 4],
    'JJA': [5, 6, 7],
    'SON': [8, 9, 10],
}

#----------------------------------------------------------------------------------
# Index range in files
#----------------------------------------------------------------------------------

begi = 'beg'
endi = 'end'

###############################################################################
#
# Open dataset once for coordinate dimensions
#
###############################################################################

ds  = xr.open_dataset(CASES[0])
lat = ds.lat
lon = ds.lon
lat_wgts = np.cos(np.deg2rad(lat))
latarray, lonarray = lat_lon_index_array(lat=lat, lon=lon,
                                         slat=southlat, nlat=northlat,
                                         wlon=westlon,  elon=eastlon)

###############################################################################
#
# Outer loop: seasons
# Inner loop: forcing experiments (all differenced against 0ka)
#
###############################################################################

for season_name, MON in SEASONS.items():

    print(f'\n==============================')
    print(f'Season: {season_name}')
    print(f'==============================')

    #-----------------------------------------------------------------
    # Build per-case monthly weights for this season
    #-----------------------------------------------------------------

    wgt_by_case = []
    for i in range(len(CASES)):
        if len(MON) == 12:
            wgt_mon_i = xr.DataArray(wgt_vals, dims=['time'])
        else:
            sub = wgt_vals[MON]
            wgt_mon_i = xr.DataArray(sub / sub.sum(), dims=['time'])
        wgt_by_case.append(wgt_mon_i)

    #-----------------------------------------------------------------
    # Pre-allocate arrays [case, (tag,) lat, lon]
    #-----------------------------------------------------------------

    prect_global = xr.DataArray(None, dims=['case','lat','lon'],
                                coords=dict(case=cases, lat=lat, lon=lon)).astype(float)
    d18Op_global = xr.DataArray(None, dims=['case','lat','lon'],
                                coords=dict(case=cases, lat=lat, lon=lon)).astype(float)

    Pi_by_tag        = xr.DataArray(None, dims=['case','tag','lat','lon'],
                                    coords=dict(case=cases, tag=tagcodes, lat=lat, lon=lon)).astype(float)
    d18Opsink_by_tag = xr.DataArray(None, dims=['case','tag','lat','lon'],
                                    coords=dict(case=cases, tag=tagcodes, lat=lat, lon=lon)).astype(float)
    d18Opwt_by_tag   = xr.DataArray(None, dims=['case','tag','lat','lon'],
                                    coords=dict(case=cases, tag=tagcodes, lat=lat, lon=lon)).astype(float)

    prect     = xr.DataArray(None, dims=['case','tag'], coords=dict(case=cases, tag=tagcodes))
    d18Op     = xr.DataArray(None, dims=['case','tag'], coords=dict(case=cases, tag=tagcodes))
    prect_reg = xr.DataArray(None, dims=['case'], coords=dict(case=cases))
    d18Op_reg = xr.DataArray(None, dims=['case'], coords=dict(case=cases))
    prect_sum = xr.DataArray(None, dims=['case'], coords=dict(case=cases))
    d18Op_sum = xr.DataArray(None, dims=['case'], coords=dict(case=cases))

    #-----------------------------------------------------------------
    # Load and process each case
    #-----------------------------------------------------------------

    for i in range(len(CASES)):

        print(f'  Working on {cases[i]}')

        wgt_mon_i = wgt_by_case[i]

        # Global prect and d18Op
        prect_global[i,:,:] = seasavg.seasavg_prect_LL(
            path=CASES[i], begi=begi, endi=endi, months=MON, wgt_mon=wgt_mon_i)
        d18Op_global[i,:,:] = seasavg.seasavg_rainiso_LL(
            iso_type='d18O', path=CASES[i], begi=begi, endi=endi,
            ptiny=1.E-18, months=MON, wgt_mon=wgt_mon_i)

        # Water tagging variables for each tag
        for tag in range(len(tagnames)):
            Pi_by_tag[i,tag,:,:], d18Opsink_by_tag[i,tag,:,:] = seasavg_watertagging_vars(
                tagcode=tagcodes[tag], months=MON, path=CASES[i],
                begi=begi, endi=endi, wgt_mon=wgt_mon_i)

        # Derived quantities + regional (area-weighted) averages per tag
        for tag in range(len(tagnames)):
            d18Opwt_by_tag[i,tag,:,:] = (d18Opsink_by_tag[i,tag,:,:]
                                         * (Pi_by_tag[i,tag,:,:] / prect_global[i,:,:]))
            prect_wgt    = Pi_by_tag[i,tag,latarray,lonarray].weighted(lat_wgts[latarray])
            prect[i,tag] = prect_wgt.mean(('lon','lat'))
            d18Op_wgt    = d18Opwt_by_tag[i,tag,latarray,lonarray].weighted(lat_wgts[latarray])
            d18Op[i,tag] = d18Op_wgt.mean(('lon','lat'))

        prect_global_wgt = prect_global[i,latarray,lonarray].weighted(lat_wgts[latarray])
        prect_reg[i]     = prect_global_wgt.mean(('lon','lat'))
        d18Op_global_wgt = d18Op_global[i,latarray,lonarray].weighted(lat_wgts[latarray])
        d18Op_reg[i]     = d18Op_global_wgt.mean(('lon','lat'))

        prect_sum[i] = np.sum(prect[i,:])
        d18Op_sum[i] = np.sum(d18Op[i,:])

    #-----------------------------------------------------------------
    # Text maps + optional screen printout: loop over forcing experiments
    # (1-4), diff against 0ka
    #-----------------------------------------------------------------

    if TEXT_MAPS or PRINT_VAL:

        print(f'  Making text maps for {season_name}...')

        for i in range(1, len(CASES)):

            # Plain-text label for this forcing, e.g. "21ka(GHG)-0ka" -- used as the 'case'
            # string so it shows up clearly in the plot title (season is prepended automatically
            # by watertagging_values_on_map) instead of relying on the tiny LaTeX subscript in `cases`.
            case_label = f'21ka({forcing_labels[i-1]})-{cases[0]}'

            print(f'    {case_label}  [{season_name}]')

            if PRINT_VAL:
                print_watertag_values(precip=prect[i,:]-prect[0,:], d18Op=d18Op[i,:]-d18Op[0,:],
                                      precip_sum=prect_sum[i]-prect_sum[0], d18Op_sum=d18Op_sum[i]-d18Op_sum[0],
                                      precip_reg_gbl=prect_reg[i]-prect_reg[0], d18Op_reg_gbl=d18Op_reg[i]-d18Op_reg[0],
                                      lat=lat, lon=lon, case=case_label, tagnames=tagnames,
                                      season=season_name, slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon)

            if TEXT_MAPS:
                watertagging_values_on_map(precip=prect[i,:], d18Op=d18Op[i,:],
                                           cntlp=prect[0,:], cntlo=d18Op[0,:], diff=True,
                                           case=case_label, tagnames=tagnames,
                                           num_landtags=num_landtags, num_oceantags=num_oceantags, path=CASES[i],
                                           season=season_name, lat=lat, lon=lon, landlat=landlat, landlon=landlon,
                                           oceanlat=oceanlat, oceanlon=oceanlon, slat=southlat, nlat=northlat,
                                           wlon=westlon, elon=eastlon, folderpath=folderpath, filesuf=filesuf,
                                           reg_name=reg_name, extra_name=f'{extra_name}{season_name}', proj=proj,
                                           central_lon_180=central_lon_180,
                                           LatMin=LatMin, LatMax=LatMax, LonMin=LonMin, LonMax=LonMax,
                                           **kwargs_mapvals)

#################################################################################################
#
# Make Excel file of monthly tagged values for each case (not season/forcing dependent - written once)
#
#################################################################################################

if MAKE_EXCEL:

    monthly_watertag_values_to_excel(CASES=CASES, cases=cases, begi=begi, endi=endi,
                                     tagnames=tagnames, tagcodes=tagcodes, folderpath=folderpath,
                                     slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon,
                                     reg_name=reg_name)

print('\nDone.')
