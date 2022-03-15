#! /bin/bash

#targetDESY="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/GPlusLaserSignalAndBackgroundAnalyzer"
#targetDESY="/nfs/dust/luxe/group/MCProduction/user/santraar/"
targetDESY="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/GPlusLaserBackgroundAnalyzer"
targetWIS="/storage/agrp/arkas/AnalyzeBackgroundFiles"
serverNameDESY="santraar@naf-luxe.desy.de"
serverNameWIS="arkas@wipp-an1"
if [[ $1 == "W" ]]
then
   target=$targetWIS
   serverName=$serverNameWIS
else
   target=$targetDESY
   serverName=$serverNameDESY
fi

sftp $serverName << EOF
put lxmacro/MHists.* $target
put lxmacro/runGLaser.sh $target
put lxmacro/process_track_tree_draw_v8.C $target


#put lxmacro/process_track_tree_draw_v5.C $target
#put lxmacro/process_hits_tree_draw_v5.C $target
#put lxmacro/process_hits_tree_draw_v6.C $target
#put lxmacro/process_track_tree_draw_v3.C $target
#put lxmacro/process_track_tree_draw_v4.C $target
#put lxmacro/process_track_tree_draw_v6.C $target
#put lxmacro/process_track_tree_draw_v7.C $target
#put lxmacro/runLocalJobs.py $target
#put lxmacro/bxForGLaser.py $target
#put lxmacro/gPlusLaser.txt $target
#put lxmacro/gPlusLaserWIS.txt $target
#put lxmacro/condorJobsMASTER.jdl $target
#put lxmacro/interactive.jdl $target
#put lxmacro/runBKGMaster.sh $target
#put lxmacro/sendCondorJobs.py $target
#put seedingAlgorithm/getBXForEBeamOnly.py $target
EOF
