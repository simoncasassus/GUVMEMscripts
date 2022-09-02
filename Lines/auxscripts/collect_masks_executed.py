from astropy.io import fits
import os, sys
import re
import numpy as np
from copy import deepcopy

include_path = os.environ['HOME'] + '/common/python/include/'
sys.path.append(include_path)
import ImUtils
from ImUtils.Resamp import *
import ImUtils.Cube2Im as Cube2Im
import PyVtools.Vtools as Vtools
import Gausssmooth

basename = 'mem_lS0.00032_lL0.0_nogrid_maskedb_'
maskdir = './channelmasks/'
os.system("mkdir "+maskdir)

allfiles = os.listdir('.')
memdirs = []
for afile in allfiles:
    if os.path.isdir(afile):
        if basename in afile:
            memdirs.append(afile)


def channumber(name):
    m = re.search('_chan(\d+)', name)
    if m:
        ichan = m.group(1)
    return int(ichan)


canvascube = './cube_canvas.fits'
hdu = fits.open(canvascube)
hdr = hdu[0].header
data = hdu[0].data.squeeze()
cube_shape = data.shape
print("cube_shape",cube_shape[1:3])
nfreqs = cube_shape[0]
hduim=Cube2Im.slice0(canvascube,ReturnHDUList=True)
hdrim=hduim[0].header
masks = data.copy()


memdirs.sort(key=channumber)

for amemdir in memdirs:
    ichan = channumber(amemdir)
    sichan = str(ichan)
    filemask = amemdir + '/mask_channel_' + sichan + '.fits'
    if not os.path.exists(filemask):
        print("does not exist: ", filemask)
        masks[ichan,:,:] =  np.ones(cube_shape[1:3])
        continue

    hdu0 = fits.open(filemask)
    hdr0 = hdu0[0].header
    mask0 = hdu0[0].data
    print("ichan",ichan)
    masks[ichan,:,:] =  mask0


hdu[0].data = masks
hdu.writeto(maskdir+'cube_masks.fits',overwrite=True)
