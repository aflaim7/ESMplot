#######################################################################################################
#
# These functions take an xr.DataArray input and generate seasonal average map plots for each case 
# contained within the variable. 
#
#######################################################################################################

import numpy as np
import xarray as xr
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib import colors
from matplotlib.backends.backend_pdf import PdfPages
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geocat.viz.util as gv
import cmaps
from ESMplot.plotting.plot_functions import save_multi_image,map_ticks_and_labels,draw_region_box

# Default variables
fig_let = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)',
           't)','u)','v)','w)','x)','y)','z)']

#######################################################################################################
# Plot contours in panel and individual map plots 
#######################################################################################################

def plot_contour_map_avg(
                         ### Required Parameters
                         var: xr.DataArray, 
 
                         ### Optional Parameters
                         cases: list = [''], var_name: str = '', seas: str = '', units: str = '',
                         figw: float = 10., figh: float = 10., fdpi: float = 300.,
                         hspace: float = None, wspace: float = None, fig_let: list = fig_let,
                         ttlloc: str = 'left', ttlfts: float = 12., ttlpad: float = 10.,
                         LatMin: float = -90., LatMax: float = 90., LonMin: float = -180.,
                         LonMax: float = 180., proj: ccrs.Projection = ccrs.PlateCarree(), 
                         coast: bool = True, coastlw: float = 0.75, lake: bool = False,
                         lakelw: float = 0.5, border: bool = True, borderlw: float = 0.75, 
                         usstate: bool = False, usstatelw: float = 0.5, add_axes: bool = True, 
                         latlblsp: float = 30., lonlblsp: float = 60., 
                         lattksp: int = 7, lontksp: int = 7, tklblsz: float = 10.,
                         tkmajlg: float = 4., tkminlg: float = 2., xmin_mj: int = 2, ymin_mj: int = 2,
                         xpads: float = 15., ypads: float = 15., 
                         glalpha: float = 0.0, glcolor: str = 'gray',
                         cntr_type: str = 'AreaFill', colort: colors.ListedColormap = cmaps.MPL_viridis, 
                         loval: float = None, hival: float = None, spval: float = None, 
                         tkstd: float = None, extnd: str = 'both', 
                         cbar_orient: str = 'horizontal', cbar_pad: float = 0.08, 
                         cbar_shrk: float = 0.6, cbar_sp: str = 'proportional', cbar_lblsz: float = 10.,
                         overlay_vec: bool = False, u: xr.DataArray = None, v: xr.DataArray = None,
                         vec_scale: float = 100., vec_pctl: float = 95., vec_arrow_frac: float = 0.1,
                         vec_key_yoffset: float = -0.05,
                         vec_wid: float = 0.002, vec_hal: float = 4.,
                         vec_hdl: float = 4., vec_hdw: float = 4., vec_skip: int = 2, 
                         vec_ref: float = 10., vec_units: str = '', vec_name: str = '',
                         regbox: bool = False, regcol: str = 'r', regline: str = '-', 
                         reglw: float = 1., regslat: float = None, regnlat: float = None, 
                         regwlon: float = None, regelon: float = None, 
                         point: bool = False, ptlat: float = None, ptlon: float = None,
                         shape_lats: list = [], shape_lons: list = [], shape_type: list = [], 
                         shape_size: list = [], shape_col: list = [], Ind_plots: bool = True,
                         extra_name: str = '', folderpath: str = '', filesuf: str = '.pdf'
                         ):

  '''Reads in an xr.DataArray of 2+ cases of a global variable and produces a panel plot and optional
  individual plots of each case in subsequent PDF pages.  

  Active issues with this script that need to be fixed:
  #1. Projection can't be changed from ccrs.PlateCarree() unless changing it in the function. This is
      an issue with geocat. 

  Required Parameters                       
  --------------------------------------------------------------------------------------------------------
  var
   class 'xarray.DataArray', The variable containing the values to be plot as contours on a map. Must 
                             contain the following dimensions: [# of cases x lat x lon]. # of cases needs 
                             to be two (2) or greater for this function. 

  Optional Parameters                       
  --------------------------------------------------------------------------------------------------------
  cases: class 'list', List of strings containing the name of case(s) that will be plotted. These strings 
                       will be displayed in the title of each map plot. Default = ['']
  var_name: class 'string', Name of the variable that will be plotted. This string will appear in the 
                            title of each map plot and in the file output name. Default = ''
  seas: class 'string', Name of season for which variable is averaged over. This string will be displayed 
                        in the title of each map plot and in the file output name. Default = ''
  units: class 'string', Specified units of variable. This string will be displayed underneath the 
                         colorbar. Default = ''
  figw, figh, fdpi: class 'float', Width (inches), height (inches), and DPI (dots per inch) of figure. 
                                   Default = 10., 10., 300.
  hspace, wspace: class 'float', Height and width of padding between subplots as a fraction of the average 
                                 Axes height/width, used in plt.subplots_adjust. If number of cases is an 
                                 odd number, this parameter is disabled and users should use figw and figh.
  fig_let: class 'list', List of letters to denote subplots. Spans a-z, but can be modified by specifying a 
                         new list. Default = ['a)','b)','c)', ... ,'z)']
  ttlloc: class 'string', Location of title above each subplot. Default = 'left'
  ttlfts: class 'float', Font size for title above each subplot. Default = 12.
  ttlpad: class 'float', Padding for title above each subplot. Default = 10.
  LatMin, LatMax, LonMin, LonMax: class 'float', Southern/northern latitude and western/eastern longitude
                                                 that sets extent of map to be plot. Values: 
                                                 LAT: - = °S, + = °N, range = -90 to 90
                                                 LON: - = °W, + = °E, range = -180 to 180
                                                 Default = -90., 90., -180., 180.
  proj: class 'cartopy.crs.Projection', Projection of map for each subplot. This parameter must be 
                                        cartopy.crs.PlateCarree() currently as cartopy's gridlines do not 
                                        support any other projection at this time. 
                                        Default = ccrs.PlateCarree()
  coast, coastlw: class 'bool','string', include coastlines on base map and if True, width of lines
                                         Default = True, 0.75
  lake, lakelw: class 'bool','string', include lakes on base map and if True, width of lines
                                       Default = False, 0.5  
  border, borderlw: class 'bool','string', include country borders on base map and if True, width of 
                                           lines. Default = True, 0.75
  usstate, usstatelw: class 'bool','float', include US state boundaries on base map and if True 
                                            width of lines. Default = False, 0.5
  add_axes: class 'bool', Add axes ticks and labels to each map. If True, the following tick and label
                          parameters are active. Default = True
  latlblsp, lonlblsp: class 'float', Spacing of latitude tick labels in degrees of latitude and 
                                     longitude. Default = 30., 60.
  lattksp, lontksp: class 'int', Tick spacing for major latitude and longitude ticks. Examples:
                                 lattksp = 7 -> -90 to 90 by 30 (7 total major ticks)
                                 lontksp = 7 -> -180 to 180 by 60 (7 total major ticks)
                                 Default = 7, 7
  tklblsz: class 'float', Font size of tick labels. Default = 10.
  tkmajlg: class 'float', Size of major ticks around the outline of each map. Default = 4.
  tkminlg: class 'float', Size of minor ticks around the outline of each map. Default = 2.
  xmin_mj: class 'int', Number of minor ticks in between each major tick on the x-axis (longitude).
                        Default = 2
  ymin_mj: class 'int', Number of minor ticks in between each major tick on the y-axis (latitude). 
                        Default = 2
  xpads, ypads: class 'float', Padding of x-axis longitude and y-axis latitude tick labels from 
                               map outline. Default = 15., 15.
  glalpha: class 'float', Alpha (line opacity) for gridlines between lat/lon ticks. Default is no 
                          gridlines. Modify 1.0 >= alpha > 0.0 for visible gridlines.
                          Default = 0.0 (no gridlines)
  glcolor: class 'str', Color of gridlines if glalpha > 0.0. Default = 'gray'
  cntr_type: class 'str', Type of contour for plotting. Options: 'AreaFill' - interpolated, 
                          'RasterFill' - raster. Default = 'AreaFill'
  colort: class 'colors.ListedColormap', Color table used for plotting contours. Specify names from cmaps 
                                         (https://github.com/hhuangwx/cmaps) or Matplotlib 
                                         (https://matplotlib.org/stable/tutorials/colors/colormaps.html)
                                         Default = cmaps.MPL_viridis
  loval: class 'float', Minimum value in contour levels. If not specified, will default to lowest value 
                        found in variable. 
  hival: class 'float', Maximum value in contour levels. If not specified, will default to highest value 
                        found in variable. 
  spval: class 'float', Stride (spacing value) in contour levels. If not specified, will default to 
                        (hival-loval)/10. 
  tkstd: class 'float', Stride of tick labels for color bar. If not specified, will default to spval. 
  extnd: :class:'str', Option to add triangles on either side of color bar that signify extended value 
                       range. Options: 'neither','max','min','both'. Default = 'both'
  cbar_orient: class 'str', Orientation of color bar. Options: 'horizontal','vertical'
                            Default = 'horizontal'
  cbar_pad: class 'float', Padding of color bar from bottom of map. Default = 0.08
  cbar_shrk: class 'float', Color bar shrink parameter. Modifies the sizing of the color bar. 
                            Default = 0.6
  cbar_sp: class 'str', Spacing of colors in color bar, If 'extnd' is not 'neither', this parameters
                        must be 'proportional'. Default = 'proportional'
  cbar_lblsz: class 'float', Label size for color bar tick labels. Default = 10.
  overlay_vec: class 'bool', Overlay vectors on map plots. If set to True, the following vector parameters 
                             will be active. See 
                             https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html and 
                             https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.quiverkey.html 
                             for more information on the vector parameters listed below. Default = False
  u, v: class 'xr.DataArray', xarray.DataArray of the u- and v-component of the vectors to plot if 
                              overlay_vec = True. Like 'var', must have dimensions: [# of cases x lat x lon].
                              Default = None, None
  vec_scale: class 'float', Scales the length of the arrow inversely. Number of data units per arrow lenth 
                            unit. A smaller scale parameter makes the arrow longer. Scale_units are 
                            permanently set to 'height' for this function. Fallback value only used if the
                            vec_pctl-based percentile below comes out non-positive or non-finite.
                            Default = 100.
  vec_pctl: class 'float', Percentile (0-100) of wind speed magnitude, computed within the plotted domain
                           (LatMin/LatMax, LonMin/LonMax) separately for each panel, used to set that
                           panel's quiver scale. Default = 95.
  vec_arrow_frac: class 'float', Fraction of the axes height that a wind vector at the vec_pctl percentile
                                 magnitude should span. Replaces the need to hand-tune vec_scale: raise this
                                 for longer arrows, lower it for shorter ones. Default = 0.1
  vec_key_yoffset: class 'float', Figure-fraction vertical offset, measured from each panel's own bottom
                                  edge (after the colorbar is placed), used to put the quiver reference key
                                  outside the map instead of overlapping it. Negative values place the key
                                  below the panel; make more negative for more clearance. Default = -0.05
  vec_wid: class 'float', Shaft width of vector. Default = 0.002
  vec_hal: class 'float', Head axis length of vector. Default = 4.
  vec_hdl: class 'float', Head length of vector. Default = 4.
  vec_hdw: class 'float', Head width of vector. Default = 4.
  vec_skip: class 'int', Number of grid cells to skip when plotting vectors. Higher numbers correspond to 
                         less congestion between plotted vector arrows. Default = 2
  vec_ref: class 'float', Reference vector to be used as the length of the vector key. Default = 5.        
  vec_units: class 'str', Units of the vector that will be displayed in vector key following 'vec_ref'.
                          Default = ''
  vec_name: class 'str', Manual text to be included in output file name containing information about vector. 
                         For example, vec_name = '850hPawinds' for u and v wind plot at 850 hPa.
                         Default = ''
  regbox: class 'bool', Include box around specified region on each subplot. If True, the following region 
                        parameters will be active. Default = False
  regcol: class 'str', Color of region box. Default = 'r' (red) 
  regline: class 'str', Line style of line marking region boundary. Default = '-'
  reglw: class 'float', Width of line marking region boundary. Default = 1.
  regslat, regnlat, regwlon, regelon: class'float', Southern/northern/western/eastern border of region box. 
                                                    Function finds grid cell midpoint closest to specified 
                                                    value and plots box around edge of grid cell.
                                                    Latitude values: - = °S, + = °N.
                                                    Longitude values: - = °W, + = °E.
                                                    Default = None, None, None, None 
  point: class 'bool', Include point at specified latitude and longtiude value on each subplot. If true, the 
                       following point parameters will be active. Default = False
  ptlat, ptlon: class 'float', Latitude and longitude points of plotted point. Function finds grid cell 
                               midpoint closest to specified value and plots marker at the grid cell 
                               midpoint. Latitude values: - = °S, + = °N. Longitude values: - = °W, + = °E.
                               Default = None, None
  shape_lats, shape_lons: class 'list', List of latitude and longitude values for plotting shapes on each 
                                        subplot. Shapes will be plot at exact latitude and longitude
                                        specified. Latitude values: - = °S, + = °N. 
                                        Longitude values: - = °W, + = °E. List should consist of floats, 
                                        for example: [30., 35., 40.]. Default = [], []
  shape_type: class 'list', Marker type for each shape. Find examples at 
                            https://matplotlib.org/stable/api/markers_api.html. List should consist of 
                            strings, for example: ['o', 's', 'p']. Default = []
  shape_size: :class:'list', Marker size for each shape. List should consist of floats, for example: 
                             [10., 5., 10.]. Default = []
  shape_col: class 'list', Marker color for each shape. List should consist of strings, for example: 
                           ['k', 'k', 'k']. Default = []
  Ind_plots: class 'bool', Include individual map plots of each case as separate PDF pages appended to output 
                           file. Individual plots will conform to all map parameters defined for panel plot.
                           Default = True
  extra_name: class 'str', Optional string to be included at the end of the file output name. This is a place 
                           to include any additional information in the file output name. Default = ''
  folderpath: class 'str', String of the path to the folder with which to deposite the output file produced 
                           by this function. The file name is generated automatically based on input 
                           parameters. Do not include first and last forward slashes, for example: 'pdfs' or 
                           'home/pdfs/untitledfolder'. Default = ''
  filesuf: class 'str', Type of output file specified as a string. Default = '.pdf' 
  _______________________________________________________________________________________________________

  Returns
  ---------------------
  output: PDF file 
          Panel (+individuals) plot of the variable input(s) saved to a specified folder/file path  

  '''

  #-------------------------------------------------------------------------
  # Make variables to plot cyclic
  #-------------------------------------------------------------------------
  
  varc = gv.xr_add_cyclic_longitudes(var, "lon")
  if overlay_vec == True:
   uc = gv.xr_add_cyclic_longitudes(u, "lon")
   vc = gv.xr_add_cyclic_longitudes(v, "lon")

  #------------------------------
  # Set base figure parameters
  #------------------------------

  # Data transform: must match the longitude convention of the data (0-360 vs -180-180)
  # CESM data uses 0-360, so the transform central_longitude must match the projection
  
  # Ceiling of half the number of cases, used for looping through axes
  rowceil = math.ceil(len(cases)/2)
  rowceil_min1 = math.ceil(len(cases)/2-1)

  # Determine if number of cases is even or odd, this determines plot dimensions
  if (len(cases) % 2) == 0: 
   numcases = 'even'
  elif (len(cases) % 2) == 1:
   numcases = 'odd'

  # Set contour level values if not specified by user
  if loval == None:
   loval = np.nanmin(var)
  if hival == None:
   hival = np.nanmax(var)
  if spval == None:
   spval = (np.nanmax(var)-np.nanmin(var))/10
  if tkstd == None:
   tkstd = (np.nanmax(var)-np.nanmin(var))/5

  # Setting file output name parameters
  if overlay_vec == False:
   vec_name = ''
  else: 
   vec_name = ''.join(('_',vec_name))

  # Setting vector grid cell skipping parameters
  skip1D = (slice(None, None, vec_skip)) 
  skip2D = (slice(None, None, vec_skip), slice(None, None, vec_skip))

  #-----------------------------------------------------------------------
  # Prepare lon/data arrays for plotting
  # CESM uses 0-360 lons; ccrs.PlateCarree() only renders -180 to 180.
  # Strip the cyclic point, roll 180deg so prime meridian is at edges,
  # convert remaining >180 values to negative, re-add cyclic at 180.
  # After this, lon_plot runs -180 to 180 and transform=PlateCarree works.
  #-----------------------------------------------------------------------

  lon_cyc = varc.lon.values            # 0 ... 357.5 ... 360 (145 pts with cyclic)
  lon_raw = lon_cyc[:-1]               # 0 ... 357.5          (144 pts, no cyclic)
  nroll   = len(lon_raw) // 2          # 72 (shift by 180 deg)
  lon_rolled = np.roll(lon_raw, -nroll)                            # 180 ... 357.5, 0 ... 177.5
  lon_shifted = np.where(lon_rolled > 180., lon_rolled - 360., lon_rolled)  # -180 ... 177.5
  lon_plot = np.append(lon_shifted, 180.)                          # -180 ... 177.5, 180

  def prep_data(arr2d):
   '''Roll a (lat, 145-lon) array to match lon_plot (-180 to 180).'''
   d = arr2d[:, :-1]                                    # strip cyclic → (lat, 144)
   d_rolled = np.roll(d, -nroll, axis=1)               # roll
   return np.concatenate([d_rolled, d_rolled[:, :1]], axis=1)  # re-add cyclic → (lat, 145)

  lon2d, lat2d = np.meshgrid(lon_plot, varc.lat.values)
  lon1d_skip   = lon_plot[skip1D]

  #-----------------------------------------------------------------------
  # Per-panel wind vector scaling
  #-----------------------------------------------------------------------
  # Quiver uses scale_units='height', so arrow length = magnitude/scale as a
  # fraction of the axes height. Deriving `scale` from the vec_pctl percentile
  # of wind speed *within the plotted domain* (LatMin/LatMax, LonMin/LonMax)
  # means each panel's arrows are sized relative to its own typical wind
  # speed, rather than one fixed vec_scale shared identically across panels
  # that may have very different wind magnitudes.

  lat_mask = (varc.lat.values >= LatMin) & (varc.lat.values <= LatMax)
  lon_mask = (lon_plot >= LonMin) & (lon_plot <= LonMax)

  def panel_vec_scale(u2d, v2d):
   spd = np.sqrt(u2d[lat_mask][:, lon_mask]**2 + v2d[lat_mask][:, lon_mask]**2)
   p = np.nanpercentile(spd, vec_pctl)
   if not np.isfinite(p) or p <= 0.:
    return vec_scale
   return p / vec_arrow_frac

  #----------------
  # Define figures
  #----------------

  print('Working on panel plot...')
 
  # Define fig and axes
  if numcases == 'even': # symmetrical plot
   fig, axes = plt.subplots(nrows=rowceil,ncols=2,figsize=(figw,figh),dpi=fdpi,subplot_kw={'projection':proj})
   fig.subplots_adjust(hspace=hspace,wspace=wspace)

  if numcases == 'odd': # use gridspec to place last axis in the middle
   fig = plt.figure(figsize=(figw,figh),dpi=fdpi)
   gs = fig.add_gridspec(nrows=100,ncols=100,hspace=hspace,wspace=wspace)  
   axes = []                   
   for r in range(rowceil_min1):
    for c in range(2):
     if c == 0:
      ax = fig.add_subplot(gs[r*int(100/rowceil):r*int(100/rowceil)+int(100/rowceil),0:48],projection=proj)
      axes.append(ax)
     if c == 1:
      ax = fig.add_subplot(gs[r*int(100/rowceil):r*int(100/rowceil)+int(100/rowceil),51:99],projection=proj)
      axes.append(ax)
   lastax = fig.add_subplot(gs[rowceil_min1*int(100/rowceil):-1,25:75],projection=proj)
   axes.append(lastax)
 
  # Reshape axes for plotting
  if numcases == 'even':  
   axes = axes.reshape(rowceil,2)

  #----------------------------------
  # Subplot map components
  #----------------------------------

  if numcases == 'even':
   for r in range(rowceil):
    for c in range(2):
     axes[r,c].set_title(fig_let[2*r+c]+' '+str(seas)+' '+str(var_name)+str(vec_name)+' '+cases[2*r+c],loc=ttlloc,
                                                                                        fontsize=ttlfts,pad=ttlpad) 
     axes[r,c].set_extent([LonMin,LonMax,LatMin,LatMax],ccrs.PlateCarree())                                    
     if coast == True:
      axes[r,c].add_feature(cfeature.COASTLINE,linewidths=coastlw)
     if lake == True:
      axes[r,c].add_feature(cfeature.LAKES,linewidths=lakelw,facecolor='none',edgecolor='k')
     if border == True:
      axes[r,c].add_feature(cfeature.BORDERS,linewidths=borderlw)
     if usstate == True:
      axes[r,c].add_feature(cfeature.STATES,linewidths=usstatelw)
 
  if numcases == 'odd':
   for i in range(len(cases)):
    axes[i].set_title(fig_let[i]+' '+str(seas)+' '+str(var_name)+str(vec_name)+' '+cases[i],loc=ttlloc,fontsize=ttlfts,
                                                                                                            pad=ttlpad) 
    axes[i].set_extent([LonMin,LonMax,LatMin,LatMax],ccrs.PlateCarree())                            
    # Figure map
    if coast == True:
     axes[i].add_feature(cfeature.COASTLINE,linewidths=coastlw)
    if lake == True:
     axes[i].add_feature(cfeature.LAKES,linewidths=lakelw,facecolor='none',edgecolor='k')
    if border == True:
     axes[i].add_feature(cfeature.BORDERS,linewidths=borderlw)
    if usstate == True:
     axes[i].add_feature(cfeature.STATES,linewidths=usstatelw) 

  #----------------------------------
  # Add map axes and ticks  
  #----------------------------------

  if add_axes == True:

   ### rows 1 to N-1
   if numcases == 'even':
    for r in range(rowceil_min1):
     for c in range(2):
      if c == 0:
       map_ticks_and_labels(ax=axes[r,c],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=False,left=True,right=False)
      if c == 1:
       map_ticks_and_labels(ax=axes[r,c],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=False,left=False,right=True)

   if numcases == 'odd':
    for i in range(len(cases)-1):
     if (i % 2) == 0: # all even indices are in left column
      map_ticks_and_labels(ax=axes[i],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                           xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                           glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                           top=False,bot=False,left=True,right=False)
     if (i % 2) == 1: # all odd indices are in left column
      map_ticks_and_labels(ax=axes[i],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                           xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                           glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                           top=False,bot=False,left=False,right=True)

   ### row N
   if numcases == 'even':
    for r in range(rowceil_min1,rowceil):
     for c in range(2):
      if c == 0:  # Left column
       map_ticks_and_labels(ax=axes[r,c],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=True,left=True,right=False)
      if c == 1:  # Right column
       map_ticks_and_labels(ax=axes[r,c],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=True,left=False,right=True)

   if numcases == 'odd':
    i = len(cases)-1
    map_ticks_and_labels(ax=axes[i],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                         xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                         glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                         top=False,bot=True,left=True,right=True)    

  #----------------------------------
  # Plot the variables 
  #----------------------------------

  vec_dict = {}  # Quiver handles, placed once the final layout (incl. colorbar) settles

  if numcases == 'even':
   for r in range(rowceil):
    for c in range(2):
      if cntr_type == 'AreaFill':
       cntr = axes[r,c].pcolormesh(lon2d,lat2d,prep_data(varc[2*r+c,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                                   norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
      elif cntr_type == 'RasterFill':
       cntr = axes[r,c].pcolormesh(lon2d,lat2d,prep_data(varc[2*r+c,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                                   norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
      if overlay_vec == True:
       u2d = prep_data(uc[2*r+c,:,:].values)
       v2d = prep_data(vc[2*r+c,:,:].values)
       scale_i = panel_vec_scale(u2d, v2d)
       vec = axes[r,c].quiver(lon1d_skip,uc.lat[skip1D],u2d[skip2D],v2d[skip2D],
                              transform=ccrs.PlateCarree(),scale_units='height',pivot='mid',
                              scale=scale_i,width=vec_wid,headlength=vec_hdl,headwidth=vec_hdw,headaxislength=vec_hal)
       vec_dict[(r,c)] = vec

  if numcases == 'odd':
   for i in range(len(cases)):
     if cntr_type == 'AreaFill':
      cntr = axes[i].pcolormesh(lon2d,lat2d,prep_data(varc[i,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                                norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
     elif cntr_type == 'RasterFill':
      cntr = axes[i].pcolormesh(lon2d,lat2d,prep_data(varc[i,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                                norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
     if overlay_vec == True:
      u2d = prep_data(uc[i,:,:].values)
      v2d = prep_data(vc[i,:,:].values)
      scale_i = panel_vec_scale(u2d, v2d)
      vec = axes[i].quiver(lon1d_skip,uc.lat[skip1D],u2d[skip2D],v2d[skip2D],
                           transform=ccrs.PlateCarree(),scale_units='height',pivot='mid',
                           scale=scale_i,width=vec_wid,headlength=vec_hdl,headwidth=vec_hdw,headaxislength=vec_hal)
      vec_dict[i] = vec

  #-------------------------------
  # Color bar for plots 
  #-------------------------------
  
  cbar = fig.colorbar(cntr,ax=axes,orientation=cbar_orient,ticks=MultipleLocator(tkstd),shrink=cbar_shrk,pad=cbar_pad,label=units,
                                   spacing=cbar_sp,extend=extnd)
  cbar.ax.tick_params(labelsize=cbar_lblsz)

  #-------------------------------------------------------------------------
  # Add the quiver reference key now, after the colorbar has carved out its
  # space. We measure each panel's actual final box (figure-fraction
  # coordinates, via get_position()) and place the key just below its
  # bottom edge — outside the map rectangle by construction, rather than
  # guessing a fraction that might land inside it.
  #-------------------------------------------------------------------------

  if overlay_vec == True:
   fig.canvas.draw()
   if numcases == 'even':
    for r in range(rowceil):
     for c in range(2):
      vec = vec_dict[(r,c)]
      pos = axes[r,c].get_position()
      qx  = pos.x0 + 0.9*(pos.x1 - pos.x0)
      qy  = pos.y0 + vec_key_yoffset
      qkey = axes[r,c].quiverkey(vec,qx,qy,vec_ref,str(vec_ref)+str(vec_units),labelpos='N',coordinates='figure',color='k')
   if numcases == 'odd':
    for i in range(len(cases)):
     vec = vec_dict[i]
     pos = axes[i].get_position()
     qx  = pos.x0 + 0.9*(pos.x1 - pos.x0)
     qy  = pos.y0 + vec_key_yoffset
     qkey = axes[i].quiverkey(vec,qx,qy,vec_ref,str(int(vec_ref))+str(vec_units),labelpos='N',coordinates='figure',color='k')

  #------------------------------
  # Add region and point to map
  #------------------------------
 
  if regbox == True or point == True:
 
   # Adjusters to put box around entire grid cell
   latadj = abs(float((var.lat[1] - var.lat[2]) / 2))
   lonadj = abs(float((var.lon[1] - var.lon[2]) / 2))

  if regbox == True: 

   # Handle values if °W = 180-360
   if regwlon < 0.:
    regwlon = regwlon + 360
   if regelon < 0.:
    regelon = regelon + 360

   # Pick best values for region
   slat = float(var.lat.sel(lat=regslat, method='nearest'))
   nlat = float(var.lat.sel(lat=regnlat, method='nearest'))
   wlon = float(var.lon.sel(lon=regwlon, method='nearest'))
   elon = float(var.lon.sel(lon=regelon, method='nearest'))

   # Handle values if °W = 180-360
   if wlon > 180.0:
    wlon = wlon - 360
   if elon > 180.0:
    elon = elon - 360
   
   if numcases == 'even': 
    for r in range(rowceil):
     for c in range(2):
      draw_region_box(ax=axes[r,c],slat=slat-latadj,nlat=nlat+latadj,wlon=wlon-lonadj,elon=elon+lonadj,
                      linestyle=regline,facecolor='none',edgecolor=regcol,linewidth=reglw,zorder=10)

   if numcases == 'odd':
    for i in range(len(cases)):
      draw_region_box(ax=axes[i],slat=slat-latadj,nlat=nlat+latadj,wlon=wlon-lonadj,elon=elon+lonadj,
                      linestyle=regline,facecolor='none',edgecolor=regcol,linewidth=reglw,zorder=10)

  if point == True:
 
   # Pick best values for point
   latpt = float(var.lat.sel(lat=ptlat, method='nearest'))
   lonpt = float(var.lon.sel(lon=ptlon, method='nearest')) 

   # Handle values if °W = 180-360
   if lonpt > 180.0:
    lonpt = lonpt - 360

   if numcases == 'even':
    for r in range(rowceil):
     for c in range(2):
      axes[r,c].plot(lonpt,latpt,'ro',markersize=5)
   if numcases == 'odd':
    for i in range(len(cases)):
     axes[i].plot(lonpt,latpt,'ro',markersize=5)

  #------------------------
  # Add shapes to map  
  #------------------------
 
  if numcases == 'even':
   for r in range(rowceil):
    for c in range(2):
     for s in range(len(shape_type)):
      axes[r,c].plot(shape_lons[s],shape_lats[s],marker=shape_type[s],markersize=shape_size[s],markerfacecolor='none',
                      markeredgecolor=shape_col)

  if numcases == 'odd':
   for i in range(len(cases)):
    for s in range(len(shape_type)):
     axes[i].plot(shape_lons[s],shape_lats[s],marker=shape_type[s],markersize=shape_size[s],markerfacecolor='none',
                  markeredgecolor=shape_col[s])

  #-----------------------------------------------------------
  # Plot individual maps and append to pdf file if necessary
  #-----------------------------------------------------------

  if Ind_plots == True:

   print('Working on individual plots...')

   for i in range(len(cases)):

    figi = plt.figure(figsize=(figw,figh),dpi=fdpi)
    axi  = figi.add_subplot(111, projection=proj) 
    axi.set_title(fig_let[i]+' '+str(seas)+' '+str(var_name)+str(vec_name)+' '+cases[i],loc=ttlloc,fontsize=ttlfts,
                                                                                                   pad=ttlpad)  # title
    axi.set_extent([LonMin,LonMax,LatMin,LatMax],ccrs.PlateCarree())                                                          # map extent
    if coast == True:
     axi.add_feature(cfeature.COASTLINE,linewidths=coastlw)
    if lake == True:
     axi.add_feature(cfeature.LAKES,linewidths=lakelw,facecolor='none',edgecolor='k')
    if border == True:
     axi.add_feature(cfeature.BORDERS,linewidths=borderlw)
    if usstate == True:
     axi.add_feature(cfeature.STATES,linewidths=usstatelw)
    map_ticks_and_labels(ax=axi,LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                         xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                         glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                         top=False,bot=True,left=True,right=True)
    if cntr_type == 'AreaFill':
     cntr = axi.pcolormesh(lon2d,lat2d,prep_data(varc[i,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                           norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
    elif cntr_type == 'RasterFill':
     cntr = axi.pcolormesh(lon2d,lat2d,prep_data(varc[i,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                           norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
    cbar_i = plt.colorbar(cntr,ax=axi,orientation=cbar_orient,ticks=MultipleLocator(tkstd),
                          shrink=cbar_shrk,pad=cbar_pad,label=units,spacing=cbar_sp,extend=extnd)
    cbar_i.ax.tick_params(labelsize=cbar_lblsz)
    if overlay_vec == True:
     u2d = prep_data(uc[i,:,:].values)
     v2d = prep_data(vc[i,:,:].values)
     scale_i = panel_vec_scale(u2d, v2d)
     vec = axi.quiver(lon1d_skip,uc.lat[skip1D],u2d[skip2D],v2d[skip2D],
                      transform=ccrs.PlateCarree(),scale_units='height',pivot='mid',scale=scale_i,
                      width=vec_wid,headlength=vec_hdl,headwidth=vec_hdw,headaxislength=vec_hal)
     figi.canvas.draw()  # finalize the post-colorbar box before placing the key
     pos = axi.get_position()
     qx  = pos.x0 + 0.9*(pos.x1 - pos.x0)
     qy  = pos.y0 + vec_key_yoffset
     qkey = axi.quiverkey(vec,qx,qy,vec_ref,str(int(vec_ref))+str(vec_units),labelpos='N',coordinates='figure',color='k')
    if regbox == True:
     draw_region_box(ax=axi,slat=slat-latadj,nlat=nlat+latadj,wlon=wlon-lonadj,elon=elon+lonadj,
                      linestyle=regline,facecolor='none',edgecolor=regcol,linewidth=reglw,zorder=10)
    if point == True:
     axi.plot(lonpt,latpt,'ro',markersize=5)
    for s in range(len(shape_type)):
     axi.plot(shape_lons[s],shape_lats[s],marker=shape_type[s],markersize=shape_size[s],markerfacecolor='none',
                      markeredgecolor=shape_col[s])

  #--------------------------
  # Save output PDF file
  #--------------------------

  save_multi_image('./'+str(folderpath)+'/'+str(seas)+'_'+str(var_name)+str(vec_name)+'_'+str(extra_name)+str(filesuf))
  plt.close('all')

#######################################################################################################
# Plot difference contours in panel and individual map plots 
#######################################################################################################

def plot_diff_contour_map_avg(
                              ### Required Parameters
                              var: xr.DataArray,
                            
                              ### Optional Parameters
                              cases: list = [''], var_name: str = '', seas: str = '', units: str = '',
                              figw: float = 10., figh: float = 10., fdpi: float = 300.,
                              hspace: float = None, wspace: float = None, fig_let: list = fig_let,
                              ttlloc: str = 'left', ttlfts: float = 12., ttlpad: float = 10.,
                              LatMin: float = -90., LatMax: float = 90., LonMin: float = -180.,
                              LonMax: float = 180., proj: ccrs.Projection = ccrs.PlateCarree(),
                              coast: bool = True, coastlw: float = 0.75, lake: bool = False,
                              lakelw: float = 0.5, border: bool = True, borderlw: float = 0.75,
                              usstate: bool = False, usstatelw: float = 0.5, add_axes: bool = True,
                              latlblsp: float = 30., lonlblsp: float = 60., 
                              lattksp: int = 7, lontksp: int = 7, tklblsz: float = 10.,
                              tkmajlg: float = 4., tkminlg: float = 2., xmin_mj: int = 2, ymin_mj: int = 2,
                              xpads: float = 15., ypads: float = 15.,
                              glalpha: float = 0.0, glcolor: str = 'gray',
                              cntr_type: str = 'AreaFill', colort: colors.ListedColormap = cmaps.ncl_default,
                              loval: float = None, hival: float = None, spval: float = None,
                              tkstd: float = None, extnd: str = 'neither',
                              cbar_orient: str = 'horizontal', cbar_pad: float = 0.08,
                              cbar_shrk: float = 0.6, cbar_sp: str = 'proportional', cbar_lblsz: float = 10.,
                              overlay_vec: bool = False, u: xr.DataArray = None, v: xr.DataArray = None,
                              vec_scale: float = 100., vec_wid: float = 0.002, vec_hal: float = 4.,
                              vec_hdl: float = 4., vec_hdw: float = 4., vec_skip: int = 2,
                              vec_ref: float = 5., vec_units: str = '', vec_name: str = '',
                              regbox: bool = False, regcol: str = 'r', regline: str = '-',
                              reglw: float = 1., regslat: float = None, regnlat: float = None,
                              regwlon: float = None, regelon: float = None,
                              point: bool = False, ptlat: float = None, ptlon: float = None,
                              shape_lats: list = [], shape_lons: list = [], shape_type: list = [],
                              shape_size: list = [], shape_col: list = [], Ind_plots: bool = True,
                              extra_name: str = '', folderpath: str = '', filesuf: str = '.pdf'
                              ):

  '''Reads in an xr.DataArray of 3+ cases of a global variable and produces a panel difference plot and 
  optional individual difference plots of each case in subsequent PDF pages.  

  Active issues with this script that need to be fixed:
  #1. Projection can't be changed from ccrs.PlateCarree() unless changing it in the function.
  #2. Default color table becomes re-registered if trying to specify the default table when calling
      the function. Ex. Cannot call cmaps.MPL_viridis when calling colort in function.  
  #3. hspace and wspace don't work when there are an odd number of plots in panel plot.

  Required Parameters                       
  --------------------------------------------------------------------------------------------------------
  var
   class 'xarray.DataArray', The variable containing the values to be plot as contours on a map. Must 
                             contain the following dimensions: [# of cases x lat x lon]. # of cases needs 
                             to be two (2) or greater for this function. 

  Optional Parameters                       
  --------------------------------------------------------------------------------------------------------
  cases: class 'list', List of strings containing the name of case(s) that will be plotted. These strings 
                       will be displayed in the title of each map plot. Default = ['']
  var_name: class 'string', Name of the variable that will be plotted. This string will appear in the 
                            title of each map plot and in the file output name. Default = ''
  seas: class 'string', Name of season for which variable is averaged over. This string will be displayed 
                        in the title of each map plot and in the file output name. Default = ''
  units: class 'string', Specified units of variable. This string will be displayed underneath the 
                         colorbar. Default = ''
  figw, figh, fdpi: class 'float', Width (inches), height (inches), and DPI (dots per inch) of figure. 
                                   Default = 10., 10., 300.
  hspace, wspace: class 'float', Height and width of padding between subplots as a fraction of the average 
                                 Axes height/width, used in plt.subplots_adjust. If number of cases is an 
                                 odd number, this parameter is disabled and users should use figw and figh.
  fig_let: class 'list', List of letters to denote subplots. Spans a-z, but can be modified by specifying a 
                         new list. Default = ['a)','b)','c)', ... ,'z)']
  ttlloc: class 'string', Location of title above each subplot. Default = 'left'
  ttlfts: class 'float', Font size for title above each subplot. Default = 12.
  ttlpad: class 'float', Padding for title above each subplot. Default = 10.
  LatMin, LatMax, LonMin, LonMax: class 'float', Southern/northern latitude and western/eastern longitude
                                                 that sets extent of map to be plot. Values: 
                                                 LAT: - = °S, + = °N, range = -90 to 90
                                                 LON: - = °W, + = °N, range = -180 to 180
                                                 Default = -90., 90., -180., 180.
  proj: class 'cartopy.crs.Projection', Projection of map for each subplot. This parameter must be 
                                        cartopy.crs.PlateCarree() currently as cartopy's gridlines do not 
                                        support any other projection at this time. 
                                        Default = ccrs.PlateCarree()
  coast, coastlw: class 'bool','string', include coastlines on base map and if True, width of lines
                                         Default = True, 0.75
  lake, lakelw: class 'bool','string', include lakes on base map and if True, width of lines
                                       Default = False, 0.5  
  border, borderlw: class 'bool','string', include country borders on base map and if True, width of 
                                           lines. Default = True, 0.75
  usstate, usstatelw: class 'bool','float', include US state boundaries on base map and if True 
                                            width of lines. Default = False, 0.5
  add_axes: class 'bool', Add axes ticks and labels to each map. If True, the following tick and label
                          parameters are active. Default = True
  latlblsp, lonlblsp: class 'float', Spacing of latitude tick labels in degrees of latitude and 
                                     longitude. Default = 30., 60.
  lattksp, lontksp: class 'int', Tick spacing for major latitude and longitude ticks. Examples:
                                 lattksp = 7 -> -90 to 90 by 30 (7 total major ticks)
                                 lontksp = 7 -> -180 to 180 by 60 (7 total major ticks)
                                 Default = 7, 7
  tklblsz: class 'float', Font size of tick labels. Default = 10.
  tkmajlg: class 'float', Size of major ticks around the outline of each map. Default = 4.
  tkminlg: class 'float', Size of minor ticks around the outline of each map. Default = 2.
  xmin_mj: class 'int', Number of minor ticks in between each major tick on the x-axis (longitude).
                        Default = 2
  ymin_mj: class 'int', Number of minor ticks in between each major tick on the y-axis (latitude). 
                        Default = 2
  xpads, ypads: class 'float', Padding of x-axis longitude and y-axis latitude tick labels from 
                               map outline. Default = 15., 15.
  glalpha: class 'float', Alpha (line opacity) for gridlines between lat/lon ticks. Default is no 
                          gridlines. Modify 1.0 >= alpha > 0.0 for visible gridlines.
                          Default = 0.0 (no gridlines)
  glcolor: class 'str', Color of gridlines if glalpha > 0.0. Default = 'gray'
  cntr_type: class 'str', Type of contour for plotting. Options: 'AreaFill' - interpolated, 
                          'RasterFill' - raster. Default = 'AreaFill'
  colort: class 'colors.ListedColormap', Color table used for plotting contours. Specify names from cmaps 
                                         (https://github.com/hhuangwx/cmaps) or Matplotlib 
                                         (https://matplotlib.org/stable/tutorials/colors/colormaps.html)
                                         Default = cmaps.MPL_viridis
  loval: class 'float', Minimum value in contour levels. If not specified, will default to lowest value 
                        found in variable. 
  hival: class 'float', Maximum value in contour levels. If not specified, will default to highest value 
                        found in variable. 
  spval: class 'float', Stride (spacing value) in contour levels. If not specified, will default to 
                        (hival-loval)/10. 
  tkstd: class 'float', Stride of tick labels for color bar. If not specified, will default to spval. 
  extnd: :class:'str', Option to add triangles on either side of color bar that signify extended value 
                       range. Options: 'neither','max','min','both'. Default = 'both'
  cbar_orient: class 'str', Orientation of color bar. Options: 'horizontal','vertical'
                            Default = 'horizontal'
  cbar_pad: class 'float', Padding of color bar from bottom of map. Default = 0.08
  cbar_shrk: class 'float', Color bar shrink parameter. Modifies the sizing of the color bar. 
                            Default = 0.6
  cbar_sp: class 'str', Spacing of colors in color bar, If 'extnd' is not 'neither', this parameters
                        must be 'proportional'. Default = 'proportional'
  cbar_lblsz: class 'float', Label size for color bar tick labels. Default = 10.
  overlay_vec: class 'bool', Overlay vectors on map plots. If set to True, the following vector parameters 
                             will be active. See 
                             https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html and 
                             https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.quiverkey.html 
                             for more information on the vector parameters listed below. Default = False
  u, v: class 'xr.DataArray', xarray.DataArray of the u- and v-component of the vectors to plot if 
                              overlay_vec = True. Like 'var', must have dimensions: [# of cases x lat x lon].
                              Default = None, None
  vec_scale: class 'float', Scales the length of the arrow inversely. Number of data units per arrow lenth 
                            unit. A smaller scale parameter makes the arrow longer. Scale_units are 
                            permanently set to 'height' for this function. Default = 100.
  vec_wid: class 'float', Shaft width of vector. Default = 0.002
  vec_hal: class 'float', Head axis length of vector. Default = 4.
  vec_hdl: class 'float', Head length of vector. Default = 4.
  vec_hdw: class 'float', Head width of vector. Default = 4.
  vec_skip: class 'int', Number of grid cells to skip when plotting vectors. Higher numbers correspond to 
                         less congestion between plotted vector arrows. Default = 2
  vec_ref: class 'float', Reference vector to be used as the length of the vector key. Default = 5.        
  vec_units: class 'str', Units of the vector that will be displayed in vector key following 'vec_ref'.
                          Default = ''
  vec_name: class 'str', Manual text to be included in output file name containing information about vector. 
                         For example, vec_name = '850hPawinds' for u and v wind plot at 850 hPa.
                         Default = ''
  regbox: class 'bool', Include box around specified region on each subplot. If True, the following region 
                        parameters will be active. Default = False
  regcol: class 'str', Color of region box. Default = 'r' (red) 
  regline: class 'str', Line style of line marking region boundary. Default = '-'
  reglw: class 'float', Width of line marking region boundary. Default = 1.
  regslat, regnlat, regwlon, regelon: class'float', Southern/northern/western/eastern border of region box. 
                                                    Function finds grid cell midpoint closest to specified 
                                                    value and plots box around edge of grid cell.
                                                    Latitude values: - = °S, + = °N.
                                                    Longitude values: - = °W, + = °E.
                                                    Default = None, None, None, None 
  point: class 'bool', Include point at specified latitude and longtiude value on each subplot. If true, the 
                       following point parameters will be active. Default = False
  ptlat, ptlon: class 'float', Latitude and longitude points of plotted point. Function finds grid cell 
                               midpoint closest to specified value and plots marker at the grid cell 
                               midpoint. Latitude values: - = °S, + = °N. Longitude values: - = °W, + = °E.
                               Default = None, None
  shape_lats, shape_lons: class 'list', List of latitude and longitude values for plotting shapes on each 
                                        subplot. Shapes will be plot at exact latitude and longitude
                                        specified. Latitude values: - = °S, + = °N. 
                                        Longitude values: - = °W, + = °E. List should consist of floats, 
                                        for example: [30., 35., 40.]. Default = [], []
  shape_type: class 'list', Marker type for each shape. Find examples at 
                            https://matplotlib.org/stable/api/markers_api.html. List should consist of 
                            strings, for example: ['o', 's', 'p']. Default = []
  shape_size: :class:'list', Marker size for each shape. List should consist of floats, for example: 
                             [10., 5., 10.]. Default = []
  shape_col: class 'list', Marker color for each shape. List should consist of strings, for example: 
                           ['k', 'k', 'k']. Default = []
  Ind_plots: class 'bool', Include individual map plots of each case as separate PDF pages appended to output 
                           file. Individual plots will conform to all map parameters defined for panel plot.
                           Default = True
  extra_name: class 'str', Optional string to be included at the end of the file output name. This is a place 
                           to include any additional information in the file output name. Default = ''
  folderpath: class 'str', String of the path to the folder with which to deposite the output file produced 
                           by this function. The file name is generated automatically based on input 
                           parameters. Do not include first and last forward slashes, for example: 'pdfs' or 
                           'home/pdfs/untitledfolder'. Default = ''
  filesuf: class 'str', Type of output file specified as a string. Default = '.pdf' 
  _______________________________________________________________________________________________________

  Returns
  ---------------------
  output: PDF file 
          Panel (+individuals) plot of the variable input(s) saved to a specified folder/file path  

  '''

  #-------------------------------------------------------------------------
  # Make variables to plot cyclic
  #-------------------------------------------------------------------------

  varc = gv.xr_add_cyclic_longitudes(var, "lon")
  if overlay_vec == True:
   uc = gv.xr_add_cyclic_longitudes(u, "lon")
   vc = gv.xr_add_cyclic_longitudes(v, "lon")

  #-------------------------------------------------------------------------
  # Make difference variables for plotting
  #-------------------------------------------------------------------------

  cases_diff = [None]*(len(cases)-1)
  for x in range(1,len(cases)):
   cases_diff[x-1] = str(cases[x])+'-'+str(cases[0])

  diff = xr.DataArray(None,dims=['casediff','lat','lon'],coords=dict(casediff=cases_diff,lat=varc.lat,lon=varc.lon)).astype(float)
  for x in range(1,len(cases)):
   diff[x-1,:,:] = varc[x,:,:] - varc[0,:,:] 

  if overlay_vec == True:
   udiff = xr.DataArray(None,dims=['casediff','lat','lon'],coords=dict(casediff=cases_diff,lat=uc.lat,lon=uc.lon)).astype(float)
   vdiff = xr.DataArray(None,dims=['casediff','lat','lon'],coords=dict(casediff=cases_diff,lat=vc.lat,lon=vc.lon)).astype(float)
   for x in range(1,len(cases)):
    udiff[x-1,:,:] = uc[x,:,:] - uc[0,:,:]
    vdiff[x-1,:,:] = vc[x,:,:] - vc[0,:,:]



  #------------------------------
  # Set base figure parameters
  #------------------------------

  # Ceiling of half the number of cases, used for looping through axes
  rowceil = math.ceil((len(cases)-1)/2)
  rowceil_min1 = math.ceil((len(cases)-1)/2-1)

  # Determine if number of cases is even or odd, this determines plot dimensions
  if ((len(cases)-1) % 2) == 0:
   numcases = 'even'
  elif ((len(cases)-1) % 2) == 1:
   numcases = 'odd'

  # Set contour level values if not specified by user
  if loval == None:
   loval = np.nanmin(diff)
  if hival == None:
   hival = -1.*loval 
  if spval == None:
   spval = (hival-loval)/10
  if tkstd == None:
   tkstd = (hival-loval)/5

  # Setting file output name parameters
  if overlay_vec == False:
   vec_name = ''
  else:
   vec_name = ''.join(('_',vec_name))

  # Setting vector grid cell skipping parameters
  skip1D = (slice(None, None, vec_skip))
  skip2D = (slice(None, None, vec_skip), slice(None, None, vec_skip))

  #-----------------------------------------------------------------------
  # Prepare coordinates and data for Pacific-centered plotting.
  # CESM lons run 0-357.5; ccrs.PlateCarree() only handles -180 to 180.
  # Roll by half the array so 180deg becomes the seam, then convert
  # remaining lons > 180 to negative. Re-add cyclic point at 180.
  #-----------------------------------------------------------------------

  lon_raw  = diff.lon.values[:-1]                                           # strip cyclic: 0...357.5 (144 pts)
  nroll    = len(lon_raw) // 2                                              # 72
  lon_roll = np.roll(lon_raw, -nroll)                                       # 180...357.5, 0...177.5
  lon_shift= np.where(lon_roll > 180., lon_roll - 360., lon_roll)          # -180...-2.5, 0...177.5
  lon_plot = np.append(lon_shift, 180.)                                     # add cyclic at 180: 145 pts

  def prep_data(arr2d):
   '''Convert a (lat, 145-lon) array from 0-360 to -180-180 lon ordering.'''
   d = arr2d[:, :-1]                                                        # strip cyclic -> (lat, 144)
   d = np.roll(d, -nroll, axis=1)                                           # roll
   return np.concatenate([d, d[:, :1]], axis=1)                             # re-add cyclic -> (lat, 145)

  lon2d, lat2d = np.meshgrid(lon_plot, diff.lat.values)
  lon1d_skip   = lon_plot[skip1D]                                           # for quiver x-positions

  #----------------
  # Define figures
  #----------------

  print('Working on panel difference plot...')

  # Define fig and axes
  if numcases == 'even': # symmetrical plot
   fig, axes = plt.subplots(nrows=rowceil,ncols=2,figsize=(figw,figh),dpi=fdpi,subplot_kw={'projection':proj})
   fig.subplots_adjust(hspace=hspace,wspace=wspace)

  if numcases == 'odd': # use gridspec to place last axis in the middle
   fig = plt.figure(figsize=(figw,figh),dpi=fdpi)
   gs = fig.add_gridspec(nrows=100,ncols=100,hspace=hspace,wspace=wspace)
   axes = []
   for r in range(rowceil_min1):
    for c in range(2):
     if c == 0:
      ax = fig.add_subplot(gs[r*int(100/rowceil):r*int(100/rowceil)+int(100/rowceil),0:48],projection=proj)
      axes.append(ax)
     if c == 1:
      ax = fig.add_subplot(gs[r*int(100/rowceil):r*int(100/rowceil)+int(100/rowceil),51:99],projection=proj)
      axes.append(ax)
   lastax = fig.add_subplot(gs[rowceil_min1*int(100/rowceil):-1,25:75],projection=proj)
   axes.append(lastax)

  # Reshape axes for plotting
  if numcases == 'even':
   axes = axes.reshape(rowceil,2)

  #----------------------------------
  # Subplot map components
  #----------------------------------

  if numcases == 'even':
   for r in range(rowceil):
    for c in range(2):
     axes[r,c].set_title(fig_let[2*r+c]+' '+str(seas)+' '+str(var_name)+str(vec_name)+' '+cases_diff[2*r+c],loc=ttlloc,
                                                                                            fontsize=ttlfts,pad=ttlpad)
     axes[r,c].set_extent([LonMin,LonMax,LatMin,LatMax],ccrs.PlateCarree())
     if coast == True:
      axes[r,c].add_feature(cfeature.COASTLINE,linewidths=coastlw)
     if lake == True:
      axes[r,c].add_feature(cfeature.LAKES,linewidths=lakelw,facecolor='none',edgecolor='k')
     if border == True:
      axes[r,c].add_feature(cfeature.BORDERS,linewidths=borderlw)
     if usstate == True:
      axes[r,c].add_feature(cfeature.STATES,linewidths=usstatelw)

  if numcases == 'odd':
   for i in range(len(cases)-1):
    axes[i].set_title(fig_let[i]+' '+str(seas)+' '+str(var_name)+str(vec_name)+' '+cases_diff[i],loc=ttlloc,
                                                                                 fontsize=ttlfts,pad=ttlpad)
    axes[i].set_extent([LonMin,LonMax,LatMin,LatMax],ccrs.PlateCarree())
    # Figure map
    if coast == True:
     axes[i].add_feature(cfeature.COASTLINE,linewidths=coastlw)
    if lake == True:
     axes[i].add_feature(cfeature.LAKES,linewidths=lakelw,facecolor='none',edgecolor='k')
    if border == True:
     axes[i].add_feature(cfeature.BORDERS,linewidths=borderlw)
    if usstate == True:
     axes[i].add_feature(cfeature.STATES,linewidths=usstatelw)

  #----------------------------------
  # Add map axes and ticks  
  #----------------------------------

  if add_axes == True:

   ### rows 1 to N-1
   if numcases == 'even':
    for r in range(rowceil_min1):
     for c in range(2):
      if c == 0:  # Left column
       map_ticks_and_labels(ax=axes[r,c],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=False,left=True,right=False)
      if c == 1:  # Right column
       map_ticks_and_labels(ax=axes[r,c],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=False,left=False,right=True)

   if numcases == 'odd':
    for i in range(len(cases)-1):
      if (i % 2) == 0: # all even indices are in left column
       map_ticks_and_labels(ax=axes[i],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=False,left=True,right=False)
      if (i % 2) == 1: # all odd indices are in right column
       map_ticks_and_labels(ax=axes[i],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=False,left=False,right=True)

   ### row N
   if numcases == 'even':
    for r in range(rowceil_min1,rowceil):
     for c in range(2):
      if c == 0:  # Left column
       map_ticks_and_labels(ax=axes[r,c],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=True,left=True,right=False)
      if c == 1:  # Right column
       map_ticks_and_labels(ax=axes[r,c],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                            xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                            glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                            top=False,bot=True,left=False,right=True)

   if numcases == 'odd':
    i = (len(cases)-1)-1
    map_ticks_and_labels(ax=axes[i],LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                         xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                         glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                         top=False,bot=True,left=True,right=True)

  #----------------------------------
  # Plot the variables 
  #----------------------------------

  if numcases == 'even':
   for r in range(rowceil):
    for c in range(2):
      if cntr_type == 'AreaFill':
       cntr = axes[r,c].pcolormesh(lon2d,lat2d,prep_data(diff[2*r+c,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                                   norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
      elif cntr_type == 'RasterFill':
       cntr = axes[r,c].pcolormesh(lon2d,lat2d,prep_data(diff[2*r+c,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                                   norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
      if overlay_vec == True:
       vec = axes[r,c].quiver(lon1d_skip,udiff.lat[skip1D],prep_data(udiff[2*r+c,:,:].values)[skip2D],prep_data(vdiff[2*r+c,:,:].values)[skip2D],transform=ccrs.PlateCarree(),scale_units='height',pivot='mid',
                               scale=vec_scale,width=vec_wid,headlength=vec_hdl,headwidth=vec_hdw,headaxislength=vec_hal)
       qkey = axes[r,c].quiverkey(vec,0.8,0.2,vec_ref,str(int(vec_ref))+str(vec_units),labelpos='N',coordinates='figure',color='k')

  if numcases == 'odd':
   for i in range(len(cases)-1):
     if cntr_type == 'AreaFill':
      cntr = axes[i].pcolormesh(lon2d,lat2d,prep_data(diff[i,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                                norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
     elif cntr_type == 'RasterFill':
      cntr = axes[i].pcolormesh(lon2d,lat2d,prep_data(diff[i,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                                norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
     if overlay_vec == True:
      vec = axes[i].quiver(lon1d_skip,udiff.lat[skip1D],prep_data(udiff[i,:,:].values)[skip2D],prep_data(vdiff[i,:,:].values)[skip2D],transform=ccrs.PlateCarree(),scale_units='height',pivot='mid',
                              scale=vec_scale,width=vec_wid,headlength=vec_hdl,headwidth=vec_hdw,headaxislength=vec_hal)
      qkey = axes[i].quiverkey(vec,0.8,0.2,vec_ref,str(int(vec_ref))+str(vec_units),labelpos='N',coordinates='figure',color='k')

  #-------------------------------
  # Color bar for plots 
  #-------------------------------

  cbar = fig.colorbar(cntr,ax=axes,orientation=cbar_orient,ticks=MultipleLocator(tkstd),shrink=cbar_shrk,pad=cbar_pad,label=units,
                                   spacing=cbar_sp,extend=extnd)
  cbar.ax.tick_params(labelsize=cbar_lblsz)

  #------------------------------
  # Add region and point to map
  #------------------------------

  if regbox == True or point == True:

   # Adjusters to put box around entire grid cell
   latadj = abs(float((var.lat[1] - var.lat[2]) / 2))
   lonadj = abs(float((var.lon[1] - var.lon[2]) / 2))

  if regbox == True:

   # Handle values if °W = 180-360
   if regwlon < 0.:
    regwlon = regwlon + 360
   if regelon < 0.:
    regelon = regelon + 360

   # Pick best values for region
   slat = float(var.lat.sel(lat=regslat, method='nearest'))
   nlat = float(var.lat.sel(lat=regnlat, method='nearest'))
   wlon = float(var.lon.sel(lon=regwlon, method='nearest'))
   elon = float(var.lon.sel(lon=regelon, method='nearest'))

   # Handle values if °W = 180-360
   if wlon > 180.0:
    wlon = wlon - 360
   if elon > 180.0:
    elon = elon - 360

   if numcases == 'even':
    for r in range(rowceil):
     for c in range(2):
      draw_region_box(ax=axes[r,c],slat=slat-latadj,nlat=nlat+latadj,wlon=wlon-lonadj,elon=elon+lonadj,
                      linestyle=regline,facecolor='none',edgecolor=regcol,linewidth=reglw,zorder=10)
      
   if numcases == 'odd':
    for i in range(len(cases)-1):
      draw_region_box(ax=axes[i],slat=slat-latadj,nlat=nlat+latadj,wlon=wlon-lonadj,elon=elon+lonadj,
                      linestyle=regline,facecolor='none',edgecolor=regcol,linewidth=reglw,zorder=10)

  if point == True:

   # Pick best values for point
   latpt = float(var.lat.sel(lat=ptlat, method='nearest'))
   lonpt = float(var.lon.sel(lon=ptlon, method='nearest'))

   # Handle values if °W = 180-360
   if lonpt > 180.0:
    lonpt = lonpt - 360

   if numcases == 'even':
    for r in range(rowceil):
     for c in range(2):
      axes[r,c].plot(lonpt,latpt,'ro',markersize=5)
   if numcases == 'odd':
    for i in range(len(cases)-1):
     axes[i].plot(lonpt,latpt,'ro',markersize=5)

  #------------------------
  # Add shapes to map  
  #------------------------

  if numcases == 'even':
   for r in range(rowceil):
    for c in range(2):
     for s in range(len(shape_type)):
      axes[r,c].plot(shape_lons[s],shape_lats[s],marker=shape_type[s],markersize=shape_size[s],markerfacecolor='none',
                      markeredgecolor=shape_col)

  if numcases == 'odd':
   for i in range(len(cases)-1):
    for s in range(len(shape_type)):
     axes[i].plot(shape_lons[s],shape_lats[s],marker=shape_type[s],markersize=shape_size[s],markerfacecolor='none',
                  markeredgecolor=shape_col[s])

  #-----------------------------------------------------------
  # Plot individual maps and append to pdf file if necessary
  #-----------------------------------------------------------

  if Ind_plots == True:

   print('Working on individual difference plots...')

   for i in range(len(cases)-1):

    figi = plt.figure(figsize=(figw,figh),dpi=fdpi)
    axi  = figi.add_subplot(111, projection=proj)
    axi.set_title(fig_let[i]+' '+str(seas)+' '+str(var_name)+str(vec_name)+' '+cases_diff[i],loc=ttlloc,fontsize=ttlfts,pad=ttlpad) 
    axi.set_extent([LonMin,LonMax,LatMin,LatMax],ccrs.PlateCarree())                                   
    if coast == True:
     axi.add_feature(cfeature.COASTLINE,linewidths=coastlw)
    if lake == True:
     axi.add_feature(cfeature.LAKES,linewidths=lakelw,facecolor='none',edgecolor='k')
    if border == True:
     axi.add_feature(cfeature.BORDERS,linewidths=borderlw)
    if usstate == True:
     axi.add_feature(cfeature.STATES,linewidths=usstatelw)
    map_ticks_and_labels(ax=axi,LatMin=LatMin,LatMax=LatMax,LonMin=LonMin,LonMax=LonMax,lattksp=lattksp,lontksp=lontksp,
                         xmin_mj=xmin_mj,ymin_mj=ymin_mj,tkmajlg=tkmajlg,tkminlg=tkminlg,proj=proj,glalpha=glalpha,
                         glcolor=glcolor,lonlblsp=lonlblsp,latlblsp=latlblsp,xpads=xpads,ypads=ypads,tklblsz=tklblsz,
                         top=False,bot=True,left=True,right=True)
    if cntr_type == 'AreaFill':
     cntr = axi.pcolormesh(lon2d,lat2d,prep_data(diff[i,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                           norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
    elif cntr_type == 'RasterFill':
     cntr = axi.pcolormesh(lon2d,lat2d,prep_data(diff[i,:,:].values),transform=ccrs.PlateCarree(),cmap=colort,
                           norm=mpl.colors.BoundaryNorm(np.arange(loval,hival+spval,spval),colort.N,extend=extnd))
    cbar_i = plt.colorbar(cntr,ax=axi,orientation=cbar_orient,ticks=MultipleLocator(tkstd),
                          shrink=cbar_shrk,pad=cbar_pad,label=units,spacing=cbar_sp,extend=extnd)
    cbar_i.ax.tick_params(labelsize=cbar_lblsz)
    if overlay_vec == True:
     vec = axi.quiver(lon1d_skip,udiff.lat[skip1D],prep_data(udiff[i,:,:].values)[skip2D],prep_data(vdiff[i,:,:].values)[skip2D],transform=ccrs.PlateCarree(),scale_units='height',pivot='mid',scale=vec_scale,
                                      width=vec_wid,headlength=vec_hdl,headwidth=vec_hdw,headaxislength=vec_hal)
     qkey = axi.quiverkey(vec,0.8,0.2,vec_ref,str(vec_ref)+str(vec_units),labelpos='N',coordinates='figure',color='k')
    if regbox == True:
     draw_region_box(ax=axi,slat=slat-latadj,nlat=nlat+latadj,wlon=wlon-lonadj,elon=elon+lonadj,
                      linestyle=regline,facecolor='none',edgecolor=regcol,linewidth=reglw,zorder=10)
    if point == True:
     axi.plot(lonpt,latpt,'ro',markersize=5)
    for s in range(len(shape_type)):
     axi.plot(shape_lons[s],shape_lats[s],marker=shape_type[s],markersize=shape_size[s],markerfacecolor='none',
                      markeredgecolor=shape_col[s])

  #--------------------------
  # Save output PDF file
  #--------------------------

  save_multi_image('./'+str(folderpath)+'/'+str(seas)+'_diff_'+str(var_name)+str(vec_name)+'_'+str(extra_name)+str(filesuf))
  plt.close('all')

