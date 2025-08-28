import sys, os
sys.path.append(os.path.dirname(os.getcwd()))  # one dir back
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cmaps
from matplotlib import colors
from ESMplot.watertagging.print_watertag_values import (
    print_watertag_values, monthly_watertag_values_to_excel,
)
from ESMplot.watertagging.watertag_plots import (
    watertagging_values_on_map, plot_tagged_precip_and_d18Op,
)
from ESMplot.watertagging.seas_avg_LL_watertags import seasavg_watertagging_vars
from ESMplot.climate_analysis import seas_avg_LL as seasavg
from ESMplot.climate_analysis.coordinate_functions import lat_lon_index_array

# New: timing + rich progress
import time
from rich.progress import (
    Progress,
    TimeElapsedColumn,
    TimeRemainingColumn,
    BarColumn,
    MofNCompleteColumn,
)

t0 = time.time()

#########################################################
#
# Specifications for plots are made here
#
#########################################################

#------------------------------------------------
# Which plots to include in output...
#------------------------------------------------

# Global maps with values for precip, precip pct, and d18Op
TEXT_MAPS = True

# Print values for each tag region to screen
PRINT_VAL = False

# Individual global maps of...
IND_PRECIP = False
IND_d18Op  = False

# Excel sheet with monthly values for each tagged region by month
MAKE_EXCEL = False

# For the above three outputs, should they be differences between cases?
DIFF = False

#------------------------------------------------
# Specify data path variables
#------------------------------------------------

# Component model to specify in case strings
model = 'cam'

# File paths and names for each case
#direct = '/glade/derecho/scratch/aflaim/iCESM_testcases/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/archive/atm/hist/'
direct = '/RAID/datasets/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/products/'

# 20yr water tagging experiments (cam only)
CASES = [
    #direct + 'f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.210501-212412.nc'
    direct + 'f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124_monthly_climatology_cat.nc'
]

cases = ['2100CE']
#CASES = ['f.e12.F_1850_CAM5.wiso.f19.0ka.002.watertags.2.'+model+'.h0.0006-0025.climo.nc',
#        'f.e12.F_1850_CAM5.wiso.f19.21ka.fullforcing.modern.d18Osw.001.watertags.'+model+'.h0.0006-0025.climo.nc',
#        'f.e12.F_1850_CAM5.wiso.f19.21kaGHG.001.watertags.2.'+model+'.h0.0006-0025.climo.nc',
#        'f.e12.F_1850_CAM5.wiso.f19.21kaGlac.001.watertags.2.'+model+'.h0.0006-0025.climo.nc']
#cases = ['0ka',
#         '$21ka$',
#         '$21ka_{GHG}$',
#         '$21ka_{GLAC}$']

# Anything extra to add to output file name?
extra_name = '210501-212412'

#--------------------------------
# Seasonal averaging variables
#--------------------------------

# Indices to define range of time dimension read in from files; 'beg' and 'end' specify entire file length
begi = 'beg'  # 'beg' or index like 0
endi = 'end'  # 'end' or index like 12

# Season to average over, indices corresponding to individual months, season string will automatically populate later
MON = [0,1,2,3,4,5,6,7,8,9,10,11]
#MON = [6,7,8,9]
#MON = [5,6,7]
#MON = [11,0,1]

# Reference list for indices
# Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
#   0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11

#---------------------------------------------------------------------------------------
# Specify monthly weights, if necessary
#---------------------------------------------------------------------------------------

# Array with 12 months of weights
wgt_by_mon = xr.DataArray(None, dims=['case','month'], coords=dict(case=cases,month=np.arange(1,13,1))).astype(float)

# Array with n (based on MON) months of weights
# NOTE: Here we are not specifying the 'time' or 'month' coord so weighting with var_time will work
wgt_mon = xr.DataArray(np.zeros([len(cases),len(MON)]), dims=['case','time'], coords=dict(case=cases)).astype(float)

