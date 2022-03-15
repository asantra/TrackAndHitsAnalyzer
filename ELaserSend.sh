#! /bin/bash
targetDESY="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/EPlusLaserSignalAndBackgroundAnalyzer"
targetWIS="/storage/agrp/arkas/AnalyzeHicsFiles"
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
put lxmacro/process_track_tree_draw_v9.C $target/
put lxmacro/runELaser.sh $target/
#### These are not needed for now
#put lxmacro/process_track_tree_draw_v3.C $target/
#put lxmacro/process_hits_tree_draw_v3.C $target/
#put lxmacro/process_hits_tree_draw_v4.C $target/
#put lxmacro/eachFileRun.sh $target/
#put lxmacro/interactive.jdl $target/
#put lxmacro/list_root_hics_165gev_w0_3000nm_WIS.txt $target/
#put lxmacro/separateOutBX.py $target/
EOF
