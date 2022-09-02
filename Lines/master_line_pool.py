import sys
import copy
import os
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
#from pylab import *
import matplotlib.colors as colors

include_path = os.environ['HOME'] + '/common/python/include/'
sys.path.append(include_path)

from GUVMEMscripts.Lines import RunLineGUVMEM_pool

sourcems = '/home/simon/HD100546_full_OOself/LB19/HD100546_SB17_IB17_LB19_12CO.ms'

cellsize = '0.004arcsec'
nxin = 4096
nyin = 4096

robustparam = '2.0'  # for restore
robustparam = '1.0'  # for restore

nchan1 = 0
nchan2 = -1

MasterInit = False

#lbdaS = 5E-4
lbdaS = 0.00032  # 10**(-3.5)
#lbdaS = 0.0001 # 10**(-3.5)
#lbdaS = 0.

RunLineGUVMEM_pool.exec_cuberun(
    sourcems,
    cellsize,
    nxin,
    nyin,
    spws='0',
    MakeCanvasCube=MasterInit,
    FileCanvasCube='cube_canvas.fits',
    lbdaS=lbdaS,
    lbdaL=0.0,
    #MINPIX=0., # 1E-3,
    MINPIX=1E-4,  #0., # 1E-3,
    #MINPIX=1E-5, # 1E-3
    DoL1=False,
    Grid=False,
    MaxNiter=30,
    XtraNameTag='_maskedb',
    nchan1=nchan1,
    nchan2=nchan2,
    manual_noise=4E-3,  # theor noise is 4.5E-4
    datacolumn='corrected',
    Extract_Channel=MasterInit,
    Gen_ImageCanvas=MasterInit,
    robustparam=robustparam,
    cards=['0'],
    PrintImages=False,
    noisecut=1.,
    DoGUVMEMRUN=False,
    DoRestore=True,
    # listchannels=[42],
    DoMask=True)  #,manual_noise=1.

sys.exit()

RunLineGUVMEM_pool.exec_cuberun(sourcems,
                                cellsize,
                                nxin,
                                nyin,
                                spws='0',
                                MakeCanvasCube=MasterInit,
                                FileCanvasCube='cube_canvas.fits',
                                lbdaS=1e-3,
                                lbdaL=0.0,
                                MINPIX=1e-3,
                                DoL1=False,
                                Grid=False,
                                MaxNiter=80,
                                XtraNameTag='_kepmask_dV0500_adjust3',
                                nchan1=nchan1,
                                nchan2=nchan2,
                                Extract_Channel=False,
                                Gen_ImageCanvas=MasterInit,
                                robustparam=robustparam,
                                cards=['0', '1', '2', '3', '4', '5'],
                                PrintImages=False,
                                noisecut=1.,
                                DoGUVMEMRUN=False,
                                DoMask=True,
                                DoRestore=True,
                                UVtaper=False)

#RunLineGUVMEM_pool.exec_cuberun(sourcems, cellsize,nxin,nyin, spws='0', MakeCanvasCube=MasterInit, FileCanvasCube='cube_canvas.fits', lbdaS=1e-3, lbdaL=0.0, MINPIX=1e-3, DoL1=False, Grid=False, MaxNiter=80,XtraNameTag='_kepmask_dV0600',fields='0',nchan1=nchan1,nchan2=nchan2,Extract_Channel=False,Gen_ImageCanvas=MasterInit,robustparam=robustparam,cards=['0','1','2','3','4','5'],PrintImages=False,noisecut=1.,DoGUVMEMRUN=True,DoMask=True,DoRestore=True,UVtaper=False)

####python get_individual_masks.py cube_canvas.mask.image_dV0800.fits
#robustparam='2.0' # for restore
#RunLineGUVMEM_pool.exec_cuberun(sourcems, cellsize,nxin,nyin, spws='0', MakeCanvasCube=MasterInit, FileCanvasCube='cube_canvas.fits', lbdaS=1e-3, lbdaL=0.0, MINPIX=1e-3, DoL1=False, Grid=False, MaxNiter=80,XtraNameTag='_kepmask_dV0800_B',fields='0',nchan1=nchan1,nchan2=nchan2,Extract_Channel=False,Gen_ImageCanvas=MasterInit,robustparam=robustparam,cards=['0','1','2','3','4','5'],PrintImages=False,noisecut=1.,DoGUVMEMRUN=True,DoMask=True,DoRestore=True,UVtaper=False)

#robustparam='1.0' # for restore
#RunLineGUVMEM_pool.exec_cuberun(sourcems, cellsize,nxin,nyin, spws='0', MakeCanvasCube=MasterInit, FileCanvasCube='cube_canvas.fits', lbdaS=1e-3, lbdaL=0.0, MINPIX=1e-3, DoL1=False, Grid=False, MaxNiter=80,XtraNameTag='_kepmask_dV0800_B',fields='0',nchan1=nchan1,nchan2=nchan2,Extract_Channel=False,Gen_ImageCanvas=MasterInit,robustparam=robustparam,cards=['0','1','2','3','4','5'],PrintImages=False,noisecut=1.,DoGUVMEMRUN=False,DoMask=True,DoRestore=True,UVtaper=False)

####python get_individual_masks.py cube_canvas.mask.image_dV0800.fits
robustparam = '2.0'  # for restore
RunLineGUVMEM_pool.exec_cuberun(sourcems,
                                cellsize,
                                nxin,
                                nyin,
                                spws='0',
                                MakeCanvasCube=MasterInit,
                                FileCanvasCube='cube_canvas.fits',
                                lbdaS=1e-3,
                                lbdaL=0.0,
                                MINPIX=1e-3,
                                DoL1=False,
                                Grid=False,
                                MaxNiter=80,
                                XtraNameTag='_kepmask_dV0500_adjust3',
                                nchan1=nchan1,
                                nchan2=nchan2,
                                Extract_Channel=False,
                                Gen_ImageCanvas=MasterInit,
                                robustparam=robustparam,
                                cards=['0', '1', '2', '3', '4', '5'],
                                PrintImages=False,
                                noisecut=1.,
                                DoGUVMEMRUN=True,
                                DoMask=True,
                                DoRestore=True,
                                UVtaper=False)

robustparam = '1.0'  # for restore
RunLineGUVMEM_pool.exec_cuberun(sourcems,
                                cellsize,
                                nxin,
                                nyin,
                                spws='0',
                                MakeCanvasCube=MasterInit,
                                FileCanvasCube='cube_canvas.fits',
                                lbdaS=1e-3,
                                lbdaL=0.0,
                                MINPIX=1e-3,
                                DoL1=False,
                                Grid=False,
                                MaxNiter=80,
                                XtraNameTag='_kepmask_dV0500_adjust3',
                                nchan1=nchan1,
                                nchan2=nchan2,
                                Extract_Channel=False,
                                Gen_ImageCanvas=MasterInit,
                                robustparam=robustparam,
                                cards=['0', '1', '2', '3', '4', '5'],
                                PrintImages=False,
                                noisecut=1.,
                                DoGUVMEMRUN=False,
                                DoMask=True,
                                DoRestore=True,
                                UVtaper=False)
