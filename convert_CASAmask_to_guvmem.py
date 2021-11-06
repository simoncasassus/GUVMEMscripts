from astropy.io import fits
import os, sys
import numpy as np

include_path='/home/simon/common/python/include/'
sys.path.append(include_path)
from ImUtils.Resamp import gridding
from copy import deepcopy

CASAmask='/strelka_ssd/simon/HD135344B/red/LBall/selfcal_tclean/tclean_HD135344Bbriggs2.0_noself_filledmask.mask.fits'

hdu = fits.open(CASAmask)
hdr = hdu[0].header
data = hdu[0].data.squeeze()
cube_shape = data.shape
print(cube_shape)

pixscl=0.003/3600.
side=2048
hdr_ref=deepcopy(hdr)

hdr_ref['NAXIS1']=side
hdr_ref['NAXIS2']=side
hdr_ref['CDELT1']=-pixscl
hdr_ref['CDELT2']=pixscl
hdr_ref['CRPIX1']=int(side/2)+1.
hdr_ref['CRPIX2']=int(side/2)+1.

hdu_resamp=gridding(hdu,hdr_ref,ReturnHDUList=True)

#def gridding(arg1, imagefile_2,fileout=False,fullWCS=True,ReturnHDU=False,ReturnHDUList=False,order=1,Verbose=False):


#nfreqs = 1

resamp=hdu_resamp[0].data
uvmemmask_data = 1-resamp

fits.writeto("guvmem_mask.fits", uvmemmask_data, hdr_ref, overwrite=True)

