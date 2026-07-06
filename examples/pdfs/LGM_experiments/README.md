# LGM Forcing Decomposition — Seasonal Water Tagging Maps

Andrew Flaim  
May 25, 2026  
af106@rice.edu  

## Overview

This directory contains iCESM water tagging simulation results including text-based water tag maps as well as global maps of seasonal precipitation and δ¹⁸Oₚ anomalies across LGM full-forcing and single-forcing experiments relative to the 0ka control. Each figure shows the difference between a 21ka forcing experiment and the 0ka control, plotted for each of the 40 tagged source regions.

All maps are Pacific-centered (central longitude = 180°) and individual tagged region maps have 850 hPa wind vector anomalies overlaid.

---
## Directory structure

`/seasonalDiffs/` contains seasonal difference maps for each individual tagged region, sorted according to forcing experiment.  
`/taggedMaps/` contains global text-based maps for ANNUAL watertag anomalies for each region of interest. Destination region definitions are summarized in the "Desination regions" section below.  
`/SundaTags/` contains initial exploratory plots made in January 2026. This directory contains global maps (both individual experiments and anomalies) and text-based maps for the Sunda shelf region.  
`/prect_d18Op_notags/` contains seasonal total (not broken up into tagged regions) precipitation and d18Op anomalies for each experiment minus the control. Sub-directories contain Atlantic and Pacific centered maps. `/pacific_centered/low_latitudes/` contains maps restricted to 40S-40N.  
`/taggedMaps/EqIPWP_singleForcing/` contains water tag text maps for annual and seasonal single forcing experiments for the Equatorial IPWP.

---
## Destination regions
These region boundaries were used for the respective text-based tag maps found in `/taggedMaps/`  

| Region | Latitude bounds | Longitude bounds |
|---|---|---|
| Equatorial IPWP | 10°S – 10°N | 90°E – 150°E |
| Indian monsoon | 5°N – 25°N | 60°E – 80°E |
| SE Asian monsoon | 10°N – 20°N | 90°E – 130°E |
| Northern Australia | 20°S – 10°S | 120°E – 150°E |
| Equatorial East Africa | 5°S – 5°N | 20°E – 50°E |
| Equatorial West Africa | 0° – 10°N | 20°W – 20°E |
| Equatorial South America | 10°S – 0° | 60°W – 30°W |

---
## Experiments

All plots show **experiment minus 0ka control**.

| Label | Forcing | Case string |
|---|---|---|
| 0ka | Pre-industrial control | `f.e12.F_1850_CAM5.wiso.f19.0ka.002.watertags.2` |
| 21ka | Full LGM forcing | `f.e12.F_1850_CAM5.wiso.f19.21ka.fullforcing.modern.d18Osw.001.watertags` |
| 21kaGHG | Greenhouse gases only | `f.e12.F_1850_CAM5.wiso.f19.21kaGHG.001.watertags.2` |
| 21kaGlac | Ice sheets + topography only | `f.e12.F_1850_CAM5.wiso.f19.21kaGlac.001.watertags.2` |
| 21kaSL | Sea level only | `f.e12.F_1850_CAM5.wiso.f19.21kaSL.002.watertags` |

All simulations use years 6–25 of the climatology (`h0.0006-0025.climo.nc`).

---

## Seasons

Each forcing experiment is plotted for 5 seasons:

| Season | Months |
|---|---|
| ANN | Annual mean (all 12 months) |
| DJF | December–January–February |
| MAM | March–April–May |
| JJA | June–July–August |
| SON | September–October–November |

---

## Variables

**Precipitation (Pi)** — tagged precipitation from each source region (mm/day), contour range ±0.5 mm/day.

**δ¹⁸Oₚ** — precipitation-weighted oxygen isotope ratio from each source region (‰), contour range ±1.0‰.

**Wind vectors** — 850 hPa wind anomalies (m/s), reference arrow = 10 m/s. Wind vector lengths were normalized to the 95th percentile of wind anomaly magnitude.

---

## Scripts

