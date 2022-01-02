from astropy.io import fits
import os, sys
import numpy as np

import pyregion

include_path=os.environ['HOME']+'/common/python/include/'
sys.path.append(include_path)

from ImUtils.Cube2Im import slice0


def convert_ds9region_tofits(file_ref,file_out,ds9region):
    print("file_ref",file_ref)
    hdu = slice0(file_ref, ReturnHDUList=True)
    hdu.data = np.ones(hdu[0].data.shape)
    # hdu = fits.open(file_ref)
    hdr = hdu[0].header
    region = pyregion.open(ds9region)
    mask = np.array(np.invert(region.get_mask(hdu[0])), dtype=int)
    hdu[0].data=mask
    print("file_out",file_out)
    hdu.writeto(file_out,overwrite=True)
    hdu.close()
    del region
    return


# SAME FITS FILE USED TO DEFINE REGION:
cubename = './output_OOselfcal_usermask_pyrarestore_chi2_statw_nogrid/_ph0_residuals.residual.image.fits'
hdu = fits.open(cubename)
hdr = hdu[0].header
data = hdu[0].data.squeeze()
#data = hdu[0].data
cube_shape=data.shape
print("cube_shape",cube_shape)
if len(cube_shape) > 2:
    nfreqs = cube_shape[0]
else:
    nfreqs = 1

for i in range(nfreqs):
    print(" i  ", i)
    #if len(cube_shape) > 2:
    #    channel_data = 1-data[i]
    #else:
    #    channel_data = 1-data
    #maskfile="mask_channel_"+str(i)+".fits"
    #hdu[0].data=channel_data
    #print("maskfile ", maskfile)
    #hdu.writeto(maskfile, overwrite=True)
    ds9regionfile='ds9_'+str(i+1)+'.reg'
    if os.path.isfile(ds9regionfile):
        fitsfileout_ds9region='ds9_'+str(i+1)+'.fits'
        convert_ds9region_tofits(cubename,fitsfileout_ds9region,ds9regionfile)
        
        #hdu0=fits.open(maskfile)
        #mask0=hdu0[0].data
        #hduds9=fits.open(fitsfileout_ds9region)
        #maskds9=hduds9[0].data
        #hduds9.close()
        #mask1=mask0*maskds9
        #hdu0[0].data=mask1
        #
        #hdu0.writeto(maskfile,overwrite=True)
        #hdu0.close()
        
