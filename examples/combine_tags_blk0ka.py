import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
import xarray as xr
from ESMplot.watertagging.combine_tagged_regions import (
    combine_regions_to_new_tag
)

# Import the monthly concatenated climatology of the water tagged time slice
ds = xr.open_dataset('/net/paleonas.wustl.edu/volume1/blkshare/ajthompson/postproc/' \
'f.e12.F_1850_CAM5.wiso.f19.0ka.002.watertags.2.cam.h0.0006-0025.climo.nc')

## Combine regions
# Sundaland
ds_combined = combine_regions_to_new_tag(
    ds,
    regions=("SLNW", "SLNE", "SLSW", "SLSE"),
    new_region="SLCB",
    inherit_attrs="consensus",
    consensus_only_keys={"units"},  # require 'units' to agree across inputs
    prefer_keys_first_present=("long_name","cell_methods"),  # but take these from preferred source
    keep_nonregion_vars=True # keep other non-region variables
)

# Sundaocean
ds_combined = combine_regions_to_new_tag(
    ds,
    regions=("SONW", "SONE", "SOSW", "SOSE"),
    new_region="SOCB",
    inherit_attrs="consensus",
    consensus_only_keys={"units"},  # require 'units' to agree across inputs
    prefer_keys_first_present=("long_name","cell_methods"),  # but take these from preferred source
    keep_nonregion_vars=True # keep other non-region variables
)

## Write out netcdf
ds_combined.to_netcdf('/RAID/datasets/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/archive/atm/hist/climatology/' \
'f.e12.F_1850_CAM5.wiso.f19.0ka.002.watertags.2.cam.h0.0006-0025.climo_combReg.nc')