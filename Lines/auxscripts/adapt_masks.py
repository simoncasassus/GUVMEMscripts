from astropy.io import fits
import os, sys
import numpy as np
from copy import deepcopy

include_path = os.environ['HOME'] + '/common/python/include/'
sys.path.append(include_path)
import ImUtils
from ImUtils.Resamp import *
import ImUtils.Cube2Im as Cube2Im

canvascube_ori = './manual_masks/cube_canvas.mask.image.0.4.fits'
hdu_ori = fits.open(canvascube_ori)
hdr_ori = hdu_ori[0].header
data = hdu_ori[0].data.squeeze()
cube_ori_shape = data.shape
print(cube_ori_shape)
nfreqs_ori = cube_ori_shape[0]
hdu_ori.close()
freqs_ori = (np.arange(nfreqs_ori) - hdr_ori['CRPIX3'] +
             1) * hdr_ori['CDELT3'] + hdr_ori['CRVAL3']


canvascube = './cube_canvas.fits'
hdu = fits.open(canvascube)
hdr = hdu[0].header
data = hdu[0].data.squeeze()
cube_shape = data.shape
print(cube_shape)
nfreqs = cube_shape[0]
hdu.close()
hduim=Cube2Im.slice0(canvascube,ReturnHDUList=True)
hdrim=hduim[0].header


ifreq0=0
freqs = (np.arange(nfreqs) - hdr['CRPIX3'] +
#            1) * hdr['CDELT3'] + hdr['CRVAL3']
#ifreq0=37
#freqs = (np.arange(ifreq0,ifreq0+1) - hdr['CRPIX3'] +
             1) * hdr['CDELT3'] + hdr['CRVAL3']


dra_visalign=0.015271016271116633+0.013322184375831063
ddec_visalign=-0.0038944634625002377-0.0015646401204495355

#delta_x 0.013322184375831063
#delta_y -0.0015646401204495355


for ifreq,afreq in enumerate(freqs):
    ifreq+=ifreq0
    ichannel_ori = np.argmin(np.fabs(afreq - freqs_ori))
    print("ifreq ",ifreq, "ichannel_ori",ichannel_ori)
    maskfile_ori = "./manual_masks/mask_channel_" + str(ichannel_ori) + ".fits"
    maskfile = "./channelmasks_dev/mask_channel_" + str(ifreq) + ".fits"
    hdu_mask_ori=fits.open(maskfile_ori)
    hdr_mask_ori = hdu_mask_ori[0].header
    #hdr_mask = deepcopy(hdrim)
    hdr_mask = deepcopy(hdr_mask_ori)
    hdr_mask['BUNIT']=''
    hdr_mask['CRVAL1'] -= (dra_visalign / 3600.) / np.cos(hdr_mask['CRVAL2'] * np.pi / 180.)
    hdr_mask['CRVAL2'] -= (ddec_visalign / 3600.)
    hdr_mask['NAXIS1'] = hdrim['NAXIS1']
    hdr_mask['NAXIS2'] = hdrim['NAXIS2']
    hdr_mask['CRPIX1'] = hdrim['CRPIX1']
    hdr_mask['CRPIX2'] = hdrim['CRPIX2']
    hdr_mask['CDELT1'] = hdrim['CDELT1']
    hdr_mask['CDELT2'] = hdrim['CDELT2']
    
    hdu_resamp = gridding(hdu_mask_ori, hdr_mask, fullWCS=False,ReturnHDUList=True,fileout=maskfile,mode='nearest')
    
    
    
    # fits.writeto(maskfile, channel_data, hdr, overwrite=True)
    

    
    # ds9regionfile = 'ds9_' + str(i + 1) + '.reg'
    # if os.path.isfile(ds9regionfile):
    #     fitsfileout_ds9region = 'ds9_' + str(i + 1) + '.fits'
    #     convert_ds9region_tofits(maskfile, fitsfileout_ds9region,
    #                              ds9regionfile)
    #     hdu0 = fits.open(maskfile)
    #     mask0 = hdu0[0].data
    #     hduds9 = fits.open(fitsfileout_ds9region)
    #     maskds9 = hduds9[0].data
    #     hduds9.close()
    #     mask1 = mask0 * maskds9
    #     hdu0[0].data = mask1
    #     hdu0.writeto(maskfile, overwrite=True)
    #     hdu0.close()
