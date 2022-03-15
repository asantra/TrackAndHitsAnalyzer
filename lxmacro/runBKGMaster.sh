#! /bin/bash

SECONDS=0


########For debug purposes:

# if [[ -d  ~/tmpdebug/ ]]
# then
#     echo "~/tmpdebug/ exists on your filesystem."
#     rm -rf  ~/tmpdebug/
#     mkdir  ~/tmpdebug/
# else
#     mkdir  ~/tmpdebug/
# fi
# 
# 
# ls -ltr  >> ~/tmpdebug/log
# env >> ~/tmpdebug/log
# pwd >> ~/tmpdebug/log
# echo $LD_LIBRARY_PATH >> ~/tmpdebug/log

########Copy input files:
cp TTTT/WWWW .
cp TTTT/MHists.C .
cp TTTT/MHists.h .
# #### for Hits and Tracks analyzer
cp TTTT/ProcessLxSim.C .
cp TTTT/ProcessLxSim.h .


ln -s /usr/lib64/libXpm.so.4 libXpm.so.4
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD

# For Tracks tree:
echo "e+laser background samples"
root -l -b -q WWWW\(\"RRRR\",\"CCCC\",\"OOOO\"\)
#mv XXXX /nfs/dust/luxe/user/santraar/TextSamples_October2021
#mv YYYY /nfs/dust/luxe/user/santraar/TextSamples_October2021
duration=$SECONDS
echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
