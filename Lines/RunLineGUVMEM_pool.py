import sys
import copy
import os
import subprocess
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
#from pylab import *
import matplotlib.colors as colors

from pprint import pprint
from copy import deepcopy

from multiprocessing import Pool
#from tqdm import tqdm

load_path_4scripts = os.environ[
    'HOME'] + '/common/python/include/GUVMEMscripts/Lines/'


def store_outputcube(datacube,
                     hdu_canvas,
                     VectorBeam,
                     beamdata,
                     masterlabel,
                     tagfileout='model_cube'):
    hdu_out = deepcopy(hdu_canvas)
    hdu_out[0].data = datacube
    if VectorBeam:
        hdu_out[1].data = beamdata
        bmaj = beamdata[0][0] / 3600.
        bmin = beamdata[0][1] / 3600.
        bpa = beamdata[0][2] / 3600.
        hdu_out[0].header['BMAJ'] = bmaj
        hdu_out[0].header['BMIN'] = bmin
        hdu_out[0].header['BPA'] = bpa
    else:
        hdu_out[0].header['BMAJ'] = beamdata[0]
        hdu_out[0].header['BMIN'] = beamdata[1]
        hdu_out[0].header['BPA'] = beamdata[2]

    hdu_out.writeto(tagfileout + masterlabel + '.fits', overwrite=True)
    return


def execute_1chan(atask):
    print(">>>>>>>>>>> execute_1chan")
    #pprint(atask)

    ichan = atask['ichan']
    card = atask['card']
    masterlabel = atask['masterlabel']
    Extract_Channel = atask['options']['Extract_Channel']
    fields = atask['options']['fields']
    spws = atask['options']['spws']
    cellsize = atask['options']['cellsize']
    nxin = atask['options']['nxin']
    nyin = atask['options']['nyin']
    robustparam = atask['options']['robustparam']
    Grid = atask['options']['Grid']
    MINPIX = atask['options']['MINPIX']
    MaxNiter = atask['options']['MaxNiter']
    lbdaS = atask['options']['lbdaS']
    lbdaL = atask['options']['lbdaL']
    PrintImages = atask['options']['PrintImages']
    DoL1 = atask['options']['DoL1']
    PositivDefinit = atask['options']['PositivDefinit']
    DoGUVMEMRUN = atask['options']['DoGUVMEMRUN']
    DoRestore = atask['options']['DoRestore']
    noisecut = atask['options']['noisecut']
    DoMask = atask['options']['DoMask']
    UVtaper = atask['options']['UVtaper']
    manual_noise = atask['options']['manual_noise']
    prior = 0
    eta = -1.0

    if Grid:
        dogrid = '-g 10'
    else:
        dogrid = ''

    if manual_noise is not None:
        manual_noisetag = '-n ' + str(manual_noise)
    else:
        manual_noisetag = ''

    if PrintImages:
        printflag = "--print-images "
    else:
        printflag = ""

    Dev = False
    if UVtaper:
        path_to_guvmem = '/home/simon/bin/gpuvmem-dev_uvtaper/gpuvmem/bin/gpuvmem'
    elif Dev:
        path_to_guvmem = '/home/simon/bin/gpuvmem-dev/gpuvmem/bin/gpuvmem'
    else:
        if DoL1:
            path_to_guvmem = '/home/simon/bin/gpuvmem_L1/bin/gpuvmem'
        else:
            path_to_guvmem = '/home/simon/bin/gpuvmem/bin/gpuvmem'

    if PositivDefinit:
        positivflag = ''
    else:
        positivflag = '--nopositivity'

    workdir = "mem" + masterlabel + "_chan" + str(ichan)

    if DoGUVMEMRUN:
        os.system("rm -rf " + workdir)
        os.system("mkdir " + workdir)

    graphic_card = "-G " + card

    channelms = 'channel_' + str(ichan) + '.ms'

    if DoMask:
        maskname = 'mask_channel_' + str(ichan) + '.fits'

    if DoGUVMEMRUN:
        command = path_to_guvmem + "  -X 16 -Y 16 -V 256 " + dogrid + " -i " + channelms + " -o " + workdir + "/out_res_ms --noise_cut " + str(
            noisecut
        ) + " -m mod_in_0.fits -p " + workdir + "/ -O " + workdir + "/mod_out.fits  " + manual_noisetag + " " + graphic_card + " -z " + str(
            MINPIX) + " -Z " + str(lbdaS) + "," + str(lbdaL) + " -t " + str(
                MaxNiter) + " --verbose -e " + str(
                    eta) + " " + positivflag + " " + printflag
        if DoMask:
            command += ' -U ' + maskname
        if UVtaper:
            command += ' --modify-weights '

        command += " \n"

        print("calling guvmem with command:")
        print(command)
        executable = "exec_gpuvmem_command_s" + card + ".bash"
        f = open(executable, "w+")
        f.write(command)
        f.close()
        #os.system("singularity exec --nv  /home/simon/bin/container.simg   bash  "+executable)
        os.system("bash  " + executable)
        #Completed=subprocess.run(["bash",executable])
        #if (Completed['returncode']<0):
        #    print("GPUVMEM RUN FAILED", Completed['returncode'])
        #    print(Completed)
        #    pprint(astak)
        #    passresult=False
        #    return passresult
        #else:
        #    os.system('rsync -va mod_in_0.fits '+workdir)

    if DoRestore:
        os.system("bash " + load_path_4scripts + "exec_restore.bash " +
                  workdir + " " + robustparam + " " + load_path_4scripts)

    mod_out_hdu = fits.open(workdir + '/mod_out.fits')
    mod_out_im = mod_out_hdu[0].data

    restored_hdu = fits.open(workdir + '/restored.fits')
    restored_im = restored_hdu[0].data

    residual_hdu = fits.open(workdir + '/out_res_ms.img.image.fits')
    residual_im = residual_hdu[0].data
    residual_h = residual_hdu[0].header

    bmaj = residual_h['BMAJ'] * 3600.
    bmin = residual_h['BMIN'] * 3600.
    bpa = residual_h['BPA']
    beam = [bmaj, bmin, bpa]

    passresult = [ichan, mod_out_im, restored_im, residual_im, beam]
    return passresult


