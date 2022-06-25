from astropy.io import fits
import os, sys
import numpy as np
import pyregion

def convert_ds9region_tofits(file_ref,file_out,ds9region):
    print("file_ref",file_ref)
    hdu = fits.open(file_ref)
    hdu[0].data = np.ones(hdu[0].data.squeeze().shape)
    hdr = hdu[0].header
    hdr.pop("NAXIS3", None)
    hdr.pop("NAXIS4", None)
    hdr["NAXIS"]=2
    hdu[0].header = hdr
    region = pyregion.open(ds9region)
    mask = np.array(np.invert(region.get_mask(hdu[0])), dtype=int)
    hdu[0].data=mask
    print("file_out",file_out)
    hdu.writeto(file_out,overwrite=True)
    hdu.close()
    del region
    return
    
    
fitsfile = sys.argv[1]
regfile = sys.argv[2]
file_out = sys.argv[3]

convert_ds9region_tofits(fitsfile, file_out, regfile)