| Script | Description |
|---|---|
| `examples/calculate_watertags_LGM_forcing_seasons.py` | Main call script that loops over seasons and forcings |
| `examples/calculate_watertags_LGM_forcing_seasons_textmaps.py` | Call script that loops over seasons and forcings for text maps (duplicate?) |
| `examples/plot_LGM_PRECT_d18Op_seasonal_forcing_pacificCenter.py` | Call script that loops over seasons and forcings for total PRECT and δ¹⁸Oₚ centered on the pacific, likewise for the atlanticCenter variation|
| `ESMplot/watertagging/watertag_plots_cenlon_LGMregions.py` | Plotting functions (`plot_tagged_precip_and_d18Op`) |
| `ESMplot/watertagging/seas_avg_LL_watertags.py` | Seasonal averaging for water tagging variables |
| `ESMplot/watertagging/tagged_regions.py` | Tag region boundary definitions |

---

## Tagged source regions

40 regions total: 13 land, 27 ocean. Region boundaries and codes are defined in `ESMplot/watertagging/tagged_regions.py`.

| # | Code | Name |
|---|---|---|
| 1 | ANTA | Antarctica |
| 2 | NAMG | North America / Greenland |
| 3 | SAME | South America (excl. Amazon) |
| 4 | ERAS | Eurasia |
| 5 | AFRI | Africa (excl. Congo) |
| 6 | SLNW | Sundaland NW |
| 7 | SLNE | Sundaland NE |
| 8 | SLSW | Sundaland SW |
| 9 | SLSE | Sundaland SE |
| 10 | SAHL | Sahulland |
| 11 | AUST | Australia / Oceania |
| 12 | AMAZ | Amazon |
| 13 | CONG | Congo |
| 14 | NPAC | North Pacific |
| 15 | NATL | North Atlantic |
| 16 | ARCT | North Barents / Arctic Sea |
| 17 | TPNE | Tropical Pacific NE |
| 18 | CARB | Caribbean |
| 19 | TANW | Tropical Atlantic NW |
| 20 | TANE | Tropical Atlantic NE |
| 21 | MEDI | Mediterranean |
| 22 | ARAB | Indian Ocean NW / Arabian Sea |
| 23 | BOFB | Indian Ocean NE / Bay of Bengal |
| 24 | SONW | Sundaland NW ocean |
| 25 | SONE | Sundaland NE ocean / South China Sea |
| 26 | SOSW | Sundaland SW ocean |
| 27 | SOSE | Sundaland SE ocean |
| 28 | TPNW | Tropical Pacific NW |
| 29 | TPNC | Tropical Pacific North Central |
| 30 | TPSE | Tropical Pacific SE |
| 31 | TASW | Tropical Atlantic SW |
| 32 | TASE | Tropical Atlantic SE |
| 33 | TISW | Tropical Indian SW |
| 34 | TISC | Tropical Indian South Central |
| 35 | TISE | Tropical Indian SE |
| 36 | SAHO | Sahul region ocean |
| 37 | TPSC | Tropical Pacific South Central |
| 38 | SPAC | South Pacific |
| 39 | SATL | South Atlantic |
| 40 | SIND | South Indian |

---
## Communication archive
Relevant communication for this analysis is included below for future reference.  
---
In person meeting June 19, 2026  
To-Do: 
- Fix seasonal single forcing text maps for Indian Monsoon  ✅ Done July 6,2026
- Add season label to panels of text maps ✅ Done July 6,2026
- Make seasonal single forcing text maps for East Africa ✅ Done July 6,2026
- Make seasonal single forcing text maps for SEAmonsoon ✅ Done July 6,2026
- Plot mid-tropospheric omega maps for single forcing and seasonal
---
Andrew Flaim <af106@rice.edu>	Thu, Jun 18, 2026 at 9:35 PM
To: "Konecky, Bronwen" <bkonecky@wustl.edu>  
Hi Bronwen,

Apologies again for taking so long to get around to this, but here's a summary of the new LGM watertag plots based on our last conversation:

I re-plotted the global (meaning not tag-specific) precipitation and d18O maps with latitude limits spanning 40S-40N and scaled the contours accordingly. This includes both annual and seasonal mean maps. Hopefully this helps highlight the tropical changes better. You can find those results here: /paleonas/aflaim/ESMplot/examples/pdfs/LGM_experiments/prect_d18Op_noTags/pacific_centered/low_latitudes/

I also made seasonal and single forcing versions of the Equatorial IPWP watertag text maps. You can find those here: /paleonas/aflaim/ESMplot/examples/pdfs/LGM_experiments/taggedMaps/EqIPWP_singleForcing

