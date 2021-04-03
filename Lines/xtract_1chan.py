#casa --log2term --nogui -c xtract_1chan.py 100
#casa --log2term --nogui -c xtract_1chan.py /data/simon/HD142_spirals/red/HD142527_12CO2-1_selfcal_origtbin_combinems_tav.ms '0,1' 0 99

import sys
import os

filenamems=sys.argv[1]
print( "xtract_1channel filenamems ",filenamems)
fields=sys.argv[2]
print( "xtract_1channel fields ",fields,"\n")
spws=sys.argv[3]
print( "xtract_1channel spws ",spws,"\n")
channel=sys.argv[4]
print( "xtract_1channel channel ",channel,"\n")
cellsizein=sys.argv[5]
print( "xtract_1channel cellsize ",cellsizein,"\n")
nxin=sys.argv[6]
print( "xtract_1channel nxin ",nxin,"\n")
nyin=sys.argv[7]
print( "xtract_1channel nyin ",nyin,"\n")
robustparam=sys.argv[8]
print( "xtract_1channel robustparam ",robustparam,"\n")
genclean=sys.argv[9]
print( "xtract_1channel genclean ",genclean,"\n")
genchannelms=sys.argv[10]
print( "xtract_1channel genchannelms ",genchannelms,"\n")


outputms='channel_'+str(channel)+'.ms'


print( "vis="+filenamems+", field="+fields+", outputvis="+outputms+"datacolumn='data',nchan=1, start=",channel,"\n")

#sys.exit()

if (float(genchannelms) > 0):

    os.system('rm -rf '+outputms)
    mstransform(vis=filenamems, field=fields, outputvis=outputms, spw=str(spws)+':'+str(channel),datacolumn='data') 




if float(genclean) > 0:
    listobs(vis=outputms,listfile='list_'+outputms+'.txt',overwrite=True)

    print( "dirty map for channel  ",channel,"\n")
    os.system('rm -rf clean_channel_'+str(channel)+'.*')
    #clean(vis=outputms,
    #      imagename='clean_channel_'+str(channel),
    #      mode='channel',
    #      niter=0,  
    #      interactive=False,
    #      cell=cellsizein,
    #      imsize=[int(nxin),int(nyin)],
    #      weighting='briggs')
    #

    tclean(vis=outputms,
           imagename='clean_channel_'+str(channel),
           gridder='standard',
           imsize=[int(nxin),int(nyin)],
           veltype='radio',
           niter=0,  
           interactive=False,
           #savemodel='modelcolumn',
           specmode='cube',
           cell=cellsizein,
           robust=float(robustparam),
           scales = [0,10,30,90], 
           cyclefactor=1,
           deconvolver='multiscale',
           weighting='briggs',
           nterms=1,
           #restoringbeam="",
           threshold="0.0uJy")



    exportfits(imagename='clean_channel_'+str(channel)+'.image',fitsimage='clean_channel_'+str(channel)+'.fits',overwrite=True);







