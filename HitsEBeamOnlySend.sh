#! /bin/bash
targetDESY="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/EPlusLaserBackgroundHitsAnalyzer/"
targetWIS="/storage/agrp/arkas/AnalyzeHitsEBeamOnly"
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
put TracksAndHitsAnalyzer/MHists.* $target
put TracksAndHitsAnalyzer/BkgTracksAndHitsAnalyzer/process_lxtrees_background_v2.C $target
put TracksAndHitsAnalyzer/BkgTracksAndHitsAnalyzer/ProcessLxSim.* $target
put TracksAndHitsAnalyzer/runHitEBeamOnly.sh $target
put lxmacro/runBKGMaster.sh $target/
put lxmacro/condorJobsMASTER.jdl $target/
put lxmacro/sendCondorJobs.py $target/

####
# put lxmacro/interactive.jdl $target/
# put TracksAndHitsAnalyzer/process_lxtrees_v2.C $target
# put TracksAndHitsAnalyzer/ProcessLxSim.* $target
# put TracksAndHitsAnalyzer/BkgTracksAndHitsAnalyzer/process_lxtrees_background.C $target
# put TracksAndHitsAnalyzer/BkgTracksAndHitsAnalyzer/QGSPList_EBeamOnly.txt $target
# put TracksAndHitsAnalyzer/getGoodBkgFiles.py $target
EOF
