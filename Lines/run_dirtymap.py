import sys
import re
import os
print(sys.argv)
filenamems=sys.argv[1]
cellsizein=sys.argv[2]
nxin=sys.argv[3]
nyin=sys.argv[4]
spws=sys.argv[5]
robustparam=sys.argv[6]
FileCanvasCube=sys.argv[7]


print( "spws ",spws )
print( "filenamems",filenamems,"\n")

print( "cellsize ",cellsizein)
print( "nxin ",nxin)
print( "nyin ",nyin)
print( "robustparam ",robustparam)




print( "dirty map for >>",filenamems,"<<<")


listobs(vis=filenamems,listfile='list_'+os.path.basename(filenamems)+'.txt',overwrite=True)

FileCanvasCube_tag=re.sub('.fits','',FileCanvasCube)


#os.system('rm -rf '+FileCanvasCube_tag+'*')
os.system('rm -rf '+FileCanvasCube_tag+".psf")
os.system('rm -rf '+FileCanvasCube_tag+".sumwt")
os.system('rm -rf '+FileCanvasCube_tag+".pb")
os.system('rm -rf '+FileCanvasCube_tag+".residual")
os.system('rm -rf '+FileCanvasCube_tag+".model")
os.system('rm -rf '+FileCanvasCube_tag+".image")
os.system('rm -rf '+FileCanvasCube_tag+".fits")



#tclean(vis=prefix+'_COcube.ms.contsub',
#       imagename=imagename, specmode='cube', imsize=2000,
#       deconvolver='multiscale', start=chanstart, width=chanwidth, nchan=nchan,
#       outframe='LSRK', veltype='radio', restfreq='230.538GHz',
#       cell='0.013arcsec', scales = [0,10,30,90], niter=10000000,
#       weighting='briggs', robust=0.5, threshold='2mJy', interactive=False,
#       usemask='auto-thresh', maskthreshold=2.0, nterms=1, cycleniter=20000,
#       restoringbeam='common', pbcor=True)

tclean(vis=filenamems,
       imagename=FileCanvasCube_tag,
       gridder='standard',
       veltype='radio',
       #spw=spws,
       specmode='cube', 
       niter=0,  
       interactive=False,
       cell=cellsizein,
       imsize=[int(nxin),int(nyin)],
       robust=float(robustparam),
       deconvolver='hogbom',
       #restoringbeam='common',
       weighting='briggs',
       nterms=1)

exportfits(imagename=FileCanvasCube_tag+'.image',fitsimage=FileCanvasCube_tag+'.fits',overwrite=True)






