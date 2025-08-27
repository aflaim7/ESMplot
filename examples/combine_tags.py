import xarray as xr
from ESMplot.watertagging.combine_tagged_regions import (
    combine_regions_to_new_tag
)

ds = xr.open_dataset('/RAID/datasets/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/archive/atm/hist/climatology/' \
'f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124_monthly_climatology_cat.nc')

# Average for 
ds_combined = combine_regions_to_new_tag(
    ds,
    regions=("EURO", "NASA", "INDA", "SASA"),
    new_region="ERAS",
    # weights={"EURO":1, "NASA":1, "INDA":1, "SASA":1},  # optional
    require_all=True,       # set True if you only want averages when *all* are present
    keep_nonregion_vars=True # keep other non-region variables
)

