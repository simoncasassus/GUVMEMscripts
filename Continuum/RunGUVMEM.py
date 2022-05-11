import sys
import copy
import os
from astropy.io import fits 
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import re

load_path_4scripts = os.environ['HOME']+'/common/python/include/GUVMEMscripts/Continuum/'


def docanvas(sourcems, nxin, nyin, cellsize, robustparam, NoiseFromTcleanResiduals=False,ManualNoise=False,NoiseFactor=False):

    #fields='0'  # no los pesca 
    os.system('casa --log2term --nogui -c '+load_path_4scripts+'make_canvas.py'+' '+sourcems+' '+cellsize+' '+str(nxin)+' '+str(nyin)+' '+robustparam)

    
    data_canvas = fits.open('autoclean.fits')
    print( data_canvas.info())
    im_canvas = data_canvas[0].data
    him_canvas = data_canvas[0].header
    
    data_resids = fits.open('autoclean.residual.fits')
    im_resids = data_resids[0].data

    noise=np.std(im_resids)
    print( "noise from tclean residuals = ",noise)
    if ManualNoise:
        noise = ManualNoise
        print("using manual noise ",noise)
        him_canvas['NOISE'] = noise
    elif NoiseFromTcleanResiduals:
        him_canvas['NOISE'] = noise
        if NoiseFactor:
            him_canvas['NOISE'] = NoiseFactor*noise
            
    
    him_canvas['RADESYS'] = 'FK5' 
    him_canvas['EQUINOX'] = '2000' 
    
    os.system('rm mod_in_0.fits ')
    data_canvas.writeto('mod_in_0.fits')

    data_canvas[0].data = im_resids*0.
    data_canvas.writeto('alpha.fits',overwrite=True)


def exec_arun(sourcems, lbdaS=0.0, lbdaL=0.0, MINPIX=0., DoL1=False, Grid=False,  wAlpha=False,graphic_cards="-M 2,3,4,5", robustparam='2.0', PrintImages=False,PositivDefinit=True,MaxNiter=80,XtraNameTag='',nCores4Gridding=10,GridRobust=False, noisecut=2.,CheckMask=True,DoMask=False,UVtaper=False,DoGUVMEMRUN=True,DoRestore=True):
    prior = 0
    eta=-1.0
    if Grid:
        dogrid='-g '+str(nCores4Gridding)
        masterlabel="_lS"+str(lbdaS)+"_lL"+str(lbdaL)
        if GridRobust:
            dogrid +=' -R '+GridRobust
    else:
        dogrid=''
        masterlabel="_lS"+str(lbdaS)+"_lL"+str(lbdaL)+"_nogrid"

    if wAlpha:
        masterlabel+="_wAlpha"
        defaultvalues=str(MINPIX)+',3.0' 
        reffreq='-F 225E9' 
    else:
        defaultvalues=str(MINPIX)
        reffreq=''

    if PrintImages:
        printflag="--print-images "
    else:
        printflag=""

    if DoL1:
        sys.exit("recompile UVMEM for L1")
        path_to_guvmem='/home/simon/bin/gpuvmem_L1/bin/gpuvmem'
        masterlabel+="_L1"
    elif UVtaper:
        path_to_guvmem='/home/simon/bin/gpuvmem_uvtaper/bin/gpuvmem'
        masterlabel+="_uvtaper"
    else:
        path_to_guvmem='/home/simon/bin/gpuvmem-dev/gpuvmem/bin/gpuvmem'
        path_to_guvmem='/home/simon/bin/gpuvmem/bin/gpuvmem'

    if PositivDefinit:
        positivflag=''
    else:
        positivflag='--nopositivity'
        masterlabel+="_nopositiv"


    masterlabel+=XtraNameTag

    workdir="mem"+masterlabel

    if DoMask:
        maskname=DoMask
        workdir+="_masked"
        
    if DoGUVMEMRUN:
        os.system("rm -rf  "+workdir)
        os.system("mkdir "+workdir)
    
        command=path_to_guvmem+" -X 16 -Y 16 -V 256 "+dogrid+" -i "+sourcems+" -o "+workdir+"/out_res_ms --noise_cut "+str(noisecut)+" -m mod_in_0.fits -p "+workdir+"/ -O "+workdir+"/mod_out.fits "+graphic_cards+" -z "+defaultvalues+" -Z "+str(lbdaS)+","+str(lbdaL)+" -t "+str(MaxNiter)+" --verbose -e "+str(eta)+" "+reffreq+" "+positivflag+" "+printflag
        
        if DoMask:
            if CheckMask:
                print("checking that mask and canvas have same WCS")
                hdu_canvas=fits.open('mod_in_0.fits')
                hdr_canvas=hdu_canvas[0].header
                hdu_mask=fits.open(maskname)
                hdr_mask=hdu_mask[0].header
                if ( (np.fabs( (hdr_mask['CDELT2']-hdr_canvas['CDELT2'])/hdr_canvas['CDELT2']) < 1E-3) | (hdr_mask['NAXIS1'] != hdr_canvas['NAXIS1'])):
                    exec_maskresamp_script = Path(__file__).parent / "exec_mask_resamp.bash"
                    mask_basename=os.path.basename(maskname)
                    mask_basename=re.sub('.fits','_resamp.fits',mask_basename,re.IGNORECASE)
                    full_path_mask=os.path.join(os.path.dirname(maskname),mask_basename)
                    print("resampling input mask: ","bash "+str(exec_maskresamp_script)+" mod_in_0.fits"+" "+maskname+" "+full_path_mask)
                    os.system("bash "+str(exec_maskresamp_script)+" mod_in_0.fits"+" "+maskname+" "+full_path_mask)
                    maskname=full_path_mask

        if DoMask:
            command+=' -U '+maskname
        if UVtaper:
            command+=' --modify-weights '
        command += " \n"

        print("calling guvmem with command:")
        print(command)
        print("workdir:")
        print(workdir)


        f=open("exec_gpuvmem_command.bash","w+")
        #f.write("./a.out\n")
        #f.write("ulimit -v 250G \n")
        f.write(command)
        #f.write("ulimit -v unlimited\n")
        f.close()
        os.system("rsync -va exec_gpuvmem_command.bash "+workdir)
        os.system("bash  exec_gpuvmem_command.bash")

    if DoRestore:    
        os.system("bash "+load_path_4scripts+"exec_restore.bash "+workdir+" "+robustparam+" "+load_path_4scripts)

