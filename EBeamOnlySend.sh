#! /bin/bash
targetDESY="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/EPlusLaserBackgroundAnalyzer/FullSimImprovedShielding" #
targetWIS="/storage/agrp/arkas/AnalyzeElectronFiles"
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
put lxmacro/MHists.* $target/
put lxmacro/process_track_tree_draw_v6.C $target/
put lxmacro/process_track_tree_draw_v7.C $target/
put lxmacro/process_track_tree_draw_v8.C $target/
put lxmacro/process_track_tree_draw_v9.C $target/
put lxmacro/runLocalJobs.py $target/
# put lxmacro/EBeamOnly.txt $target/
# put lxmacro/EBeamOnlyWIS.txt $target/
# put lxmacro/EBeamOnlyWISFull.txt $target/
# put lxmacro/EBeamOnlyWISPartial.txt $target/
put seedingAlgorithm/getBXForEBeamOnly.py $target/
# put lxmacro/*DividedByBX*txt $target/
put lxmacro/condorJobsMASTER.jdl $target/
put lxmacro/runBKGMaster.sh $target/
put lxmacro/interactive.jdl $target/
put lxmacro/runEBeamOnly.sh $target/
put lxmacro/sendCondorJobs.py $target/
put TracksAndHitsAnalyzer/BkgTracksAndHitsAnalyzer/ProcessLxSim.C $target
put TracksAndHitsAnalyzer/BkgTracksAndHitsAnalyzer/ProcessLxSim.h $target
EOF
