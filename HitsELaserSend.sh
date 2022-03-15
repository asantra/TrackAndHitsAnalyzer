#! /bin/bash
targetDESY="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/EPlusLaserSignalAndBackgroundHitsAnalyzer"
targetWIS="/storage/agrp/arkas/AnalyzeHitsElectron"
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
put TracksAndHitsAnalyzer/process_lxtrees_v2.C $target
put TracksAndHitsAnalyzer/process_lxtrees_v4.C $target
put TracksAndHitsAnalyzer/process_lxtrees_v5.C $target
put TracksAndHitsAnalyzer/process_lxtrees_v6.C $target
put TracksAndHitsAnalyzer/BkgTracksAndHitsAnalyzer/ProcessLxSim.C $target
put TracksAndHitsAnalyzer/BkgTracksAndHitsAnalyzer/ProcessLxSim.h $target
put lxmacro/runBKGMaster.sh $target/
put lxmacro/condorJobsMASTER.jdl $target/
put lxmacro/sendCondorJobs.py $target/
put TracksAndHitsAnalyzer/runHitELaser.sh $target
put TracksAndHitsAnalyzer/eachFileRun.sh $target
EOF
