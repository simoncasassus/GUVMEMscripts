from astropy.io import fits
import os, sys
import numpy as np

cubename = sys.argv[1]

hdu = fits.open(cubename)

hdr = hdu[0].header
data = hdu[0].data.squeeze()

cube_shape = data.shape

print(cube_shape)

nfreqs = cube_shape[0]

hdu.close()

for i in range(0, nfreqs):
    channel_data = 1-data[i]
    fits.writeto("mask_channel_"+str(i)+".fits", channel_data, hdr, overwrite=True)

