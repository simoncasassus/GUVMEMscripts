#casa --log2term --nogui -c casarestore_4guvmem.py
import os

residual_ms = "_ph0_residuals.ms" #input
model_fits = "_ph0.fits"  # input 
restored = "restored"  #output
weight="briggs" # "briggs"
polarization="I" 
robustparam=0.3
print("Restoring with robustparam ",robustparam)

######################################################################
residual_image=residual_ms+"_"+str(robustparam)+".img"

os.system("rm -rf *.log *.last "+residual_image+".* mod_out convolved_mod_out convolved_mod_out.fits "+restored+" "+restored+".fits")

importfits(imagename="mod_out",fitsimage=model_fits)

shape = imhead(imagename="mod_out", mode="get", hdkey="shape")
pix_num = shape[0]
cdelt = imhead(imagename="mod_out", mode="get", hdkey="cdelt2")
cdelta = qa.convert(v=cdelt,outunit="arcsec")
cdeltd = qa.convert(v=cdelt,outunit="deg")
pix_size = str(cdelta['value'])+"arcsec"
#print( "pix_size",pix_size)
#print( "pix_num",pix_num)

#clean(vis=residual_ms, imagename=residual_image, mode='mfs', niter=0, stokes=polarization, weighting=weight, robust=float(robustparam),imsize=[pix_num,pix_num], cell=pix_size)

os.system("rm -rf "+residual_image+"*")
tclean(vis=residual_ms,
       imagename=residual_image,
       gridder='standard',
       veltype='radio',
       niter=0,  
       interactive=False,
       #savemodel='modelcolumn',
       specmode='mfs',
       cell=pix_size,
       imsize=[pix_num,pix_num],
       robust=float(robustparam),
       scales = [0,10,30,90], 
       cyclefactor=1,
       deconvolver='multiscale',
       weighting='briggs',
       datacolumn='data',
       nterms=1)
       #restoringbeam="",
       #threshold="0.0uJy"


exportfits(imagename=residual_image+".image", fitsimage=residual_image+".image.fits")

ia.open(infile=residual_image+".image")
rbeam=ia.restoringbeam()
ia.done()

bmaj = imhead(imagename=residual_image+".image", mode="get", hdkey="beammajor")
bmin = imhead(imagename=residual_image+".image", mode="get", hdkey="beamminor")
bpa  = imhead(imagename=residual_image+".image", mode="get", hdkey="beampa")

minor = qa.convert(v=bmin,outunit="deg")
pa    = qa.convert(v=bpa ,outunit="deg")


#DO NOT DELETE convert_factor = (pi/(4*log(2))) * major['value']* minor['value'] /  (cdeltd['value']**2)



ia.open(infile="mod_out")
ia.convolve2d(outfile="convolved_mod_out", axes=[0,1], type='gauss', major=bmaj, minor=bmin, pa=bpa)
ia.done()

exportfits(imagename="convolved_mod_out", fitsimage="convolved_mod_out.fits")
ia.open(infile="convolved_mod_out.fits")
ia.setrestoringbeam(beam=rbeam)
ia.done()

imagearr=["convolved_mod_out.fits",residual_image+".image.fits"]

#immath(imagename=imagearr,expr=" (IM0 * convert_factor  + IM1) ", outfile=restored)

immath(imagename=imagearr,expr=" (IM0   + IM1) ", outfile=restored)

exportfits(imagename=restored, fitsimage=restored+".fits",overwrite=True)

