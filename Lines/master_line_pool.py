import sys
import copy
import os
from astropy.io import fits 
import matplotlib.pyplot as plt
import numpy as np
#from pylab import *
import matplotlib.colors as colors


include_path=os.environ['HOME']+'/common/python/include/'
sys.path.append(include_path)

from GUVMEMscripts.Lines import RunLineGUVMEM_pool



sourcems ='/path/to/12CO3-2.ms'

cellsize='0.02arcsec' 
nxin=512
nyin=512

robustparam='2.0' # for restore

nchan1=0
nchan2=-1


MasterInit=True
lbdaS=0.
RunLineGUVMEM_pool.exec_cuberun(sourcems, cellsize,nxin,nyin, spws='0', MakeCanvasCube=MasterInit, FileCanvasCube='cube_canvas.fits', lbdaS=lbdaS, lbdaL=0.0, MINPIX=0., DoL1=False, Grid=False, MaxNiter=80,XtraNameTag='',fields='0',nchan1=nchan1,nchan2=nchan2,Extract_Channel=True,Gen_ImageCanvas=MasterInit,robustparam=robustparam,cards=['0','1','2','3','4','5'],PrintImages=False,noisecut=1.2,DoGUVMEMRUN=False,DoMask=False,DoRestore=True,UVtaper=False)


MasterInit=False
lbdaS=1E-3
RunLineGUVMEM_pool.exec_cuberun(sourcems, cellsize,nxin,nyin, spws='0', MakeCanvasCube=MasterInit, FileCanvasCube='cube_canvas.fits', lbdaS=lbdaS, lbdaL=0.0, MINPIX=1E-3, DoL1=False, Grid=False, MaxNiter=80,XtraNameTag='_Kepmask',fields='0',nchan1=nchan1,nchan2=nchan2,Extract_Channel=False,Gen_ImageCanvas=MasterInit,robustparam=robustparam,cards=['0','1','2','3','4','5'],PrintImages=False,noisecut=1.2,DoGUVMEMRUN=True,DoMask=False,DoRestore=True,UVtaper=False)



