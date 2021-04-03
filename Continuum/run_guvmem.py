import sys
import copy
import os
from astropy.io import fits 
import matplotlib.pyplot as plt
import numpy as np

import RunGUVMEM


print( "sys.argv",sys.argv)

sourcems =  '/home/simon/V4046Sgr/data/V4046Sgr_cont_self.ms'

cellsize='0.004arcsec'
nxin=2048
nyin=2048
nxin=4096
nyin=4096
nxin=1024
nyin=1024
#nxin=8192
#nyin=8192

robustparam='0.0'

#RunGUVMEM.docanvas(sourcems,nxin, nyin, cellsize,robustparam)

#######################################################################


#######################################################################


graphic_cards="-G 2,3,4,5"

# chi2

#RunGUVMEM.exec_arun(sourcems, lbdaS=0.0, lbdaL=0.0, MINPIX=0., DoL1=False, Grid=False,  wAlpha=False, graphic_cards=graphic_cards,PrintImages=True)

#RunGUVMEM.exec_arun(sourcems, lbdaS=0.0, lbdaL=0.0, MINPIX=0., DoL1=False, Grid=True,  wAlpha=False, graphic_cards=graphic_cards,PrintImages=False,robustparam='2.0',XtraNameTag='')

#RunGUVMEM.exec_arun(sourcems, lbdaS=0.0, lbdaL=0.0, MINPIX=0., DoL1=False, Grid=False,  wAlpha=False, graphic_cards=graphic_cards,PrintImages=False,robustparam='0.0',XtraNameTag='')


lbdaSs = (0.0001,0.001,0.005)
lbdaSs = (0.01,0.1,1.0)
lbdaLs = (0., ) 


#lbdaSs = (0.0001,0.001,0.01,0.1)
lbdaSs = (0.005,0.0075,0.01)


for lbdaS in lbdaSs:
    for lbdaL in lbdaLs:
        RunGUVMEM.exec_arun(sourcems, lbdaS=lbdaS, lbdaL=lbdaL, MINPIX=1E-3, DoL1=False, Grid=True,  wAlpha=False, graphic_cards=graphic_cards,PrintImages=False,robustparam=robustparam,GridRobust=robustparam)

lbdaSs = (0.05,0.07, 0.1, 0.15,0.2)

for lbdaS in lbdaSs:
    for lbdaL in lbdaLs:
        RunGUVMEM.exec_arun(sourcems, lbdaS=lbdaS, lbdaL=lbdaL, MINPIX=1E-3, DoL1=False, Grid=False,  wAlpha=False, graphic_cards=graphic_cards,PrintImages=False)