### Enter monthly weights for each case here
#...............................................................................................................
# 0ka
wgt_by_mon[0,:] = np.array([0.08493151,0.076712325,0.08493151,0.08219178,0.08493151,0.08219178,
                            0.08493151,0.08493151 ,0.08219178,0.08493151,0.08219178,0.08493151])
# 21ka
wgt_by_mon[1:,:] = np.array([0.084931507,0.076712329,0.084931507,0.082191781,0.084931507,0.082191781,
                             0.084931507,0.084931507,0.082191781,0.084931507,0.082191781,0.084931507])
#...............................................................................................................

# Modify depending if averaging over entire year or only a select few months
for i in range(len(cases)):
    wgt_mon[i,:] = wgt_by_mon[i,:] if len(MON) == 12 else wgt_by_mon[i,MON]/np.sum(wgt_by_mon[i,MON])

#----------------------------------------------------------------------------------
# Water tagging variables, plotting boundaries takes place in a separate function
#----------------------------------------------------------------------------------

# Long-form name of each tag (in order)
tagnames = ['Antarctica','Western North America','Eastern North America','South America (-Amazon)','Europe','Northern Asia','India','Southeast Asia','Africa (-Congo)','Sundaland combined',
            'Sahulland','Australia/Oceania','Amazon','Congo','Western North Pacific','Eastern North Pacific',
            'Western North Atlantic','Eastern North Atlantic','North Barents/Arctic Sea','Tropical Pacific NE','Caribbean','Tropical Atlantic NW',
            'Tropical Atlantic NE','Mediterranean','Indian Ocean NW/Arabian Sea','Indian Ocean NE/Bay of Bengal',
            'Sundaland ocean combined',
            'Tropical Pacific NW','Tropical Pacific North Central','Tropical Pacific SE','Tropical Atlantic SW',
            'Tropical Atlantic SE','Tropical Indian SW','Tropical Indian South Central','Tropical Indian SE',
            'Sahul region ocean','Tropical Pacific South Central','South Pacific','South Atlantic','South Indian']

# Code name of each tag (in order)
tagcodes = ['ANTA','WNAM','ENAM','SAME','EURO',
            'NASA','INDA','SASA','AFRI','SLCB',
            'SAHL','AUST','AMAZ','CONG',          # Land end
            'ENPA','WNPA','WNAT','ENAT','ARCT',
            'TPNE','CARB','TANW','TANE','MEDI',
            'ARAB','BOFB','SOCB','TPNW','TPNC',
            'TPSE','TASW','TASE','TISW','TISC',
            'TISE','SAHO','TPSC','SPAC','SATL','SIND']

# Number of land vs. ocean tags
num_landtags  = 14
num_oceantags = 26

# Lat/lon values for plotting text in land and ocean tag region plots
# if central_longitude - 0. (default), lat/lon values are read as specified below

# Tag codes:ANTA,WNAM,ENAM,SAME,EURO,NASA,INDA,SASA,AFRI,SLCB,SAHL,AUST,AMAZ,CONG,
landlat  = [ -81,  38,  38, -20,  58,  58,  20,  25,  20,   4,  -7, -26,   0,   3]
landlon =  [   0,-130, -50, -58,  30,  90,  80, 105,  20, 105, 135, 135, -61,  22]

# Tag codes:ENPA,WNPA,WNAT,ENAT,ARCT,TPNE,CARB,TANW,TANE,MEDI,ARAB,BOFB,SOCB,TPNW,TPNC,TPSE,TASW,TASE,TISW,TISC,TISE,SAHO,TPSC,SPAC,SATL,SIND
oceanlat = [  36,  36,  60,  60,  60,   8,  30,  15,  15,  40,  10,  20,   4,  15,  15, -15, -15, -15,  -8, -15, -18,  -7, -15,  -40, -40,-40]
oceanlon = [-150, 150, -60,   0,  70,-120, -90, -50,   0,  22,  63,  85, 105, 135, 160,-113, -30,   5,  55,  80, 108, 135, 160, -130, -30, 75]

