####################################################################################################################
#
# Plot global maps of total precipitation and d18Op anomalies (LGM forcing minus 0ka PI control)
# with 850 hPa wind vector overlays, for ANN and four seasons.
#
# Forcing experiments:
#   Full forcing  (21ka      - 0ka)
#   GHG           (21kaGHG   - 0ka)
#   Glacial       (21kaGlac  - 0ka)
#   Sea level     (21kaSL    - 0ka)
#
# Variables:
#   Total precipitation  (PRECC + PRECL, mm/day)
#   Precipitation d18O   (d18Op, per mil)
#
# Years used: 6-25 of each climatology file (same as water tagging analysis)
#
####################################################################################################################

import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cmaps

from ESMplot.climate_analysis import seas_avg_LL as seasavg
from ESMplot.plotting.plot_map_avg_functions import plot_contour_map_avg

####################################################################################################################
#
# Specifications
#
####################################################################################################################

#-------------------------------------------------
# Which variables to plot
#-------------------------------------------------

PLOT_PRECT = False
PLOT_d18Op = True

#-------------------------------------------------
# Cases
#-------------------------------------------------

dir   = '/paleonas/ajthompson/postproc/'
model = 'cam'

# 0ka control (index 0) + 4 forcing experiments (indices 1-4)
CASES = [
    dir + 'f.e12.F_1850_CAM5.wiso.f19.0ka.002.watertags.2.'                                          + model + '.h0.0006-0025.climo.nc',
    dir + 'f.e12.F_1850_CAM5.wiso.f19.21ka.fullforcing.modern.d18Osw.001.watertags.'                 + model + '.h0.0006-0025.climo.nc',
    dir + 'f.e12.F_1850_CAM5.wiso.f19.21kaGHG.001.watertags.2.'                                      + model + '.h0.0006-0025.climo.nc',
    dir + 'f.e12.F_1850_CAM5.wiso.f19.21kaGlac.001.watertags.2.'                                     + model + '.h0.0006-0025.climo.nc',
    dir + 'f.e12.F_1850_CAM5.wiso.f19.21kaSL.002.watertags.'                                         + model + '.h0.0006-0025.climo.nc',
]

# Labels used in plot titles and file names
cases = [
    '0ka',
    '$21ka$',
    '$21ka_{GHG}$',
    '$21ka_{GLAC}$',
    '$21ka_{SL}$',
]


cases_diff = [f'{cases[i]}-{cases[0]}' for i in range(1, len(cases))]

begi = 'beg'
endi = 'end'

#-------------------------------------------------
# Monthly weights
#-------------------------------------------------

wgt_vals = np.array([0.084931507, 0.076712329, 0.084931507, 0.082191781,
                     0.084931507, 0.082191781, 0.084931507, 0.084931507,
                     0.082191781, 0.084931507, 0.082191781, 0.084931507])

#-------------------------------------------------
# Seasons
#-------------------------------------------------

SEASONS = {
    'ANN': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'DJF': [11, 0, 1],
    'MAM': [2, 3, 4],
    'JJA': [5, 6, 7],
    'SON': [8, 9, 10],
}

#-------------------------------------------------
# Wind vector specifications
#-------------------------------------------------

overlay_vec  = True
WIND_LEVEL   = 850
plev         = np.arange(0, 1050, 50)

vec_scale    = 100.    # fallback only; per-panel percentile scaling (below) normally takes over
vec_pctl     = 95.     # percentile of wind speed (within LatMin:LatMax) used to set each panel's scale
vec_arrow_frac = 0.1   # fraction of axis height a vec_pctl-magnitude arrow should span; tune for arrow length
vec_key_yoffset = -0.08  # figure-fraction gap below each panel where the reference key is drawn; more negative = more clearance
vec_ref      = 2.
vec_units    = 'm/s'
vec_name     = f'850hPaWind'
vec_wid      = 0.002
vec_hdl      = 4.
vec_hdw      = 4.
vec_hal      = 4.
vec_skip     = 4

#-------------------------------------------------
# Contour levels — difference plots
#-------------------------------------------------

# Precipitation anomaly
p_loval    = -1
p_hival    =  1
p_spval    =  0.1
p_tkstd    =  0.25
p_extnd    = 'both'
p_units    = 'mm/day'
p_colort   = cmaps.BlueYellowRed_r

# d18Op anomaly
o_loval    = -1.5
o_hival    =  1.5
o_spval    =  0.1
o_tkstd    =  0.5
o_extnd    = 'both'
o_units    = 'per mil'
o_colort   = cmaps.BlueYellowRed

#-------------------------------------------------
# Map specifications
#-------------------------------------------------

LatMin = -45.;  LatMax = 45.
LonMin = -180.; LonMax = 180.
proj   = ccrs.PlateCarree(central_longitude=180.)

cntr_type  = 'RasterFill'
folderpath = 'pdfs'
filesuf    = '_lowlat.pdf'

####################################################################################################################
#
# Load data and make plots — loop over seasons
#
####################################################################################################################

