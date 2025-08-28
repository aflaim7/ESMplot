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

def combine_regions_to_new_tag(
    ds: xr.Dataset,
    regions=("EURO", "NASA", "INDA", "SASA"),
    new_region="ERAS",
    *,
    # math/combination controls
    weights: dict | None = None,       # per-region multipliers before summing
    require_all: bool = False,         # only combine when *all* regions for a group are present
    join: str = "exact",               # "exact" or "outer"
    zero_fill: bool = False,           # if join!="exact": fill NaNs with 0 before summing
    skipna: bool = True,               # ignore NaNs when summing
    dtype: str = "float32",

    # attribute/encoding inheritance controls
    inherit_attrs: str = "prefer_order",  # "prefer_order" | "consensus"
    copy_encoding: bool = True,           # try to copy .encoding (e.g., _FillValue, scale_factor)
    annotate_sources: bool = True,        # add helper attrs like 'combined_from_regions'
    consensus_only_keys: set | None = None,  # if set, only require consensus for these keys
    prefer_keys_first_present: tuple = (),   # keys to always take from preferred source even if consensus mode
    keep_nonregion_vars: bool = True
) -> xr.Dataset:
    """
    Sum per-region variables into a new region (e.g., ERAS) while inheriting attrs/encoding.

    Matches variables named like:
      [<prefix>][<sep>]<REGION><tail>
    where <prefix> is optional, <sep> is an optional underscore, <REGION>∈regions,
    and <tail> is the suffix (e.g., '18OI', 'V', 'r', etc.).

    Output variable name:
      f"{prefix}{sep}{new_region}{tail}"

    Attribute inheritance:
      - prefer_order: copy attrs from the first region in `regions` that appears in the group
      - consensus: copy only keys whose values are identical across all present inputs
      - You can also:
          * specify `consensus_only_keys` to require consensus only for a subset (e.g., {'units'})
          * specify `prefer_keys_first_present` to always take some keys from the preferred source
      - We also optionally copy `.encoding`.
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

    def _preferred_region(present_regions):
        # first region in declared order that is present
        for r in regions:
            if r in present_regions:
                return r
        return present_regions[0]

    def _merge_attrs(das_by_region: dict[str, xr.DataArray]):
        present_regions = list(das_by_region.keys())
        # pick preferred source DA
        pref_region = _preferred_region(present_regions)
        pref_da = das_by_region[pref_region]
        merged = {}

        if inherit_attrs == "prefer_order":
            merged = dict(pref_da.attrs)
        elif inherit_attrs == "consensus":
            # union of keys across inputs
            keys = set().union(*(da.attrs.keys() for da in das_by_region.values()))
            for k in keys:
                if k in prefer_keys_first_present:
                    merged[k] = pref_da.attrs.get(k)
                    continue
                values = [das_by_region[r].attrs.get(k) for r in present_regions]
                # if consensus_only_keys provided, require consensus only for those
                if consensus_only_keys is not None and k not in consensus_only_keys:
                    # take from preferred if not in the consensus set
                    merged[k] = pref_da.attrs.get(k)
                else:
                    # require exact equality (including None)
                    all_equal = all(v == values[0] for v in values)
                    if all_equal:
                        merged[k] = values[0]
                    else:
                        # skip conflicting key
                        continue
        else:
            raise ValueError("inherit_attrs must be 'prefer_order' or 'consensus'")

        if annotate_sources:
            merged["combined_from_regions"] = ",".join(sorted(present_regions))
            merged["source_attr_region"] = _preferred_region(present_regions)
            merged["combine_operation"] = "sum"
        return merged, pref_da.encoding if copy_encoding else None

    new_vars = {}
    missing_summary = {}

    for (prefix, sep, tail), reg_map in groups.items():
        present = [r for r in regions if r in reg_map]  # keep canonical order
        if require_all and len(present) != len(regions):
            missing_summary[(prefix, sep, tail)] = sorted(set(regions) - set(present))
            continue

        if not present:
            continue

        # align inputs in the same order as `present`
        das = [reg_map[r] for r in present]
        das_aligned = xr.align(*das, join=join)

        # apply weights (as multipliers) before summing
        if weights is None:
            arr = xr.concat(das_aligned, dim="__region__")
        else:
            arr = xr.concat(
                [d * float(weights.get(r, 0.0)) for d, r in zip(das_aligned, present)],
                dim="__region__",
            )

        if zero_fill and join != "exact":
            arr = arr.fillna(0)

        eras = arr.sum(dim="__region__", skipna=skipna).astype(dtype)

        # inherit attrs & encoding
        das_by_region_aligned = {r: d for r, d in zip(present, das_aligned)}
        merged_attrs, exemplar_encoding = _merge_attrs(das_by_region_aligned)
        eras.attrs = merged_attrs
        if copy_encoding and isinstance(exemplar_encoding, dict):
            # avoid copying incompatible keys; xarray will ignore unknowns on write
            eras.encoding = dict(exemplar_encoding)

        # name & stash
        new_name = f"{prefix}{sep}{new_region}{tail}"
        eras.name = new_name
        new_vars[new_name] = eras

    # assemble output
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