#------------------------------------------------------------------------------------------
# Define region for which water tagging results will be calculated
#------------------------------------------------------------------------------------------

# Name the region
reg_name = 'ncrcat_test'

# SundaSahul, slat=-12., nlat=10., wlon=90., elon=130.

# Define bounds (for single grid cell, set lats as same value and lons as same value)
# negative values = °S and °W, positive values = °N and °E
southlat = 14.0
northlat = 18.0
westlon  = -92.5
eastlon  = -90.0

#-----------------------------------------------------------------
# Specify individual map plot contour levels for prect and d18Op
#-----------------------------------------------------------------

# When DIFF == False, modify these values for contour levels
if DIFF == False:

    # Precipitation contours are set manually to include tick for cutoff value
    p_hival   = 2.                          # high value
    p_loval   = 0.                          # low value
    p_spval   = 0.1                         # spacing
    p_mantick = [0.001,0.2,0.5,1.0,1.5,2.0] # manual colorbar ticks
    p_extnd   = 'max'                       # placement of triangles

    # d18Op contours are set based on the following parameters
    o_hival = 0.           # high value
    o_loval = -2.5         # low value
    o_spval = 0.1          # spacing
    o_tkstd = 0.5          # tick stride
    o_extnd = 'both'       # placement of triangles

# When DIFF == True, modify these values for contour levels
if DIFF == True:

    # Precipitation contours are set based on the following parameters
    p_hival   = 0.5                         # high value
    p_loval   = -0.5                        # low value
    p_spval   = 0.05                        # spacing
    p_mantick = [-0.5,-0.25,0.,0.25,0.5]    # manual colorbar ticks
    p_extnd   = 'both'                      # placement of triangles

    # d18Op contours are set based on the following parameters
    o_hival = 1.           # high value
    o_loval = -1.          # low value
    o_spval = 0.1          # spacing
    o_tkstd = 0.5          # tick stride
    o_extnd = 'both'       # placement of triangles

#------------------------------------------------------------
# For map plots, zoom into any world region in particular?
#------------------------------------------------------------

# True=entire world, False=zoomed in to coordinate values in second block
World = True

if World == True:
    LatMin = -90
    LatMax = 90
    LonMin = -180
    LonMax = 180
else:
    LatMin = -5.   #   -15.0     # negative values = °S
    LatMax = 60.   #    90.0     # positive values = °N
    LonMin = -140. #  -180.0     # negative values = °W
    LonMax = 0.    #    60.0     # positive values = °E

#---------------------------------------------------------------
# Specify vectors to overlay on plot, if necessary
#---------------------------------------------------------------

# Overlay a vector? If True, what type and level of the atmosphere?
overlay_vec  = True
overlay_type = 'IVT'   # 'wind','IVT'

# Define pressure levels with this array, ex. Pressure array goes from 0 hPa to 1000 hPa by 50 hPa
plev = np.arange(0,1050,50)

# Variables for overlay_type == 'wind', uses 'plev' from above
WIND_LEVEL = 700   # Integer, in hPa
WIND_UNITS = 'm/s' # Text string
kwargs_WIND = dict(vec_name=f'{overlay_type}{WIND_LEVEL}hPa',
                   vec_units='m/s',vec_ref=10.,vec_scale=200.,vec_skip=4)

# Variables for overlay_type == 'IVT', uses 'plev' from above
ptop_lev = 50.   # in hPa
pbot_lev = 1018. # in hPa
kwargs_IVT = dict(vec_name=f'{overlay_type}{int(ptop_lev)}-{int(pbot_lev)}hPa',
                  vec_units='kg/(m*s)',vec_ref=250.,vec_scale=3000.)

# Define which kwargs to pass: wind or ivt
kwargs_vec = kwargs_WIND if overlay_type == 'wind' else kwargs_IVT if overlay_type == 'IVT' else None
if overlay_vec == False:
    u_avg_by_case, v_avg_by_case = None, None

