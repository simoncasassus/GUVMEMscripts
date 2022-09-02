from astropy.io import fits
import os, sys
import numpy as np
from copy import deepcopy

include_path = os.environ['HOME'] + '/common/python/include/'
sys.path.append(include_path)
import ImUtils
from ImUtils.Resamp import *
import ImUtils.Cube2Im as Cube2Im


canvascube = './cube_canvas.fits'
hdu = fits.open(canvascube)
hdr = hdu[0].header
data = hdu[0].data.squeeze()
cube_shape = data.shape
print(cube_shape)
print(cube_shape[1:3])
nfreqs = cube_shape[0]
hdu.close()
hduim=Cube2Im.slice0(canvascube,ReturnHDUList=True)
hdrim=hduim[0].header

masks = data.copy()

for ichan in range(nfreqs):
    filemask0 =  'mask_channel_' + str(ichan) + '.fits'
    if os.path.exists(filemask0):
        hdu0 = fits.open(filemask0)
        hdr0 = hdu0[0].header
        hdu1 = deepcopy(hdu0)
        mask0 = hdu0[0].data
        print("ichan",ichan)
        masks[ichan,:,:] =  mask0
    else:
        masks[ichan,:,:] =  np.ones(cube_shape[1:3])


hdu[0].data = masks
hdu.writeto('cube_masks.fits',overwrite=True)
