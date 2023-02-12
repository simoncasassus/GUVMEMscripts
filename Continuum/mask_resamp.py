import numpy as np
import sys
from astropy.io import fits
import re
import os

include_path=os.environ['HOME']+'/common/python/include/'
sys.path.append(include_path)
from ImUtils import Resamp

#import Resamp


# #include_path=os.environ['HOME']+'/common/python/include/'
# #sys.path.append(include_path)
# #from Imutils import Resamp 
# 
# import Resamp
# 
# file_canvas=sys.argv[1]
# file_mask=sys.argv[2]
# fileout=sys.argv[3]
# Resamp.gridding(file_mask,file_canvas,fileout=fileout)



file_canvas=sys.argv[1]
file_mask=sys.argv[2]
fileout=sys.argv[3]

hdu_mask = fits.open(file_mask)
mask = hdu_mask[0].data
mask[(mask == 1)] = 2
mask[(mask < 1)] = 1
mask[(mask == 2)] = 0
hdu_mask[0].data=mask

hdu_mask.writeto('foo.fits',overwrite=True)

hdu_resamp=Resamp.gridding(hdu_mask,file_canvas,fileout=False,ReturnHDUList=True,order=0)

hdu_resamp.writeto('bar.fits',overwrite=True)

mask = hdu_resamp[0].data
mask[(mask == 1)] = 2
mask[(mask < 1)] = 1
mask[(mask == 2)] = 0
hdu_resamp[0].data=mask
hdu_resamp.writeto(fileout,overwrite=True)
