from astropy.io import fits
import os, sys
import numpy as np

import astropy.units as u

include_path=os.environ['HOME']+'/common/python/include/'
sys.path.append(include_path)

include_path=os.environ['HOME']+'/common/python/extgitpacks/pyFIST/'
sys.path.append(include_path)

from fitsmanip import fist


def convert_ds9region_tofits(file_ref,file_out,ds9region):
    hdu = fits.open(file_ref)
    hdr = hdu[0].header
    cdelt = hdr['CDELT2']
    rmap=fist(file_ref,cdelt*u.deg)
    rmap.maskRegion(ds9region)
    rmap.writeMask(file_out)
    hdu.close()
    return



cubename = 'cube_canvas.mask.image.0.4.fits'
hdu = fits.open(cubename)
hdr = hdu[0].header
data = hdu[0].data.squeeze()
cube_shape = data.shape
print(cube_shape)
nfreqs = cube_shape[0]
hdu.close()

for i in range(0, nfreqs):
    channel_data = 1-data[i]
    maskfile="mask_channel_"+str(i)+".fits"
    fits.writeto(maskfile, channel_data, hdr, overwrite=True)
    ds9regionfile='ds9_'+str(i+1)+'.reg'
    if os.path.isfile(ds9regionfile):
        fitsfileout_ds9region='ds9_'+str(i+1)+'.fits'
        convert_ds9region_tofits(maskfile,fitsfileout_ds9region,ds9regionfile)
        hdu0=fits.open(maskfile)
        mask0=hdu0[0].data
        hduds9=fits.open(fitsfileout_ds9region)
        maskds9=hduds9[0].data
        hduds9.close()
        mask1=mask0*maskds9
        hdu0[0].data=mask1
        hdu0.writeto(maskfile,overwrite=True)
        hdu0.close()
        