Finally, I adjusted the color scale range for the individual region maps for the annual mean full forcing d18O plots to better highlight the isotope changes from each region. You can find those updated maps on slides 41-80 of this file: /paleonas/aflaim/ESMplot/examples/pdfs/LGM_experiments/seasonalDiffs/full_forcing/$21ka$-0ka_ANN_watertagged_prect_d18Op_wind850hPa_d18OscaleAdjusted.pdf
(This especially helps for plots like slide 57 and slide 62.)

Hopefully this is useful and let me know if you'd like any adjustments or new plots.

Best,
Andrew

---
In person meeting June 5, 2026  
Requested analysis:  
- Replot LGM d18O maps to be 40S-40N and rescale the color contours  
- Make single forcing EqIPWP water tag text maps for ANN and seasonal
- Adjust 21ka-0ka full forcing individual region map color bars and latitude range  

---
Konecky, Bronwen <bkonecky@wustl.edu>	Thu, May 28, 2026 at 12:26 PM
To: Andrew Flaim <af106@rice.edu>

Hi again Andrew,

Wow your markdown file is extremely nice. :) And thanks for generating all these plots! I’m still sorting through them. One thing I am wondering is whether you could make a few plots of just maps of ANN and seasonal mean PRECT and d18Op anomalies (relative to PI) with 850 hPa wind overlays for each of the LGM simulations. So not for the water tags, but for the non-tagged simulations (or, just the regular PRECT and d18Op for the same years 6-25 from the water tag simulations would work too).

This will help to give some overall context for regions that are wetter or drier overall, but receive less/more moisture from different tags.

Thank you!

---
Konecky, Bronwen <bkonecky@wustl.edu>	Thu, May 21, 2026 at 3:46 PM
To: "af106@rice.edu" <af106@rice.edu>, "Flaim, Andrew" <aflaim@wustl.edu>

Hi Andrew,

I’m finally rekindling the LGM water tags project and really hoping to get this darn thing submitted this summer. I was going through the google slides doc you shared back in January—thanks again for this. I’ve been brainstorming some next steps. I think the first thing would be if you could please run Alex’s ESMplot code to generate all those maps with several different “red box” destinations around the tropical water belt, for the 21ka_ALL – PI:

Equatorial IPWP (10N-10S, 90E-150E)
Indian monsoon region (5-25N,60E-80E) 
SE Asian monsoon region (10N-20N, 90-130E)
Northern Australia (10S-20S, 120E-150E)
Equatorial East Africa (5S-5N, 20E-50E)
Equatorial West Africa (0-10N, 20W-20E)
Equatorial South America (0-10S, 60W-30W)

Ideally these would all be Pacific-centered… if that does not break things.

It would also be really helpful to have ANN and seasonal mean PRECT and d18Op with 850 hPa wind overlays for each of the LGM simulations (including the single forcing runs) – PI.

I am pretty sure Alex already has code for these plots in ESMplot. Let me know if not.

I know it will be a ton of plots, but once those are generated I can look at all the PDFs and wrap my head around the story that we can piece together for the LGM. Then we can meet to discuss. I think taking a bit more of a bird’s-eye view of the whole land-based tropical rain belt, rather than hyperfocusing on the IPWP, might actually make the paper a simpler pitch. I’m currently thinking AGU Earth and Space Sciences for a journal.

I know you have a lot of other things on your plate right now, so just let me know what a super rough timeline would be and I can definitely work around it.

Thank you so much!

-Bronwen

---
Zoom message  
From Flaim, Andrew  
To: Konecky, Bronwen  
January 12, 2026  

I've completed some preliminary post-processing for the LGM water tag simulations. You can see the output here: https://docs.google.com/presentation/d/1ZmaIJaMheRCu1MfYbuRhX8Ts5zTsDtYNHoeu27fBXmI/edit?usp=sharing

You can see all of the output for the individual forcing water tags here: /paleonas/aflaim/ESMplot/examples/pdfs/LGM_experiments

If you'd like to reference the ESMplot scripts I used to generate these plots you can see that here: /paleonas/aflaim/ESMplot/examples/calculate_watertags_LGM.py

For these plots I drew a box generally over the IPWP/sunda region to calculate the tagged changes, but now that the plotting is set up we could easily move the box anywhere. We can also make Pacific-centered maps if you'd prefer. These plots serve as a sanity check that the land/ocean changes between the LGM and present are evident, especially in the sea level forcing.

Do you have any preliminary science questions or other related analysis that could help guide the project from here? I'd love to keep working on this project so let me know what would be most helpful.