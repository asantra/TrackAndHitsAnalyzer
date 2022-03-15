#! /bin/bash


SECONDS=0

filename=""

if [[ $1 == "W" ]]
then
    filename="gPlusLaserWIS.txt"
else
#    filename="gPlusLaser.txt"
#     filename="/nfs/dust/luxe/user/oborysov/hics_list/list_root_bppp_background_fast_0508546b_0_5.txt"
    filename="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/GPlusLaserBackgroundHitsAnalyzer/excessBX2File.txt"
fi

# # For Tracks tree:
# echo "photon+laser background samples"
# root -l -b -q process_track_tree_draw_v5.C\(\"${filename}\"\)
# duration=$SECONDS
# echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
# 
# exit 1
#### hits tree
SECONDS=0
echo "photon+laser background samples"
# root -l -b -q process_lxtrees_v2.C\(\"${filename}\"\)
# root -l -b -q process_lxtrees_background_v2.C\(\"${filename}\"\,\"2\", \"gPlusLaser_list_root_55ae8938_DividedByBX2A\")
counter=0
increment=1
while IFS= read -r line
do
  counter=$(( $counter + $increment ))
  echo "$line  $counter"
  echo "$line">oneFileName.txt
  root -l -b -q process_lxtrees_background_v2.C\(\"oneFileName.txt\",\"2\",\"gPlusLaser_list_root_55ae8938_DividedByBX2A\"\)
  if [[ $counter == "12" ]]
  then 
    break
  fi
#   bash eachFileRun.sh oneFileName.txt $counter
done < "$filename"

duration=$SECONDS
echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
