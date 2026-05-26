####################################################################################################################
#
# Calculate and plot rainfall and d18Op results from water tagged iCESM simulation(s)
# 
# *** This script produces global d18Op and precip maps for: ***
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
###################################################################################################################

import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cmaps
from matplotlib import colors
from ESMplot.watertagging.print_watertag_values import print_watertag_values, monthly_watertag_values_to_excel
from ESMplot.watertagging.watertag_plots_cenlon_LGMregions import watertagging_values_on_map, plot_tagged_precip_and_d18Op
from ESMplot.watertagging.seas_avg_LL_watertags import seasavg_watertagging_vars
from ESMplot.climate_analysis import seas_avg_LL as seasavg
from ESMplot.climate_analysis.coordinate_functions import lat_lon_index_array

#########################################################
#
# Specifications for plots are made here
#
#########################################################

#------------------------------------------------
# Which plots to include in output
#------------------------------------------------

IND_PRECIP = True
IND_d18Op  = True

#------------------------------------------------
# Specify data path variables 
#------------------------------------------------

dir   = '/paleonas/ajthompson/postproc/'
model = 'cam'

# 0ka control (index 0 — always the reference case)
# Forcing experiments (indices 1–4): Full, GHG, Glac, SL
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

# Anything extra to add to output file names?
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

reg_name = ''

# EquatorSouthAmerica
southlat = -10
northlat =   0
westlon  = -60
eastlon  = -30

#-----------------------------------------------------------------
# Contour levels for DIFF plots
#-----------------------------------------------------------------

# Precipitation
p_hival   =  0.5
p_loval   = -0.5
p_spval   =  0.05
p_mantick = [-0.5, -0.25, 0., 0.25, 0.5]
p_extnd   = 'both'

# d18Op
o_hival =  1.
o_loval = -1.
o_spval =  0.1
o_tkstd =  0.5
o_extnd = 'both'

#------------------------------------------------------------
# Map extent
#------------------------------------------------------------

World  = True

if World:
    LatMin = -90;  LatMax = 90
    LonMin = -180; LonMax = 180
else:
    LatMin = -5.;  LatMax = 60.
    LonMin = -140.; LonMax = 0.

# Pacific-centered projection
central_lon_180 = True

#---------------------------------------------------------------
# Vector overlay specifications
#---------------------------------------------------------------

overlay_vec  = True
overlay_type = 'wind'

plev       = np.arange(0, 1050, 50)
WIND_LEVEL = 850
WIND_UNITS = 'm/s'
# vec_scale_ref: the vec_scale that looks correct for the full forcing difference.
# The dynamic scaling will anchor all other forcings relative to this value.
vec_scale_ref = 200.
kwargs_WIND = dict(vec_name=f'{overlay_type}{WIND_LEVEL}hPa',
                   vec_units='m/s', vec_ref=10., vec_scale=vec_scale_ref, vec_skip=4)

ptop_lev = 50.
pbot_lev = 1018.
kwargs_IVT = dict(vec_name=f'{overlay_type}{int(ptop_lev)}-{int(pbot_lev)}hPa',
                  vec_units='kg/(m*s)', vec_ref=250., vec_scale=3000.)

kwargs_vec = kwargs_WIND if overlay_type == 'wind' else kwargs_IVT if overlay_type == 'IVT' else None

#-------------------------------------------------
# Plotting specifications
#-------------------------------------------------

proj         = ccrs.PlateCarree(central_longitude=180.) if central_lon_180 else ccrs.PlateCarree()
Contour_type = 'RasterFill'
folderpath   = 'pdfs'
filesuf      = '.pdf'

colorp = cmaps.BlueYellowRed_r
coloro = cmaps.BlueYellowRed

