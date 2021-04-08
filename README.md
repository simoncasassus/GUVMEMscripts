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






