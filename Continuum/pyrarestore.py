import sys
from astropy.io import fits 
from pyralysis.io import DaskMS
# from pyralysis.reconstruction import Image
import astropy.units as u
import numpy as np
from pyralysis.units import lambdas_equivalencies
from pyralysis.transformers.weighting_schemes import Uniform, Robust
from pyralysis.transformers import Gridder, HermitianSymmetry, DirtyMapper
from pyralysis.io import FITS
from astropy.units import Quantity
import re


residual_ms = "out_res_ms" #input
model_fits = "mod_out.fits"  # input 
weighting="briggs"
robustparam=2.

######################################################################

hdu_model=fits.open(model_fits)
im_model=hdu_model[0].data
head_model=hdu_model[0].header
hdu_model.close()

pixscl=head_model['CDELT2'] * 3600. # arcsec
side= head_model['NAXIS1']

x = DaskMS(input_name=residual_ms)
dataset = x.read()
dataset.field.mean_ref_dir
dataset.psf[0].sigma

# h_symmetry = HermitianSymmetry(input_data=dataset)
# h_symmetry.apply()

imsize = [side, side]

#dx = Quantity([dataset.theo_resolution/7, dataset.theo_resolution/7])
#dx.to(u.arcsec)
dx = [pixscl, pixscl] * u.arcsec

du = (1/(imsize*dx)).to(u.lambdas, equivalencies=lambdas_equivalencies())

gridder = Gridder(imsize=imsize, cellsize=dx, hermitian_symmetry=True)

fits_io = FITS()




if re.search('Natural',weighting,re.IGNORECASE):
    dirty_mapper = DirtyMapper(input_data=dataset, imsize=imsize, cellsize=dx, stokes="I,Q", hermitian_symmetry=False)
    dirty_images_natural = dirty_mapper.transform()
    dirty_image_natural = dirty_images_natural[0].data[0].compute()
    #dirty_beam_natural = dirty_images_natural[1].data[0].compute()
    fits_io.write(dirty_images_natural[0].data, output_name='pyra_dirty_nat.fits')
    fits_io.write(dirty_images_natural[0].data, output_name=file_pyra_dirty)

    #gridded_visibilities_nat = dirty_mapper.uvgridded_visibilities.compute()
    #gridded_weights_nat = dirty_mapper.uvgridded_weights.compute()

elif re.search('Briggs',weighting,re.IGNORECASE):
    ######################################################################
    # Briggs weighting:

    robust = Robust(input_data=dataset, robust_parameter=robustparam, gridder=gridder)
    robust.apply()

    dataset.calculate_psf()
    
    dirty_mapper = DirtyMapper(input_data=dataset, imsize=imsize, cellsize=dx, stokes="I,Q", hermitian_symmetry=False)

    dirty_images_robust = dirty_mapper.transform()
    dirty_image = dirty_images_robust[0].data[0].compute()
    #dirty_beam = dirty_images_robust[1].data[0].compute()
    fits_io.write(dirty_images_robust[0].data, output_name=file_pyra_dirty)


elif re.search('Uniform',weighting,re.IGNORECASE):
    ######################################################################
    # Uniform weighting

    uniform = Uniform(input_data=dataset, gridder=Gridder(imsize=imsize, uvcellsize=du))

    uniform.apply()

    dataset.calculate_psf()
    
    dirty_mapper = DirtyMapper(input_data=dataset, imsize=imsize, cellsize=dx, stokes="I,Q", hermitian_symmetry=False)
    
    dirty_images_uniform = dirty_mapper.transform()
    
    dirty_image = dirty_images_uniform[0].data[0].compute()
    dirty_beam = dirty_images_uniform[1].data[0].compute()
    
    fits_io.write(dirty_images_uniform[0].data, output_name=file_pyra_dirty)

else:
    print("unrecognised weighting scheme:",weighting)



# RESTORING:


hdu_resid=fits.open(file_pyra_dirty)
im_resid=hdu_res[0].data
head_resid= hdu_res[0].header
bmaj=head_res['BMAJ']
bmin=head_res['BMIN']
bpa=head_res['BPA']

from Gausssmooth import Gauss_filter
stdev_x = bmaj / (head_res['CDELT2']*2.*sqrt(2*np.log(2)))
stdev_y = bmin / (head_res['CDELT2']*2.*sqrt(2*np.log(2)))
PA=bpa

im_model_s=Gauss_filter(im_model, stdev_x, stdev_y, PA)

im_resto=im_model_s+im_resid

hdu_resid[0].data=im_resto
hdu_resid.writeto('restored_pyra.fits')
