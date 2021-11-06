import numpy as np
import sys
import astropy.constants as const

include_path='/home/simon/common/python/include/'
sys.path.append(include_path)

c_light = const.c.value

print("c_light",c_light)

D=12. #m
nu=230527578576.2 # Hz

nu=3.435093381181E+11

lbda=c_light/nu
print("lbda =",lbda)
FWHM_A= 180. * 3600. * 1.2*lbda/ (D * np.pi) # arcsec
print("FWHM_A",FWHM_A,"arcsec")
sigma_A =  FWHM_A/(2. * np.sqrt(2. * np.log(2)))
rmax=3. #arcsec
noise_cut = 1./np.exp(-0.5 * (rmax / sigma_A)**2)
print("noise_cut",noise_cut)
