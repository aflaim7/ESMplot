# Using NCO to calculate monthly climatology from monthly time slice output
cd /RAID/datasets/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004/archive/atm/hist/

#ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-01.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-01.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-02.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-02.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-03.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-03.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-04.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-04.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-05.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-05.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-06.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-06.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-07.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-07.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-08.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-08.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-09.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-09.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-10.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-10.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-11.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-11.nc
ncra f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.{2105..2124}-12.nc climatology/f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-12.nc

# Combine monthly averages
ncrcat f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124-{01..12}.nc f.ie12.BRCP85C5CN.f19_g16.LME.004_2100watertags.004.cam.h0.2105-2124_monthly_climatology_cat.nc