def exec_cuberun(sourcems,
                 cellsize,
                 nxin,
                 nyin,
                 lbdaS=0.0,
                 lbdaL=0.0,
                 MakeCanvasCube=True,
                 FileCanvasCube='cube_canvas.fits',
                 MINPIX=0.,
                 DoL1=False,
                 Grid=False,
                 PrintImages=False,
                 PositivDefinit=True,
                 MaxNiter=80,
                 XtraNameTag='',
                 spws='0',
                 fields='0',
                 nchan1=0,
                 nchan2=-1,
                 Extract_Channel=True,
                 Gen_ImageCanvas=True,
                 CleanUpChannels=False,
                 CleanUp=False,
                 DoGUVMEMRUN=True,
                 DoRestore=True,
                 robustparam='1.0',
                 cards=['0', '1', '2', '3', '4', '5'],
                 noisecut=2.,
                 manual_noise=None,
                 DoMask=False,
                 UVtaper=False):

    # Extract_Channel=False can save time if already extracted
    # CleanUpChannels=True saves disk space, but cannot try  other restoring beams
    # CleanUp=True removes all channel runs

    # first do a dirty map to define canvas
    if MakeCanvasCube:
        command = 'casa --log2term --nogui -c ' + load_path_4scripts + 'run_dirtymap.py' + ' ' + sourcems + ' ' + cellsize + ' ' + str(
            nxin) + ' ' + str(nyin) + ' ' + str(
                spws) + ' ' + robustparam + ' ' + FileCanvasCube
        print("building canvas cube with command: ", command)
        os.system(command)

    if DoL1:
        MINPIX = 0.

    hdu_canvas = fits.open(FileCanvasCube)
    cube_canvas = hdu_canvas[0].data
    h_canvas = hdu_canvas[0].header
    nchans = cube_canvas.shape[1]

    VectorBeam = False
    if (len(hdu_canvas) > 1):
        print("no beam info, look for extra HDU")
        beamhdr = hdu_canvas[1].header
        beamdata = hdu_canvas[1].data
        VectorBeam = True
        bmaj = beamdata[0][0]
        bmin = beamdata[0][1]
        bpa = beamdata[0][2]
    else:
        bmaj = h_canvas['BMAJ']
        bmin = h_canvas['BMIN']
        bpa = h_canvas['BPA']
        beamdata = [bmaj, bmin, bpa]

    print("nchans: ", nchans)

    if (nchan2 < 0):
        nchan2 = nchans - 1  # 0-offset last channel number

    # nchan1=22
    # nchan2=28

    cube_model = np.zeros_like(cube_canvas)
    cube_restored = np.zeros(cube_canvas.shape)
    cube_residuals = np.zeros(cube_canvas.shape)

    if Extract_Channel:
        #for ichan in (nchan1,nchan2):
        for ichan in range(nchan1, nchan2 + 1):
            print("ichan " + str(ichan))
            channelms = 'channel_' + str(ichan) + '.ms'
            genchannelms = 1
            genclean = 0
            os.system('casa --log2term --nogui -c ' + load_path_4scripts +
                      'xtract_1chan.py' + ' ' + sourcems + ' ' + fields + ' ' +
                      str(spws) + ' ' + str(ichan) + ' ' + cellsize + ' ' +
                      str(nxin) + ' ' + str(nyin) + ' ' + robustparam + ' ' +
                      str(genclean) + ' ' + str(genchannelms))

    if Gen_ImageCanvas:
        for ichan in (nchan1, nchan2):
            genchannelms = 0
            genclean = 1
            os.system('casa --log2term --nogui -c ' + load_path_4scripts +
                      'xtract_1chan.py' + ' ' + sourcems + ' ' + fields + ' ' +
                      str(spws) + ' ' + str(ichan) + ' ' + cellsize + ' ' +
                      str(nxin) + ' ' + str(nyin) + ' ' + robustparam + ' ' +
                      str(genclean) + ' ' + str(genchannelms))

            data_canvas_1chan = fits.open('clean_channel_' + str(ichan) +
                                          '.fits')
            # print data_canvas_1chan.info()
            im_canvas_1chan = data_canvas_1chan[0].data
            him_canvas_1chan = data_canvas_1chan[0].header
            # print im_canvas_1chan.shape

            hdu = fits.PrimaryHDU(im_canvas_1chan)
            #him_canvas_1chan['NOISE'] = 0.01
            him_canvas_1chan['RADESYS'] = 'FK5'
            him_canvas_1chan['EQUINOX'] = 2000.
            hdu.header = him_canvas_1chan

            os.system('rm mod_in_0.fits ')
            hdu.writeto('mod_in_0.fits')
            hdu.data = im_canvas_1chan * 0.
            hdu.writeto('alpha.fits', overwrite=True)

    if Grid:
        masterlabel = "_lS" + str(lbdaS) + "_lL" + str(lbdaL)
    else:
        masterlabel = "_lS" + str(lbdaS) + "_lL" + str(lbdaL) + "_nogrid"

    if DoL1:
        masterlabel += "_L1"

    if not PositivDefinit:
        masterlabel += "_nopositiv"

    masterlabel += XtraNameTag

    mastertasks = {
        'sourcems': sourcems,
        'masterlabel': masterlabel,
        'options': {
            'Extract_Channel': Extract_Channel,
            'fields': fields,
            'spws': spws,
            'cellsize': cellsize,
            'nxin': nxin,
            'nyin': nyin,
            'robustparam': robustparam,
            'Grid': Grid,
            'MINPIX': MINPIX,
            'MaxNiter': MaxNiter,
            'lbdaS': lbdaS,
            'lbdaL': lbdaL,
            'PrintImages': PrintImages,
            'DoL1': DoL1,
            'PositivDefinit': PositivDefinit,
            'DoGUVMEMRUN': DoGUVMEMRUN,
            'manual_noise': manual_noise,
            'DoMask': DoMask,
            'UVtaper': UVtaper,
            'DoRestore': DoRestore,
            'noisecut': noisecut
        }
    }

    ncards = len(cards)
    nchannels = nchan2 - nchan1 + 1
    if (nchannels < ncards):
        ncards = nchannels

    nbatches = int(nchannels / ncards)
    remainder = nchannels % ncards
    batches = []
    for ibatch in list(range(nbatches)):
        batches.append({
            'ichan_start': ibatch * ncards + nchan1,
            'ncards': ncards
        })

    if (remainder > 0):
        print("THERE IS A REMAINDER:", remainder)
        batches.append({
            'ichan_start': nbatches * ncards + nchan1,
            'ncards': remainder
        })

    print("BATCHES")
    pprint(batches)

    for abatch in batches:
        ichan_start = abatch['ichan_start']
        ncards = abatch['ncards']
        tasks = []
        for icard in list(range(ncards)):
            atask = deepcopy(mastertasks)
            atask['ichan'] = ichan_start + icard
            print("icard", icard, "ncards", ncards)
            atask['card'] = cards[icard]

            tasks.append(atask)

        with Pool(ncards) as pool:
            #passpoolresults = list(tqdm(pool.imap(execute_1chan, tasks), total=len(tasks)))
            passpoolresults = list(pool.imap(execute_1chan, tasks))
            pool.close()
            pool.join()
            print('Done whole pool')

        for acardresult in passpoolresults:
            if not acardresult:
                continue
            ichan = acardresult[0]
            mod_out_im = acardresult[1]
            restored_im = acardresult[2]
            residual_im = acardresult[3]
            beam = acardresult[4]
            cube_model[0, ichan, :, :] = mod_out_im
            cube_restored[0, ichan, :, :] = restored_im
            cube_residuals[0, ichan, :, :] = residual_im
            if VectorBeam:
                beamdata[ichan][0] = beam[0]
                beamdata[ichan][1] = beam[1]
                beamdata[ichan][2] = beam[2]
            else:
                beamdata[0] = beam[0] / 3600.
                beamdata[1] = beam[1] / 3600.
                beamdata[2] = beam[2] / 3600.

    #hdu_model = fits.PrimaryHDU(cube_model)
    #hdu_model.header=h_canvas
    #hdu_model.writeto('model_cube'+masterlabel+'.fits',overwrite=True)
    #hdu_model.writeto('model_cube'+masterlabel+'.fits',overwrite=True)
    #hdu_restored = fits.PrimaryHDU(cube_restored)
    #hdu_restored.header = h_canvas
    #hdu_restored.writeto('restored_cube'+masterlabel+'.fits',overwrite=True)
    #hdu_residual = fits.PrimaryHDU(cube_residuals)
    #hdu_residual.header = h_canvas
    #hdu_residual.writeto('residual_cube'+masterlabel+'.fits',overwrite=True)

    store_outputcube(cube_model,
                     hdu_canvas,
                     VectorBeam,
                     beamdata,
                     masterlabel,
                     tagfileout='model_cube')

    masterlabel += '_robust' + str(robustparam)

    store_outputcube(cube_restored,
                     hdu_canvas,
                     VectorBeam,
                     beamdata,
                     masterlabel,
                     tagfileout='restored_cube')
    store_outputcube(cube_residuals,
                     hdu_canvas,
                     VectorBeam,
                     beamdata,
                     masterlabel,
                     tagfileout='residual_cube')

    if CleanUpChannels:
        os.system("rm -rf clean_channel*")
        os.system("rm -rf channel_*")

    if CleanUp:
        os.system("rm -rf mem_lS*")
        os.system("rm -rf casa-*.log")
