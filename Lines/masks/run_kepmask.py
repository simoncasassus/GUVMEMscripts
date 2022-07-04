# execute in CASA

import numpy as np

#execfile('keplerian_mask.py')


#def z_func(r):
#    return 0.33 * r**0.76

def z_func(r):
    r0=2.
    taper=(1.-np.tanh(r/r0))
    return (0.5 * (r/r0)**0.8)*taper

#make_mask(image='cube_canvas.image', inc=17.6, PA=242.0, mstar=1.7, dist=135.7, vlsr=7.12e3, zr =0.3, nbeams=2.0, r_min=0.01, r_max = 1.5, dV0=400.)    
#make_mask(image='cube_canvas_uvtaper.image', inc=17.6, PA=242.0, mstar=1.7, dist=135.7, vlsr=7.12e3, zr =0.3, nbeams=2.0, r_min=0.01, r_max = 1.5, dV0=400.)    
#make_mask(image='cube_canvas.image', inc=17.6, PA=242.0, mstar=1.7, dist=135.7, vlsr=7.12e3, z_func=z_func, nbeams=2.0, r_min=0.01, r_max = 1.5, dV0=400.)    
#make_mask(image='cube_canvas.image', inc=17.6, PA=242.0, mstar=1.7, dist=135.7, vlsr=7.12e3, z_func=z_func, nbeams=3.0, r_min=0.01, r_max = 1.6, dV0=400.)    

#make_mask(image='cube_canvas.image', inc=41.1, PA=324.0, mstar=2.0, dist=110.0, vlsr=5.65e3, z_func =z_func, nbeams=5.0, r_min=0.01, r_max = 3.5, dV0=500.)    

#make_mask(image='cube_canvas.image', inc=41.1, PA=324.0, mstar=2.0, dist=110.0, vlsr=5.65e3, z_func =z_func, nbeams=10.0, r_min=0.01, r_max = 3.5, dV0=800.)    

#make_mask(image='cube_canvas.image', inc=41.1, PA=324.0, mstar=2.0, dist=110.0, vlsr=5.65e3, z_func =z_func, nbeams=9.0, r_min=0.01, r_max = 4.0, dV0=600.)    

make_mask(image='cube_canvas.image', inc=41.1, PA=324.0, mstar=2.0, dist=110.0, vlsr=5.65e3, z_func =z_func, nbeams=11.0, r_min=0.01, r_max = 4.5, dV0=1000.)    

exportfits(imagename='cube_canvas.mask.image', fitsimage='cube_canvas.mask.image.fits',overwrite=True)

