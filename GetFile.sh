#! /bin/bash
targetDESY="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/GEANT4_LUXE_Analyzer"
targetBKG="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/BackgroundAnalyzer"
targetElectron="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/ElectronAnalyzer"
targetELaserW="/storage/agrp/arkas/AnalyzeHicsFiles"
targetBKGW="/storage/agrp/arkas/AnalyzeBackgroundFiles"
targetElectronW="/storage/agrp/arkas/AnalyzeElectronFiles"
serverNameDESY="santraar@naf-luxe.desy.de"
serverNameWIS="arkas@wipp-an1"

if [[ $1 == "ELaserW" ]]
then
   target=$targetELaserW
   servername=$serverNameWIS
elif [[ $1 == "ELaser" ]]
then
   target=$targetDESY
   servername=$serverNameDESY
elif [[ $1 == "EBeamOnlyW" ]]
then
   target=$targetElectronW
   servername=$serverNameWIS
elif [[ $1 == "EBeamOnly" ]]
then
   target=$targetElectron
   servername=$serverNameDESY
elif [[ $1 == "GLaserW" ]]
then
   target=$targetBKGW
   servername=$serverNameWIS
elif [[ $1 == "GLaser" ]]
then
   target=$targetBKG
   servername=$serverNameDESY
else
   target=$targetBKG
   servername=$serverNameWIS
fi

echo "The target directory "$target
sftp $servername << EOF
get $target/*root OutputFile/ 
#get $target/*trackInfoClean.txt seedingAlgorithm/ 
EOF
