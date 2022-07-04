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

#python pyra_dirty_maps.py residual_ms file_pyra_dirty weighting robust side cell

residual_ms = "out_res_ms"  #input
model_fits = "mod_out.fits"  # input
weighting = "briggs"
#weighting = "natural"
#weighting = "uniform"
robustparam = 2.
if weighting == 'briggs':
    fileout = 'restored_pyra_' + weighting + '_r' + str(robustparam) + '.fits'
    fileresiduals = residual_ms + "_" + weighting + '_r' + str(
        robustparam) + ".img.pyra.fits"
else:
    fileout = 'restored_pyra_' + weighting + '.fits'
    fileresiduals = residual_ms + "_" + weighting + ".img.pyra.fits"

from astropy.convolution import interpolate_replace_nans
from astropy.convolution import convolve as astropy_convolve
from scipy.signal import convolve as scipy_convolve
from scipy.signal import choose_conv_method


def Gauss_filter(inarray,
                 stdev_x,
                 stdev_y,
                 PA,
                 Plot=False,
                 Spike=False,
                 Boundary='extend',
                 ConvoMethod='auto',
                 UseAstropy=False):
    ''' 
        inarray: input data array
        stdev_x: float
	1sigma std dev. along BMAJ in pixels 
        stdev_y: float
	1sigma std dev. along BMIN in pixels
        PA: East of North in degrees  '''

    IsCube = False
    LargerThanACube = False
    datashape = inarray.shape
    if (len(datashape) > 3):
        print(
            "larger than a cube, looping over  assumming first 3 are the relevant ones"
        )
        (nz0, ny0, nx0) = (datashape[-3], datashape[-2], datashape[-1])
        print("looping over 3rd dimmension with nz0=", nz0)
        LargerThanACube = True
        inarray0 = inarray.copy()
        inarray = inarray0[0, :]
        IsCube = True
    elif (len(datashape) == 3):
        IsCube = True
        (nz0, ny0, nx0) = datashape
        print("this is a cube, looping over 3rd dimmension with nz0=", nz0)
    elif (len(datashape) == 2):
        (ny0, nx0) = datashape
    else:
        sys.exit("smaller than an image")

    nx = min(ny0, min(nx0, int(7. * stdev_x)))
    nx = nx + ((nx + 1) % 2)
    ny = nx

    #x=np.arange(1,nx+1)
    #y=np.arange(1,ny+1)
    x = np.arange(0, nx)
    y = np.arange(0, ny)
    X, Y = np.meshgrid(x, y)
    X0 = (float(nx) - 1) / 2.
    Y0 = (float(ny) - 1) / 2.

    print("Kernel center: x0", X0, "Y0", Y0, " Kernel dimmensions:", nx, ny)

    #----------
    theta = np.pi * (90. - PA) / 180.  #
    A = 1
    a = np.cos(theta)**2 / (2. * stdev_x**2) + np.sin(theta)**2 / (2. *
                                                                   stdev_y**2)
    b = np.sin(2 * theta) / (4. * stdev_x**2) - np.sin(
        2. * theta) / (4. * stdev_y**2)
    c = np.sin(theta)**2 / (2. * stdev_x**2) + np.cos(theta)**2 / (2. *
                                                                   stdev_y**2)

    Z = A * np.exp(-(a * (X - X0)**2 - 2. * b * (X - X0) * (Y - Y0) + c *
                     (Y - Y0)**2))

    Z /= np.sum(Z)

    if Plot == True:
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        plt.imshow(Z, cmap=cm.jet, origin='lower')
        plt.show()

    print("data dims", inarray.shape)
    print("kernel  dims", Z.shape)

    if (IsCube):
        smootharray = inarray.copy()
        for k in range(nz0):
            print("k", k)
            im = np.double(inarray[k, :, :])
            if UseAstropy:
                im_smooth = astropy_convolve(im, Z)
            else:
                ##im = interpolate_replace_nans(im, Z)
                bestmethod = choose_conv_method(im, Z)
                #if (bestmethod != ConvoMethod):
                #        print("WARNING: not using the best ConvoMethod, which is ",bestmethod)
                #        #im_smooth = scipy_convolve(im, Z,method=ConvoMethod,mode='same')
                ##print("im ",im.shape,im.dtype)
                ##print("Z",Z.shape,Z.dtype)
                if ((bestmethod != ConvoMethod) and (ConvoMethod != 'auto')):
                    print("WARNING not using default  ConvoMethod, which is ",
                          bestmethod)
                    im_smooth = scipy_convolve(im,
                                               Z,
                                               mode='same',
                                               method=ConvoMethod)
                else:
                    im_smooth = scipy_convolve(im, Z, mode='same')
                print("im_smooth.shape", im_smooth.shape, "im.shape", im.shape)

            smootharray[k, :, :] = im_smooth
            if Plot == True:
                plt.imshow(im_smooth, cmap=cm.magma, origin='lower')
                plt.show()
    elif (len(datashape) == 2):
        if UseAstropy:
            smootharray = astropy_convolve(inarray, Z)
        else:
            # im = interpolate_replace_nans(im, Z)
            im = np.double(inarray)
            bestmethod = choose_conv_method(im, Z)
            if ((bestmethod != ConvoMethod) and (ConvoMethod != 'auto')):
                print("WARNING not using default  ConvoMethod, which is ",
                      bestmethod)
                smootharray = scipy_convolve(im,
                                             Z,
                                             mode='same',
                                             method=ConvoMethod)
            else:
                smootharray = scipy_convolve(im, Z, mode='same')
        if Plot == True:
            plt.imshow(smootharray, cmap=cm.magma, origin='lower')
            plt.show()
        if (Spike):
            im_spike = np.zeros(inarray.shape)
            im_spike[int(nx0 / 2), int(ny0 / 2)] = 1.
            print("spike at", int(nx0 / 2), int(ny0 / 2))
            smooth_spike = convolve(im_spike, Z, boundary='extend')
            hdu = fits.PrimaryHDU()
            hdu.data = im_spike
            hdu.writeto('spike.fits', overwrite=True)
            hdu.data = smooth_spike
            hdu.writeto('spike_smooth.fits', overwrite=True)

    if LargerThanACube:
        inarray0[0, :] = smootharray
        return inarray0
    else:
        return smootharray