#-------------------------------------------------
# Plotting specifications are set here
#-------------------------------------------------

proj         = ccrs.PlateCarree()  # Map projection
Contour_type = 'RasterFill'        # 'RasterFill' or 'AreaFill'
folderpath   = 'pdfs'              # folder to output file to
filesuf      = '.pdf'              # type of output file

# When DIFF == False, modify these to set color tables
if DIFF == False:
    colorp = cmaps.cmp_haxby_r       # Contour plot color table, "_r" at end reverses color table
    coloro = colors.LinearSegmentedColormap.from_list('name', cmaps.cmp_haxby(np.arange(50)))
    # Remove last color (white) from cmp_haxby

# When DIFF == True, modify these to set color tables
elif DIFF == True:
    colorp = cmaps.BlueYellowRed_r
    coloro = cmaps.BlueYellowRed

#-------------------------------------------------
# Other specifications are set here as kwargs
#-------------------------------------------------

kwargs_mapvals  = dict(tag_fs=3.0,bckgrnd_col='w',bckgrnd_pad=0.08,tag_zorder=1,central_lon_180=False)
kwargs_cntrplot = dict(figw=10.,figh=10.,fdpi=300.)
kwargs_diffplot = dict(figw=10.,figh=10.,fdpi=300.,cutoff=0.)

###############################################################################
#
# Loop through each case to create variables
#
###############################################################################

#-------------------------------------------------------
# Make season string automatically from season indices
#-------------------------------------------------------

month_by_letter = ['J','F','M','A','M','J','J','A','S','O','N','D']
season = 'ANN' if len(MON) == 12 else ''.join([month_by_letter[i] for i in MON])

#-----------------------------------------------------------------
# Create multidimensional variable(s) [# of cases x lat x lon]
#-----------------------------------------------------------------

# Dataset for dimensions
ds = xr.open_dataset(CASES[0])

# Global variables [case,lat,lon]
prect_global = xr.DataArray(None, dims=['case','lat','lon'],
                            coords=dict(case=cases,lat=ds.lat,lon=ds.lon)).astype(float)
d18Op_global = xr.DataArray(None, dims=['case','lat','lon'],
                            coords=dict(case=cases,lat=ds.lat,lon=ds.lon)).astype(float)

# Variables by tag [case,tag,lat,lon]
Pi_by_tag = xr.DataArray(None, dims=['case','tag','lat','lon'],
                         coords=dict(case=cases,tag=tagcodes,lat=ds.lat,lon=ds.lon)).astype(float)
d18Opsink_by_tag = xr.DataArray(None, dims=['case','tag','lat','lon'],
                                coords=dict(case=cases,tag=tagcodes,lat=ds.lat,lon=ds.lon)).astype(float)
d18Opwt_by_tag = xr.DataArray(None, dims=['case','tag','lat','lon'],
                              coords=dict(case=cases,tag=tagcodes,lat=ds.lat,lon=ds.lon)).astype(float)
# Average value for each tag [case,tag]
prect = xr.DataArray(None, dims=['case','tag'], coords=dict(case=cases,tag=tagcodes))
d18Op = xr.DataArray(None, dims=['case','tag'], coords=dict(case=cases,tag=tagcodes))

# Global variable's average of the selected region
prect_reg = xr.DataArray(None, dims=['case'], coords=dict(case=cases))
d18Op_reg = xr.DataArray(None, dims=['case'], coords=dict(case=cases))

# Sum of all tagged region values
prect_sum = xr.DataArray(None, dims=['case'], coords=dict(case=cases))
d18Op_sum = xr.DataArray(None, dims=['case'], coords=dict(case=cases))

# Wind vectors if specified above
if overlay_vec == True:
    U = xr.DataArray(None, dims=['case','lat','lon'], coords=dict(case=cases,lat=ds.lat,lon=ds.lon)).astype(float)
    V = xr.DataArray(None, dims=['case','lat','lon'], coords=dict(case=cases,lat=ds.lat,lon=ds.lon)).astype(float)

