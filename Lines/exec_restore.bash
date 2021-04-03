workdir=$1
robustparam=$2
load_path_4scripts=$3

echo $workdir
echo "RUNNING RESTORE"

rsync -va $load_path_4scripts/casarestore_4guvmem.py $workdir 
cd $workdir
#casa --log2term --nogui -c casarestore_4guvmem.py  $robustparam
casa  --nogui -c casarestore_4guvmem.py  $robustparam
cd ../