file_pyra_dirty = fileresiduals

hdu_model = fits.open(model_fits)
im_model = hdu_model[0].data
head_model = hdu_model[0].header

pixscl = head_model['CDELT2'] * 3600.  # arcsec
side = head_model['NAXIS1']

print("loading residual ms")
x = DaskMS(input_name=residual_ms)
dataset = x.read(data_column='DATA', calculate_psf=True)
dataset.field.mean_ref_dir
dataset.psf[0].sigma

# h_symmetry = HermitianSymmetry(input_data=dataset)
# h_symmetry.apply()

imsize = [side, side]

#dx = Quantity([dataset.theo_resolution/7, dataset.theo_resolution/7])
#dx.to(u.arcsec)
dx = [pixscl, pixscl] * u.arcsec

du = (1 / (imsize * dx)).to(u.lambdas, equivalencies=lambdas_equivalencies())

print("Init gridder")
gridder = Gridder(imsize=imsize, cellsize=dx, hermitian_symmetry=True)

fits_io = FITS()

print("Weighting scheme")

if re.search('Natural', weighting, re.IGNORECASE):
    print("Natural weights: Init dirty_mapper")
    dirty_mapper = DirtyMapper(input_data=dataset,
                               imsize=imsize,
                               cellsize=dx,
                               stokes="I,Q",
                               hermitian_symmetry=False)

    print("Compute natural weights image")

    dirty_images_natural = dirty_mapper.transform()
    dirty_image_natural = dirty_images_natural[0].data[0].compute()
    #dirty_beam_natural = dirty_images_natural[1].data[0].compute()

    fits_io.write(dirty_images_natural[0].data,
                  output_name='pyra_dirty_nat.fits')

    fits_io.write(dirty_images_natural[0].data, output_name=file_pyra_dirty)

    #gridded_visibilities_nat = dirty_mapper.uvgridded_visibilities.compute()
    #gridded_weights_nat = dirty_mapper.uvgridded_weights.compute()

elif re.search('Briggs', weighting, re.IGNORECASE):
    ######################################################################
    # Briggs weighting:

    robust = Robust(input_data=dataset,
                    robust_parameter=robustparam,
                    gridder=gridder)
    robust.apply()

    dataset.calculate_psf()

    dirty_mapper = DirtyMapper(input_data=dataset,
                               imsize=imsize,
                               cellsize=dx,
                               stokes="I,Q",
                               hermitian_symmetry=False)

    dirty_images_robust = dirty_mapper.transform()
    dirty_image = dirty_images_robust[0].data[0].compute()
    #dirty_beam = dirty_images_robust[1].data[0].compute()
    fits_io.write(dirty_images_robust[0].data, output_name=file_pyra_dirty)

elif re.search('Uniform', weighting, re.IGNORECASE):
    ######################################################################
    # Uniform weighting

    uniform = Uniform(input_data=dataset,
                      gridder=Gridder(imsize=imsize, uvcellsize=du))

    uniform.apply()

    dataset.calculate_psf()

    dirty_mapper = DirtyMapper(input_data=dataset,
                               imsize=imsize,
                               cellsize=dx,
                               stokes="I,Q",
                               hermitian_symmetry=False)

    dirty_images_uniform = dirty_mapper.transform()

    dirty_image = dirty_images_uniform[0].data[0].compute()
    dirty_beam = dirty_images_uniform[1].data[0].compute()

    fits_io.write(dirty_images_uniform[0].data, output_name=file_pyra_dirty)

else:
    print("unrecognised weighting scheme:", weighting)

# RESTORING:

hdu_resid = fits.open(file_pyra_dirty)
im_resid = hdu_resid[0].data
head_resid = hdu_resid[0].header
bmaj = head_resid['BMAJ']
bmin = head_resid['BMIN']
bpa = head_resid['BPA']

stdev_x = bmaj / (head_resid['CDELT2'] * 2. * np.sqrt(2 * np.log(2)))
stdev_y = bmin / (head_resid['CDELT2'] * 2. * np.sqrt(2 * np.log(2)))
PA = bpa

beam = (np.pi /
        (4. * np.log(2))) * bmaj * bmin * (1. / head_resid['CDELT2'])**2

print("Smoothing model image")

im_model_s = Gauss_filter(im_model, stdev_x, stdev_y, PA)
im_model_s *= beam

head_model['BUNIT'] = 'Jy/beam'
head_model['BMAJ'] = bmaj
head_model['BMIN'] = bmin
head_model['BPA'] = bpa

hdu_model[0].data = im_model_s
hdu_model[0].header = head_model
hdu_model.writeto('mod_out_s.fits', overwrite=True)

im_resto = im_model_s + im_resid

hdu_resid[0].data = im_resto
hdu_resid.writeto(fileout, overwrite=True)
