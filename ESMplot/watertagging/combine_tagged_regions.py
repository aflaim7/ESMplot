#######################################################################################################
# 
# This function combines the variables associated with a given list of tagged regions
#   to compare the input with other water tag experiments that use different tags.
# For example, combine Europe and Asia tags to compare with an experiment that uses a Eurasia tag.
# Note that the outer edges of the combined tags must be equal to the comparison target.
#
#######################################################################################################

import re
from collections import defaultdict
import xarray as xr

def combine_regions_to_new_tag(  # same name as before for easy swapping
    ds: xr.Dataset,
    regions=("EURO", "NASA", "INDA", "SASA"),
    new_region="ERAS",
    *,
    # Optional per-region multipliers applied before summing (e.g., scale by area fraction)
    weights: dict | None = None,     # {"EURO":1, "NASA":1, ...}
    require_all: bool = False,       # if True, only combine when *all* regions for a group are present
    keep_nonregion_vars: bool = True,
    dtype="float32",
    skipna=True,                     # True → ignore NaNs when summing
    join="exact",                    # "exact" or "outer" coord alignment
    zero_fill=False                  # if join!="exact": fill missing coords with 0 before summing
) -> xr.Dataset:
    """
    Collapse per-region variables into a new *summed* region (e.g., ERAS).

    Matches variables shaped like:
      [<prefix>][<sep>]<REGION><tail>
    where <prefix> is optional, <sep> is an optional underscore, <REGION>∈regions,
    and <tail> is the remaining suffix (e.g., '18OI', 'V', 'r', etc.).

    Examples:
      'NASA18OI'         -> prefix='',     sep='',  region='NASA', tail='18OI'
      'PRECRC_NASA18Or'  -> prefix='PRECRC', sep='_', region='NASA', tail='18Or'

    Output variable name:
      f"{prefix}{sep}{new_region}{tail}"

    NOTE: This version **sums** across regions (not average). If you previously used the
    averaging build, this is the only logic change.
    """
    if not regions:
        raise ValueError("Provide at least one region prefix in `regions`.")

    region_alt = "|".join(map(re.escape, regions))
    pat = re.compile(rf"^(?P<prefix>.*?)(?P<sep>_)?(?P<region>{region_alt})(?P<tail>.+)$")

    groups = defaultdict(dict)    # (prefix, sep, tail) -> {region: DataArray}
    region_vars = []

    for vname, da in ds.data_vars.items():
        m = pat.match(vname)
        if m:
            key = (m.group("prefix") or "", m.group("sep") or "", m.group("tail"))
            groups[key][m.group("region")] = da
            region_vars.append(vname)

    new_vars = {}
    missing_summary = {}

    for (prefix, sep, tail), reg_map in groups.items():
        present = sorted(reg_map.keys())
        if require_all and len(present) != len(regions):
            missing_summary[(prefix, sep, tail)] = sorted(set(regions) - set(present))
            continue

        # collect, respecting canonical region order
        das, wts = [], []
        for r in regions:
            if r in reg_map:
                das.append(reg_map[r])
                wts.append(1.0 if weights is None else float(weights.get(r, 0.0)))
            elif not require_all:
                continue

        if not das:
            continue

        # align
        das_aligned = xr.align(*das, join=join)
        if weights is None:
            arr = xr.concat(das_aligned, dim="__region__")
        else:
            arr = xr.concat([d * w for d, w in zip(das_aligned, wts)], dim="__region__")

        # optional zero fill when using outer joins
        if zero_fill and join != "exact":
            arr = arr.fillna(0)

        # ********** SUM instead of MEAN **********
        eras = arr.sum(dim="__region__", skipna=skipna)
        # *****************************************

        eras = eras.astype(dtype)
        new_name = f"{prefix}{sep}{new_region}{tail}"
        eras.name = new_name
        new_vars[new_name] = eras

    # build output
    parts = []
    if keep_nonregion_vars:
        keep = [v for v in ds.data_vars if v not in set(region_vars)]
        parts.append(ds[keep])
    else:
        parts.append(xr.Dataset(coords=ds.coords))

    parts.append(xr.Dataset(new_vars))
    ds_out = xr.merge(parts)
    ds_out.attrs = dict(ds.attrs)

    if missing_summary:
        ds_out.attrs[f"{new_region}_missing_regions_info"] = str(missing_summary)

    return ds_out