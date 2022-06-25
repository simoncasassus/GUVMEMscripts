import sys
import numpy as np
import re
from astropy.io import fits
import os

file_residuals = 'out_res_ms.img.image.fits'
file_restored = 'restored_nat.fits'

hdu_resids = fits.open(file_residuals)
hdu_restor = fits.open(file_restored)

resids = hdu_resids[0].data
restor = hdu_restor[0].data

mask = np.invert(np.isnan(resids))
rms = np.std(resids[mask])

mask = np.invert(np.isnan(restor))
peak = np.max(restor[mask])
psnr = peak / rms
print("Peak %.2e rms %.2e PSNR %.2f" % (peak, rms, psnr))



resids = np.nan_to_num(resids)
rms = np.std(resids)

restor = np.nan_to_num(restor)
peak = np.max(restor)
psnr = peak / rms
print("Peak %.2e rms %.2e PSNR %.2f" % (peak, rms, psnr))