#--------------------------
# Loop through each case with Rich progress
#--------------------------

with Progress(
    "[progress.description]{task.description}",
    BarColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
) as progress:

    cases_task = progress.add_task("Cases", total=len(CASES))

    for i in range(len(CASES)):
        progress.console.print(f"[bold]Working on {cases[i]}[/bold]")

        # -----------------------------------------------------------------
        # Global variables: prect and d18Op
        # -----------------------------------------------------------------
        prect_global[i,:,:] = seasavg.seasavg_prect_LL(
            path=CASES[i], begi=begi, endi=endi, months=MON, wgt_mon=wgt_mon[i,:]
        )
        d18Op_global[i,:,:] = seasavg.seasavg_rainiso_LL(
            iso_type='d18O', path=CASES[i], begi=begi, endi=endi,
            ptiny=1.E-18, months=MON, wgt_mon=wgt_mon[i,:]
        )

        # -----------------------------
        # Loop through each tag (inner progress)
        # -----------------------------
        tags_task = progress.add_task(f"Tags ({cases[i]})", total=len(tagnames))
        for tag in range(len(tagnames)):
            Pi_by_tag[i,tag,:,:], d18Opsink_by_tag[i,tag,:,:] = seasavg_watertagging_vars(
                tagcode=tagcodes[tag], months=MON, path=CASES[i], begi=begi, endi=endi, wgt_mon=wgt_mon[i,:]
            )
            progress.advance(tags_task)

        # -----------------------------------
        # Perform calculation on variables
        # -----------------------------------
        lat = ds.lat
        lon = ds.lon
        lat_wgts = np.cos(np.deg2rad(lat))

        # Create list arrays of lat and lon values for regional averaging
        latarray, lonarray = lat_lon_index_array(
            lat=ds.lat, lon=ds.lon, slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon
        )

        # Loop through each tag to calculate prect and d18Op tag region values
        for tag in range(len(tagnames)):
            # Use water tagging equation: d18Opwt@gc = d18Op_tag@gc * ( total16Op_tag@gc / prect_global@gc )
            d18Opwt_by_tag[i,tag,:,:] = d18Opsink_by_tag[i,tag,:,:] * (
                Pi_by_tag[i,tag,:,:] / prect_global[i,:,:]
            )

            # Area weight prect and d18Op for tagged region average
            prect_wgt    = Pi_by_tag[i,tag,latarray,lonarray].weighted(lat_wgts[latarray])
            prect[i,tag] = prect_wgt.mean(('lon','lat'))
            d18Op_wgt    = d18Opwt_by_tag[i,tag,latarray,lonarray].weighted(lat_wgts[latarray])
            d18Op[i,tag] = d18Op_wgt.mean(('lon','lat'))

        # Calculate tagged region average with global variables to check against tagged variables
        prect_global_wgt = prect_global[i,latarray,lonarray].weighted(lat_wgts[latarray])
        prect_reg[i]     = prect_global_wgt.mean(('lon','lat'))
        d18Op_global_wgt = d18Op_global[i,latarray,lonarray].weighted(lat_wgts[latarray])
        d18Op_reg[i]     = d18Op_global_wgt.mean(('lon','lat'))

        # Sum tag values together
        prect_sum[i] = np.sum(prect[i,:])
        d18Op_sum[i] = np.sum(d18Op[i,:])

        # Define wind vector variables if necessary
        if overlay_vec == True:
            if overlay_type == 'wind':
                U[i,:,:], V[i,:,:] = seasavg.seasavg_wind_vec_LL(
                    path=CASES[i], begi=begi, endi=endi, level=WIND_LEVEL,
                    plev=plev, months=MON, wgt_mon=wgt_mon[i,:]
                )
            if overlay_type == 'IVT':
                U[i,:,:], V[i,:,:] = seasavg.seasavg_IVT_vec_LL(
                    path=CASES[i], begi=begi, endi=endi, ptop=ptop_lev,
                    pbot=pbot_lev, plev=plev, months=MON, wgt_mon=wgt_mon[i,:]
                )
        elif overlay_vec == False:
            U, V = None, None

        progress.advance(cases_task)

