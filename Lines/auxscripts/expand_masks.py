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
#mask0dir = 'channelmasks_dev/'
mask0dir = './'
#mask1dir = 'channelmasks_expanded/'
#mask0dir = 'channelmasks_expanded/'
mask1dir = './channelmasks_expanded5/'
theta = 0.1  # arcsec, std dev for circular Gaussian smooth
nsigma = 1.
rcutoff = 4.5  #arcsec
View = False
cmap = 'inferno_r'

os.system("mkdir  " + mask1dir)
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


memdirs.sort(key=channumber)

for amemdir in memdirs:
    ichan = str(channumber(amemdir))
    filemask0 = mask0dir + 'mask_channel_' + str(ichan) + '.fits'
    filemask1 = mask1dir + 'mask_channel_' + str(ichan) + '.fits'
    fileresiduals = amemdir + '/out_res_ms.img.image.fits'
    if not os.path.exists(fileresiduals):
        print("does not exist: ", fileresiduals)
        continue

    hdu0 = fits.open(filemask0)
    hdr0 = hdu0[0].header
    hdu1 = deepcopy(hdu0)
    mask0 = hdu0[0].data
    mask1 = hdu1[0].data
    #if View:
    #    Vtools.View(hdu0, cmap=cmap)
    nx, ny = mask0.shape
    #print("nx, ny",nx,ny)
    x = np.arange(0, nx)
    y = np.arange(0, ny)
    X, Y = np.meshgrid(x, y)
    X0 = (float(nx) - 1) / 2.
    Y0 = (float(ny) - 1) / 2.
    rrs = np.sqrt((X - hdr0['CRPIX1'] + 1)**2 +
                  (Y - hdr0['CRPIX2'] + 1)**2) * hdr0['CDELT2'] * 3600.
    #Vtools.View(rrs)
    hdures = fits.open(fileresiduals)
    hdrres = hdures[0].header
    resids = np.squeeze(hdures[0].data)
    #if View:
    #    Vtools.View(hdures, cmap=cmap)

    sigma_x = (theta / 3600.) / hdr0['CDELT2']
    sigma_y = sigma_x
    smask = Gausssmooth.Gauss_filter(mask0,
                                     sigma_x,
                                     sigma_y,
                                     0.,
                                     Verbose=False)

    sresids = Gausssmooth.Gauss_filter(resids,
                                       sigma_x,
                                       sigma_y,
                                       0.,
                                       Verbose=False)

    noise = np.std(sresids)
    #print("noise", noise)
    noise = np.std(resids[(smask > 1E-3)])
    #print("noise outside mask", noise)

    expandedmask = (sresids > nsigma * noise) & (smask < 0.99)
    naddedpixels = np.sum(expandedmask)
    if naddedpixels > 0:
        print("expanded channel ", ichan)
        # mask1 = smask.copy()
        mask1[expandedmask] = 0.
        smask1 = Gausssmooth.Gauss_filter(mask1,
                                          sigma_x,
                                          sigma_y,
                                          0.,
                                          Verbose=False)
        #Vtools.View(smask1, cmap='Greys')

        smask1[(smask1 < 0.99)] = 0.
        smask1[(smask1 >= 0.99)] = 1.
        smask1[(rrs > rcutoff)] = 1.
        hdu1[0].data = smask1
        hdu1.writeto(filemask1, overwrite=True)
        if View:
            Vtools.View(hdures, cmap='Greys')
            print("expanded mask")
            #Vtools.View([hdu1, hdu0], cmap=cmap, contlevels=[0.5])
            Vtools.View(hdu1, cmap=cmap)
