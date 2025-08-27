# Using NCO to calculate monthly climatology from monthly time slice output

in=/RAID/datasets/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/archive/atm/hist/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.210501-212412.nc
outdir=/RAID/datasets/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/archive/atm/hist/climatology/
mkdir -p "$outdir"
outfile=f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124_monthly_climatology.nc


# 1-based (Fortran) indexing so m=1..12 is Jan..Dec
for m in {1..12}; do
  # take every 12th timestep starting at month m
  ncks -O -F -d time,$m,,12 "$in" "$outdir/mon_${m}.nc"
  # average across the time records (years) for this month
  ncra -O "$outdir/mon_${m}.nc" "$outdir/clim_mon_${m}.nc"
done

# stack the 12 monthly fields onto a new "month" dimension
ncecat -O -u month "$outdir"/clim_mon_*.nc "$outdir$outfile"

# make month 1..12 instead of 0..11 and add a label
ncap2 -O -s 'month=month+1; month@long_name="calendar month (1-12)"' \
  "$outdir$outfile" "$outdir$outfile"

# (optional) clean up intermediates
rm "$outdir"/mon_*.nc "$outdir"/clim_mon_*.nc