########################################################################################################
#
# Make map/text plots for each case (diffs if specified above)
#
########################################################################################################

if TEXT_MAPS == True:
    print('Plotting text maps...')

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:

        if DIFF == False:
            task = progress.add_task("Text maps", total=len(CASES))
            for i in range(len(CASES)):
                progress.console.print(str(cases[i]))

                if PRINT_VAL == True:
                    print_watertag_values(
                        precip=prect[i,:], d18Op=d18Op[i,:], precip_sum=prect_sum[i], d18Op_sum=d18Op_sum[i],
                        precip_reg_gbl=prect_reg[i], d18Op_reg_gbl=d18Op_reg[i],
                        lat=lat, lon=lon, case=cases[i], tagnames=tagnames, season=season,
                        slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon,
                    )

                if TEXT_MAPS == True:
                    watertagging_values_on_map(
                        precip=prect[i,:], d18Op=d18Op[i,:], case=cases[i], tagnames=tagnames,
                        num_landtags=num_landtags, num_oceantags=num_oceantags, path=CASES[i],
                        season=season, lat=lat, lon=lon, landlat=landlat, landlon=landlon,
                        oceanlat=oceanlat, oceanlon=oceanlon, slat=southlat, nlat=northlat,
                        wlon=westlon, elon=eastlon, folderpath=folderpath, filesuf=filesuf,
                        reg_name=reg_name, extra_name=extra_name, proj=proj,
                        LatMin=LatMin, LatMax=LatMax, LonMin=LonMin, LonMax=LonMax,
                        **kwargs_mapvals,
                    )
                progress.advance(task)

        elif DIFF == True:
            task = progress.add_task("Text map diffs", total=max(0, len(CASES)-1))
            for i in range(1, len(CASES)):
                progress.console.print(cases[i]+'-'+cases[0])

                if PRINT_VAL == True:
                    print_watertag_values(
                        precip=prect[i,:]-prect[0,:], d18Op=d18Op[i,:]-d18Op[0,:],
                        precip_sum=prect_sum[i]-prect_sum[0], d18Op_sum=d18Op_sum[i]-d18Op_sum[0],
                        precip_reg_gbl=prect_reg[i]-prect_reg[0], d18Op_reg_gbl=d18Op_reg[i]-d18Op_reg[0],
                        lat=lat, lon=lon, case=str(cases[i]+'-'+cases[0]), tagnames=tagnames, season=season,
                        slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon,
                    )

                if TEXT_MAPS == True:
                    watertagging_values_on_map(
                        precip=prect[i,:], d18Op=d18Op[i,:], cntlp=prect[0,:], cntlo=d18Op[0,:], diff=True,
                        case=f'$\\Delta$({cases[i]} $\\minus$ {cases[0]})', tagnames=tagnames,
                        num_landtags=num_landtags, num_oceantags=num_oceantags, path=CASES[i],
                        season=season, lat=lat, lon=lon, landlat=landlat, landlon=landlon,
                        oceanlat=oceanlat, oceanlon=oceanlon, slat=southlat, nlat=northlat,
                        wlon=westlon, elon=eastlon, folderpath=folderpath, filesuf=filesuf,
                        reg_name=reg_name, extra_name=extra_name, proj=proj,
                        LatMin=LatMin, LatMax=LatMax, LonMin=LonMin, LonMax=LonMax,
                        **kwargs_mapvals,
                    )
                progress.advance(task)

#################################################################################################
#
# Make map plots for precipitation and d18Op for each tagged region (diffs if specified above)
#
#################################################################################################

