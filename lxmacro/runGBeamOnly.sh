#! /bin/bash

# For Tracks tree:
echo "g+laser electron only samples"


### 2021 g+laser bkg files
filename="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/GPlusLaserBackgroundAnalyzer/gPlusLaser_list_txt_55ae8938_First1p22BX.txt"



#### this block is to read one line of a list at a time
echo "background g+laser"
counter=0
increment=1

while IFS= read -r line
do
  counter=$(( $counter + $increment ))
  echo "$line  $counter"
  #echo "$line">oneFileName.txt
  
  root -l -b -q process_track_tree_draw_v8.C\(\"$line\",\"$counter\",\"$filename\"\)
  if [[ $counter == "4" ]]
  then 
    break
  fi
#   bash eachFileRun.sh oneFileName.txt $counter
done < "$filename"

duration=$SECONDS
echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