for season_name, MON in SEASONS.items():

    print(f'\n==============================')
    print(f'Season: {season_name}')
    print(f'==============================')

    # Build per-season monthly weights
    if len(MON) == 12:
        wgt_mon = xr.DataArray(wgt_vals, dims=['time'])
    else:
        sub = wgt_vals[MON]
        wgt_mon = xr.DataArray(sub / sub.sum(), dims=['time'])

    #-----------------------------------------------------------------
    # Load all cases
    #-----------------------------------------------------------------

    print('  Loading precipitation...')
    prect_all = xr.concat(
        [seasavg.seasavg_prect_LL(months=MON, path=c, begi=begi, endi=endi, wgt_mon=wgt_mon)
         for c in CASES],
        dim='case'
    ).assign_coords(case=cases)

    print('  Loading d18Op...')
    d18Op_all = xr.concat(
        [seasavg.seasavg_rainiso_LL(iso_type='d18O', months=MON, path=c,
                                    begi=begi, endi=endi, wgt_mon=wgt_mon)
         for c in CASES],
        dim='case'
    ).assign_coords(case=cases)

    if overlay_vec:
        print('  Loading 850 hPa winds...')
        u_list, v_list = [], []
        for c in CASES:
            u_i, v_i = seasavg.seasavg_wind_vec_LL(months=MON, path=c, begi=begi, endi=endi,
                                                    level=WIND_LEVEL, plev=plev, wgt_mon=wgt_mon)
            u_list.append(u_i)
            v_list.append(v_i)
        u_all = xr.concat(u_list, dim='case').assign_coords(case=cases)
        v_all = xr.concat(v_list, dim='case').assign_coords(case=cases)

    #-----------------------------------------------------------------
    # Build difference arrays: each forcing minus 0ka (index 0)
    #-----------------------------------------------------------------

    prect_diff = xr.concat(
        [prect_all.sel(case=cases[i]) - prect_all.sel(case=cases[0])
         for i in range(1, len(cases))],
        dim='case'
    ).assign_coords(case=cases_diff)

    d18Op_diff = xr.concat(
        [d18Op_all.sel(case=cases[i]) - d18Op_all.sel(case=cases[0])
         for i in range(1, len(cases))],
        dim='case'
    ).assign_coords(case=cases_diff)

    if overlay_vec:
        u_diff = xr.concat(
            [u_all.sel(case=cases[i]) - u_all.sel(case=cases[0])
             for i in range(1, len(cases))],
            dim='case'
        ).assign_coords(case=cases_diff)
        v_diff = xr.concat(
            [v_all.sel(case=cases[i]) - v_all.sel(case=cases[0])
             for i in range(1, len(cases))],
            dim='case'
        ).assign_coords(case=cases_diff)

    #-----------------------------------------------------------------
    # Plot precipitation anomaly
    #-----------------------------------------------------------------

    if PLOT_PRECT:

        print(f'  Plotting precipitation anomaly [{season_name}]...')

        if not overlay_vec:
            u_diff, v_diff = None, None

        plot_contour_map_avg(
            var=prect_diff,
            cases=cases_diff,
            var_name='Precip',
            seas=season_name,
            units=p_units,
            proj=proj,
            cntr_type=cntr_type,
            colort=p_colort,
            loval=p_loval, hival=p_hival, spval=p_spval, tkstd=p_tkstd, extnd=p_extnd,
            LatMin=LatMin, LatMax=LatMax, LonMin=LonMin, LonMax=LonMax,
            overlay_vec=overlay_vec,
            u=u_diff, v=v_diff,
            vec_scale=vec_scale, vec_pctl=vec_pctl, vec_arrow_frac=vec_arrow_frac, vec_key_yoffset=vec_key_yoffset,
            vec_ref=vec_ref, vec_units=vec_units, vec_name=vec_name,
            vec_wid=vec_wid, vec_hdl=vec_hdl, vec_hdw=vec_hdw, vec_hal=vec_hal, vec_skip=vec_skip,
            Ind_plots=True,
            folderpath=folderpath,
            extra_name=season_name,
            filesuf=filesuf,
        )

    #-----------------------------------------------------------------
    # Plot d18Op anomaly
    #-----------------------------------------------------------------

    if PLOT_d18Op:

        print(f'  Plotting d18Op anomaly [{season_name}]...')

        if not overlay_vec:
            u_diff, v_diff = None, None

        plot_contour_map_avg(
            var=d18Op_diff,
            cases=cases_diff,
            var_name='d18Op',
            seas=season_name,
            units=o_units,
            proj=proj,
            figw=10,figh=5,
            hspace=0.1,wspace=0.1,
            cbar_pad=0.12,
            cntr_type=cntr_type,
            colort=o_colort,
            loval=o_loval, hival=o_hival, spval=o_spval, tkstd=o_tkstd, extnd=o_extnd,
            LatMin=LatMin, LatMax=LatMax, LonMin=LonMin, LonMax=LonMax,
            overlay_vec=overlay_vec,
            u=u_diff, v=v_diff,
            vec_scale=vec_scale, vec_pctl=vec_pctl, vec_arrow_frac=vec_arrow_frac, vec_key_yoffset=vec_key_yoffset,
            vec_ref=vec_ref, vec_units=vec_units, vec_name=vec_name,
            vec_wid=vec_wid, vec_hdl=vec_hdl, vec_hdw=vec_hdw, vec_hal=vec_hal, vec_skip=vec_skip,
            Ind_plots=True,
            folderpath=folderpath,
            extra_name=season_name,
            filesuf=filesuf,
        )

print('\nDone.')
