#casa --log2term --nogui -c make_canvas.py  /data/simon/HD142_spirals/red/HD142527_12CO2-1_selfcal_origtbin_combinems_tav.ms '0,1' 0 99

import sys
import os

print(sys.argv)


sourcems=sys.argv[1]
print( "sourcems",sourcems)
#fields=sys.argv[4]
#spws=sys.argv[5] # not used

#channel=sys.argv[8]

cellsize=sys.argv[2]

nxin=sys.argv[3]
nyin=sys.argv[4]

robustparam=sys.argv[5]


listobs(sourcems,listfile='list_inputms.txt',overwrite=True)


print( "auto clean for: ",sourcems)
os.system('rm -rf autoclean.*')
tclean(vis=sourcems,
       imagename='autoclean',
       gridder='standard',
       specmode='mfs',
       niter=0,  
       interactive=False,
       cell=cellsize,
       deconvolver='hogbom',
       imsize=[int(nxin),int(nyin)],
       robust=float(robustparam),
       weighting='briggs')

exportfits(imagename='autoclean.image',fitsimage='autoclean.fits',overwrite=True);
exportfits(imagename='autoclean.residual',fitsimage='autoclean.residual.fits',overwrite=True);








