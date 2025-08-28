import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
import xarray as xr
from ESMplot.watertagging.combine_tagged_regions import (
    combine_regions_to_new_tag
)

# Import the monthly concatenated climatology of the water tagged time slice
ds = xr.open_dataset('/RAID/datasets/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/archive/atm/hist/climatology/' \
'f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124_monthly_climatology_cat.nc')

## Combine regions
# ERAS
ds_combined = combine_regions_to_new_tag(
    ds,
    regions=("EURO", "NASA", "INDA", "SASA"),
    new_region="ERAS",
    inherit_attrs="consensus",
    consensus_only_keys={"units"},  # require 'units' to agree across inputs
    prefer_keys_first_present=("long_name","cell_methods"),  # but take these from preferred source
    keep_nonregion_vars=True # keep other non-region variables
)

# NAMG
ds_combined = combine_regions_to_new_tag(
    ds_combined,
    regions=("WNAM", "ENAM"),
    new_region="NAMG",
    inherit_attrs="consensus",
    consensus_only_keys={"units"},
    prefer_keys_first_present=("long_name","cell_methods"),
    keep_nonregion_vars=True
)

# NATL
ds_combined = combine_regions_to_new_tag(
    ds_combined,
    regions=("WNAT", "ENAT"),
    new_region="NATL",
    inherit_attrs="consensus",
    consensus_only_keys={"units"},  # require 'units' to agree across inputs
    prefer_keys_first_present=("long_name","cell_methods"),  # but take these from preferred source
    keep_nonregion_vars=True # keep other non-region variables
)

# NPAC
ds_combined = combine_regions_to_new_tag(
    ds_combined,
    regions=("WNPA", "ENPA"),
    new_region="NPAC",
    inherit_attrs="consensus",
    consensus_only_keys={"units"},  # require 'units' to agree across inputs
    prefer_keys_first_present=("long_name","cell_methods"),  # but take these from preferred source
    keep_nonregion_vars=True # keep other non-region variables
)

## Write out netcdf
ds_combined.to_netcdf('/RAID/datasets/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/archive/atm/hist/climatology/' \
'f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124_monClim_combReg.nc')