kwargs_mapvals  = dict(tag_fs=3.0, bckgrnd_col='w', bckgrnd_pad=0.08, tag_zorder=1)
kwargs_cntrplot = dict(figw=10., figh=10., fdpi=300.)
kwargs_diffplot = dict(figw=10., figh=10., fdpi=300., cutoff=0.,
                       central_lon_180=central_lon_180, regbox=False)

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

    Pi_by_tag       = xr.DataArray(None, dims=['case','tag','lat','lon'],
                                   coords=dict(case=cases, tag=tagcodes, lat=lat, lon=lon)).astype(float)
    d18Opsink_by_tag = xr.DataArray(None, dims=['case','tag','lat','lon'],
                                    coords=dict(case=cases, tag=tagcodes, lat=lat, lon=lon)).astype(float)
    d18Opwt_by_tag  = xr.DataArray(None, dims=['case','tag','lat','lon'],
                                   coords=dict(case=cases, tag=tagcodes, lat=lat, lon=lon)).astype(float)

    prect    = xr.DataArray(None, dims=['case','tag'], coords=dict(case=cases, tag=tagcodes))
    d18Op    = xr.DataArray(None, dims=['case','tag'], coords=dict(case=cases, tag=tagcodes))
    prect_reg = xr.DataArray(None, dims=['case'], coords=dict(case=cases))
    d18Op_reg = xr.DataArray(None, dims=['case'], coords=dict(case=cases))
    prect_sum = xr.DataArray(None, dims=['case'], coords=dict(case=cases))
    d18Op_sum = xr.DataArray(None, dims=['case'], coords=dict(case=cases))

    if overlay_vec:
        U = xr.DataArray(None, dims=['case','lat','lon'],
                         coords=dict(case=cases, lat=lat, lon=lon)).astype(float)
        V = xr.DataArray(None, dims=['case','lat','lon'],
                         coords=dict(case=cases, lat=lat, lon=lon)).astype(float)
    else:
        U, V = None, None

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

        # Derived quantities
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

        # Wind vectors
        if overlay_vec:
            if overlay_type == 'wind':
                U[i,:,:], V[i,:,:] = seasavg.seasavg_wind_vec_LL(
                    path=CASES[i], begi=begi, endi=endi, level=WIND_LEVEL,
                    plev=plev, months=MON, wgt_mon=wgt_mon_i)
            elif overlay_type == 'IVT':
                U[i,:,:], V[i,:,:] = seasavg.seasavg_IVT_vec_LL(
                    path=CASES[i], begi=begi, endi=endi, ptop=ptop_lev,
                    pbot=pbot_lev, plev=plev, months=MON, wgt_mon=wgt_mon_i)

    #-----------------------------------------------------------------
    # Plot: loop over forcing experiments (1–4), diff against 0ka
    #-----------------------------------------------------------------

    print(f'  Plotting maps for {season_name}...')

    # Compute p95 of full forcing wind anomaly magnitude (case index 1 = full forcing).
    # All forcings are scaled relative to this so that full forcing uses vec_scale_ref
    # and weaker forcings get proportionally longer arrows.
    if overlay_vec:
        u_full = (U[1,:,:] - U[0,:,:]).values
        v_full = (V[1,:,:] - V[0,:,:]).values
        p95_full = np.nanpercentile(np.sqrt(u_full**2 + v_full**2), 95)
        if p95_full == 0.:
            p95_full = 1.  # fallback to avoid division by zero
    
    for i in range(1, len(CASES)):

        print(f'    {cases[i]}-{cases[0]}  [{season_name}]')

        # Scale vec_scale proportionally: full forcing gets vec_scale_ref,
        # weaker forcings get a smaller vec_scale (= longer arrows).
        if overlay_vec:
            u_diff = (U[i,:,:] - U[0,:,:]).values
            v_diff = (V[i,:,:] - V[0,:,:]).values
            p95_i  = np.nanpercentile(np.sqrt(u_diff**2 + v_diff**2), 95)
            if p95_i > 0.:
                vec_scale_dynamic = vec_scale_ref * (p95_i / p95_full)
            else:
                vec_scale_dynamic = vec_scale_ref
        else:
            vec_scale_dynamic = vec_scale_ref

        # Build a kwargs_vec copy with the updated scale
        kwargs_vec_dynamic = {**kwargs_vec, 'vec_scale': vec_scale_dynamic}

        plot_tagged_precip_and_d18Op(
            # Required variables
            P=IND_PRECIP, O=IND_d18Op, season=season_name,
            prect=Pi_by_tag[i,:,:,:] - Pi_by_tag[0,:,:,:],
            d18Op=d18Opwt_by_tag[i,:,:,:] - d18Opwt_by_tag[0,:,:,:],
            lat=lat, lon=lon,
            num_landtags=num_landtags, num_oceantags=num_oceantags,
            tagnames=tagnames, case=f'{cases[i]}-{cases[0]}',

            # Wind vectors
            overlay_vec=overlay_vec,
            u=U[i,:,:] - U[0,:,:] if overlay_vec else None,
            v=V[i,:,:] - V[0,:,:] if overlay_vec else None,
            **kwargs_vec_dynamic,

            # Mapping specifications
            colorp=colorp, coloro=coloro, cntr_type=Contour_type, proj=proj,
            p_hival=p_hival, p_loval=p_loval, p_spval=p_spval,
            p_mantick=p_mantick, p_extnd=p_extnd,
            o_hival=o_hival, o_loval=o_loval,
            o_spval=o_spval, o_tkstd=o_tkstd, o_extnd=o_extnd,
            slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon,
            LatMin=LatMin, LatMax=LatMax, LonMin=LonMin, LonMax=LonMax,

            # Output file naming
            folderpath=folderpath, filesuf=filesuf,
            reg_name=reg_name,
            extra_name=season_name,

            # All other kwargs
            **kwargs_diffplot)

print('\nDone.')
