# GUVMEMscripts

dependencies:
make sure to download the devel branch of  gpuvmem, and install it. 



Lines:

installation:
0- locate your python `include' directory, for me this is
INCLUDE=/home/simon/common/python/include
1- make a symlink to GUVMEMscipts in your PYTHON include path:
for me, this is:
ln -s /home/simon/gitcommon/GUVMEMscripts  $INCLUDE/GUVMEMscripts

2- Edit L19 in RunLineGUVMEM_pool.py:
load_path_4scripts = $INCLUDE/GUVMEMscripts/Lines/'

3- Edit L11 in master_line_pool.py
include_path= os.environ['HOME']+'/common/python/include/'
to
include_path= $INCLUDE


execute
python  master_line_pool.py






masks:

In ds9 use Regions->shape->ellipse, use shift + drag on corners of rectangle to rotate,  and save regions for each channel separatedly 

mv ds9.reg  ds9_1.reg
conda install -c conda-forge pyregion
python adjusts_masks_image.py
