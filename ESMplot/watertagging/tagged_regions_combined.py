####################################################################
# This script determines how to plot tagged regions on a map
#  Handles tagged regions for combined bk 0ka and aaf 2090CE time slice
#  Note that these are almost the same as the bk 0ka tags except sundaland and sundaocean are combined
####################################################################

from matplotlib.patches import Rectangle
import matplotlib.lines as lines
import cartopy.crs as ccrs

####################################################################
# 1. Define each tagged region below as it will appear on map
#
# 2. Use a loop outside of the function to plot all on the same 
#    map or only one at a time
#
# This script contains draw_land_tags and draw_ocean_tags
#
# NOTE: Provided in this script is an example of drawing 40 specific
#       tags.
#
####################################################################

#-------------------
# Land tags
#-------------------

def draw_land_tags(numtag,ax,lw,major,minor,color,zorder):

 '''
 Required Parameters
 -----------------------------------------------------------------
 numtag
  class: 'int', number of tag to draw, use this with a loop
                to plot all on the same map or only one at a time

 ax
  class: 'matplotlib.axes.Axes', axis on which to draw polgons

 lw
  class: 'string', width of each line

 major
  class: 'string', line style of the major lines
 
 minor
  class: 'string', line style of the minor lines

 color
  class: 'string', color of the lines

 zorder
  class: 'int', zorder of the lines
 -----------------------------------------------------------------

 EXAMPLE FOR RECTANGLE:
 rlats = 'int' (southernmost latitude of rectangle)
 rlatn = 'int' (northernmost latitude of rectangle)
 rlonw = 'int' (westernmost longitude of rectangle)
 rlone = 'int' (easternmost longitude of rectangle)
 ax.add_patch(Rectangle( (rlonw,rlats),              # starting point
                         abs(abs(rlonw)-abs(rlone)), # X length
                         abs(abs(rlatn)-abs(rlats)), # Y length
              linestyle=major,facecolor='none',
              edgecolor=color,linewidth=lw,zorder=zorder))
 NOTE: If crossing Equator (Y) or Prime Meridan (X), 
       add (+) instead of subtract (-) when determining
       X or Y length.

 EXAMPLE FOR LINE:
 rlats = 'int' (southernmost latitude of line)
 rlatn = 'int' (northernmost latitude of line)
 rlonw = 'int' (westernmost longitude of line)
 rlone = 'int' (easternmost longitude of line)
 ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
 '''

 if numtag == 0:
  # 1. Antarctica   
  rlats = -60
  rlatn = -60
  rlonw = -180 
  rlone = 180 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
 
 if numtag == 1:
  # 2. North America
  rlats = 15
  rlatn = 90
  rlonw = -180 #+180
  rlone = -18 #+180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 2: 
  # 3. South America (-Amazon)      # crosses equator
  rlats = -60
  rlatn = 15
  rlonw = -180 #+180
  rlone = -18 #+180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
 
 if numtag == 3:
  # 4. Eurasia      
  rlats = 90   # Northern border 
  rlatn = 90 
  rlonw = -18 
  rlone = 180 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 4    # Eastern border
  rlatn = 90
  rlonw = 180 
  rlone = 180 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 4    # Southern border part 1
  rlatn = 4  
  rlonw = 119 
  rlone = 180 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 4    # Southern border part 2
  rlatn = 17  
  rlonw = 119 
  rlone = 119 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 17   # Southern border part 3
  rlatn = 17 
  rlonw = 95   
  rlone = 119  
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 4    # Southern border part 4
  rlatn = 17
  rlonw = 95 
  rlone = 95 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 4    # Southern border part 5
  rlatn = 4  
  rlonw = 52 
  rlone = 95 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 4    # Southern border part 6
  rlatn = 37
  rlonw = 52 
  rlone = 52 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 37   # Southern border part 7
  rlatn = 37
  rlonw = -18 
  rlone = 52  
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 37   # Western border
  rlatn = 90
  rlonw = -18 
  rlone = -18
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))

 if numtag == 4:
  # 5. Africa (-Congo)           # crosses prime meridian and equator
  rlats = -60
  rlatn = 37
  rlonw = -18 #+180
  rlone = 52  #-180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)+abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
 
 if numtag == 5:
  # 10. Sundaland combined 
  rlats = -10
  rlatn = 17
  rlonw = 95  #-180
  rlone = 119 #-180
  # Compute width and height with crossing checks
  dx = abs(rlone - rlonw) if (rlone * rlonw >= 0) else abs(rlone) + abs(rlonw)
  dy = abs(rlatn - rlats) if (rlatn * rlats >= 0) else abs(rlatn) + abs(rlats)
  ax.add_patch(Rectangle((rlonw, rlats), dx, dy,transform=ccrs.PlateCarree(),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
 
 if numtag == 6:
  # 10. Sahulland                  # crosses equator
  rlats = -19
  rlatn = 4
  rlonw = 119  #-180
  rlone = 150  #-180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
 
 if numtag == 7:
  # 11. Australia/Oceania         # crosses equator
  rlats = -60
  rlatn = 4
  rlonw = 52   #-180
  rlone = 180  #-180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
 
 if numtag == 8:
  # 12. Amazon       # crosses equator 
  rlats = -10
  rlatn = 10
  rlonw = -70  #+180
  rlone = -45  #+180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=minor,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
 
 if numtag == 9: 
  # 13. Congo        # crosses equator 
  rlats = -10
  rlatn = 10
  rlonw = 10  #-180
  rlone = 35  #-180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=minor,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))


#-------------------
# Ocean tags
#-------------------

def draw_ocean_tags(numtag,ax,lw,major,minor,color,zorder):

 '''
 Required Parameters
 -----------------------------------------------------------------
 numtag
  class: 'int', number of tag to draw, use this with a loop
                to plot all on the same map or only one at a time

 ax
  class: 'matplotlib.axes.Axes', axis on which to draw polgons

 lw
  class: 'string', width of each line

 major
  class: 'string', line style of the major lines
 
 minor
  class: 'string', line style of the minor lines

 color
  class: 'string', color of the lines

 zorder
  class: 'int', zorder of the lines
 -----------------------------------------------------------------

 EXAMPLE FOR RECTANGLE:
 rlats = 'int' (southernmost latitude of rectangle)
 rlatn = 'int' (northernmost latitude of rectangle)
 rlonw = 'int' (westernmost longitude of rectangle)
 rlone = 'int' (easternmost longitude of rectangle)
 ax.add_patch(Rectangle( (rlonw,rlats),              # starting point
                         abs(abs(rlonw)-abs(rlone)), # X length
                         abs(abs(rlatn)-abs(rlats)), # Y length
              linestyle=major,facecolor='none',
              edgecolor=color,linewidth=lw,zorder=zorder))
 NOTE: If crossing Equator (Y) or Prime Meridan (X), 
       add (+) instead of subtract (-) when determining
       X or Y length.

 EXAMPLE FOR LINE:
 rlats = 'int' (southernmost latitude of line)
 rlatn = 'int' (northernmost latitude of line)
 rlonw = 'int' (westernmost longitude of line)
 rlone = 'int' (easternmost longitude of line)
 ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
 '''

 if numtag == 10:
  # 14. North Pacific 
  rlats = 25   # Western Hemisphere portion
  rlatn = 90
  rlonw = -180
  rlone = -100
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
  rlats = 25   # Eastern Hemisphere portion
  rlatn = 90
  rlonw = 118
  rlone = 180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 11:
  # 15. North Atlantic
  rlats = 25
  rlatn = 48
  rlonw = 0
  rlone = 0
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 48
  rlatn = 48
  rlonw = 0
  rlone = 20
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 48
  rlatn = 90
  rlonw = 20
  rlone = 20
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 90
  rlatn = 90
  rlonw = -100
  rlone = 20
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 48
  rlatn = 90
  rlonw = -100
  rlone = -100
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 48
  rlatn = 48
  rlonw = -100
  rlone = -75 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 25
  rlatn = 48
  rlonw = -75  
  rlone = -75 
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 25
  rlatn = 25
  rlonw = -75
  rlone = 0
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))

 if numtag == 12:
  # 16. North Barents/Arctic Sea
  rlats = 48
  rlatn = 90
  rlonw = 20
  rlone = 118
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 13:
  # 17. Tropical Pacific NE
  rlats = 25   # Northern border          
  rlatn = 25
  rlonw = -150
  rlone = -100
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 18   # Eastern border part 1    
  rlatn = 25
  rlonw = -100
  rlone = -100
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 18   # Eastern border part 2             
  rlatn = 18
  rlonw = -100
  rlone = -92
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 15   # Eastern border part 3    
  rlatn = 18
  rlonw = -92
  rlone = -92
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 15   # Eastern border part 4   
  rlatn = 15
  rlonw = -92
  rlone = -84
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 8    # Eastern border part 5    
  rlatn = 15
  rlonw = -84
  rlone = -84
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 8    # Eastern border part 6   
  rlatn = 8
  rlonw = -84
  rlone = -75
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 8    # Eastern border part 6 
  rlatn = 8
  rlonw = -84
  rlone = -75
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 0    # Eastern border part 7
  rlatn = 8
  rlonw = -75
  rlone = -75
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 0    # Southern border        
  rlatn = 0
  rlonw = -150
  rlone = -75
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 0    # Western border 
  rlatn = 25
  rlonw = -150
  rlone = -150
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))

 if numtag == 14:
  # 18. Caribbean
  rlats = 48   # North border              
  rlatn = 48
  rlonw = -100
  rlone = -75
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 8    # East border              
  rlatn = 48
  rlonw = -75
  rlone = -75
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 18   # West border              
  rlatn = 48
  rlonw = -100
  rlone = -100
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 18   # Southern border part 1    
  rlatn = 18
  rlonw = -100
  rlone = -92
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 15   # Southern border part 2   
  rlatn = 18
  rlonw = -92
  rlone = -92
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 15   # Southern border part 3  
  rlatn = 15
  rlonw = -92
  rlone = -84
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 8    # Southern border part 4   
  rlatn = 15
  rlonw = -84
  rlone = -84
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))
  rlats = 8    # Southern border part 5  
  rlatn = 8
  rlonw = -84
  rlone = -75
  ax.add_line(lines.Line2D([rlonw,rlone],[rlats,rlatn],linestyle=major,color=color,lw=lw,zorder=zorder))

 if numtag == 15:
  # 19. Tropical Atlantic NW
  rlats = 0
  rlatn = 25
  rlonw = -75
  rlone = -30
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 16:
  # 20. Tropical Atlantic NE      # crosses prime meridian
  rlats = 0
  rlatn = 25
  rlonw = -30
  rlone = 20
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)+abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 17:
  # 21. Mediterranean
  rlats = 30
  rlatn = 48
  rlonw = 0
  rlone = 45
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 18:
  # 22. Indian Ocean NW/Arabian Sea
  rlats = 4
  rlatn = 30
  rlonw = 30
  rlone = 75
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 19:
  # 23. Indian Ocean NE/Bay of Bengal
  rlats = 4
  rlatn = 30
  rlonw = 75
  rlone = 95
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 20:
  # 26. Sundaland combined
  rlats = -10
  rlatn = 17
  rlonw = 95
  rlone = 119
  dx = abs(rlone - rlonw) if (rlone * rlonw >= 0) else abs(rlone) + abs(rlonw)
  dy = abs(rlatn - rlats) if (rlatn * rlats >= 0) else abs(rlatn) + abs(rlats)
  ax.add_patch(Rectangle((rlonw, rlats), dx, dy,transform=ccrs.PlateCarree(),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 21:
  # 29. Tropical Pacific North Central
  rlats = 0    # Western Hemisphere portion
  rlatn = 25
  rlonw = -180
  rlone = -150
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
  rlats = 0    # Eastern Hemisphere portion
  rlatn = 25
  rlonw = 150
  rlone = 180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 22:
  # 30. Tropical Pacific SE
  rlats = -25
  rlatn = 0
  rlonw = -150
  rlone = -60
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 23:
  # 31. Tropical Atlantic SW
  rlats = -25
  rlatn = 0
  rlonw = -60
  rlone = -10
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 24:
  # 32. Tropical Atlantic SE                # crosses prime meridian
  rlats = -25
  rlatn = 0
  rlonw = -10
  rlone = 20
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)+abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 25:
  # 33. Tropical Indian Ocean SW       # crosses equator
  rlats = -25
  rlatn = 4
  rlonw = 30
  rlone = 70
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 26:
  # 34. Tropical Indian Ocean South Central         # crosses equator
  rlats = -25
  rlatn = 4
  rlonw = 70
  rlone = 95
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=5))

 if numtag == 27: 
  # 35. Tropical Indian Ocean SE
  rlats = -25
  rlatn = -10
  rlonw = 95
  rlone = 119
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 28:
  # 36. Sahul region ocean   # crosses equator
  rlats = -25
  rlatn = 4
  rlonw = 119
  rlone = 150
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)+abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 29:
  # 37. Tropical Pacific South Central
  rlats = -25   # Western Hemisphere portion
  rlatn = 0
  rlonw = -180
  rlone = -150
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
  rlats = -25   # Eastern Hemisphere portion
  rlatn = 0
  rlonw = 150
  rlone = 180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 30:
  # 38. South Pacific
  rlats = -90   # Western Hemisphere portion
  rlatn = -25
  rlonw = -180
  rlone = -70
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))
  rlats = -90   # Eastern Hemisphere portion
  rlatn = -25
  rlonw = 140
  rlone = 180
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=5))

 if numtag == 31:
  # 39. South Atlantic              #     crosses prime meridian
  rlats = -90
  rlatn = -25
  rlonw = -70
  rlone = 25
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)+abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))

 if numtag == 32:
  # 40. South Indian Ocean
  rlats = -90
  rlatn = -25
  rlonw = 25
  rlone = 140
  ax.add_patch(Rectangle((rlonw,rlats),abs(abs(rlonw)-abs(rlone)),abs(abs(rlatn)-abs(rlats)),
                linestyle=major,facecolor='none',edgecolor=color,linewidth=lw,zorder=zorder))




 