if IND_PRECIP == True or IND_d18Op == True:
    print('Plotting maps for each tagged region...')

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:

        if DIFF == False:
            task = progress.add_task("Tag maps", total=len(CASES))
            for i in range(len(CASES)):
                progress.console.print(str(cases[i]))
                plot_tagged_precip_and_d18Op(
                    # Required variables for plot
                    P=IND_PRECIP, O=IND_d18Op, season=season,
                    prect=Pi_by_tag[i,:,:,:], d18Op=d18Opwt_by_tag[i,:,:,:], lat=lat, lon=lon,
                    num_landtags=num_landtags, num_oceantags=num_oceantags,
                    tagnames=tagnames, case=cases[i],

                    # Vector variables for plot
                    overlay_vec=overlay_vec, u=U[i,:,:], v=V[i,:,:], **kwargs_vec,

                    # Mapping specifications
                    colorp=colorp, coloro=coloro, proj=proj,
                    cntr_type=Contour_type, p_hival=p_hival, p_loval=p_loval, p_spval=p_spval,
                    p_mantick=p_mantick, p_extnd=p_extnd, o_hival=o_hival, o_loval=o_loval,
                    o_spval=o_spval, o_tkstd=o_tkstd, o_extnd=o_extnd,
                    slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon,
                    LatMin=LatMin, LatMax=LatMax, LonMin=LonMin, LonMax=LonMax,

                    # Naming conventions for output file
                    folderpath=folderpath, filesuf=filesuf,
                    reg_name=reg_name, extra_name=extra_name,

                    # All other specifications must be contained within kwargs_cntrplot
                    **kwargs_cntrplot,
                )
                progress.advance(task)

        else:  # DIFF == True
            task = progress.add_task("Tag map diffs", total=max(0, len(CASES)-1))
            for i in range(1, len(CASES)):
                progress.console.print(cases[i]+'-'+cases[0])
                plot_tagged_precip_and_d18Op(
                    # Required variables for plot
                    P=IND_PRECIP, O=IND_d18Op, season=season,
                    prect=Pi_by_tag[i,:,:,:]-Pi_by_tag[0,:,:,:],
                    d18Op=d18Opwt_by_tag[i,:,:,:]-d18Opwt_by_tag[0,:,:,:],
                    lat=lat, lon=lon, num_landtags=num_landtags, num_oceantags=num_oceantags,
                    tagnames=tagnames, case=str(cases[i]+'-'+cases[0]),

                    # Vector variables for plot
                    overlay_vec=overlay_vec, u=U[i,:,:]-U[0,:,:], v=V[i,:,:]-V[0,:,:], **kwargs_vec,

                    # Mapping specifications
                    colorp=colorp, coloro=coloro, cntr_type=Contour_type, proj=proj,
                    p_hival=p_hival, p_loval=p_loval, p_spval=p_spval,
                    p_mantick=p_mantick, p_extnd=p_extnd, o_hival=o_hival, o_loval=o_loval,
                    o_spval=o_spval, o_tkstd=o_tkstd, o_extnd=o_extnd,
                    slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon,
                    LatMin=LatMin, LatMax=LatMax, LonMin=LonMin, LonMax=LonMax,

                    # Naming conventions for output file
                    folderpath=folderpath, filesuf=filesuf,
                    reg_name=reg_name, extra_name=extra_name,

                    # All other specifications must be contained within kwargs_diffplot
                    **kwargs_diffplot,
                )
                progress.advance(task)

#################################################################################################
#
# Make Excel file of monthly tagged values for each case
#
#################################################################################################

if MAKE_EXCEL == True:
    print("Writing Excel…")
    monthly_watertag_values_to_excel(
        CASES=CASES, cases=cases, begi=begi, endi=endi,
        tagnames=tagnames, tagcodes=tagcodes, folderpath=folderpath,
        slat=southlat, nlat=northlat, wlon=westlon, elon=eastlon,
        reg_name=reg_name,
    )

print(f"Done in {time.time() - t0:,.1f}s")
