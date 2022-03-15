#! /bin/bash



# For Tracks tree:
echo "e+laser electron only samples"

filename=""
filename1=""
filename2=""
filename3=""
filename4=""

if [[ $1 == "W" ]]
then
   #filename="EBeamOnlyWIS.txt"
   filename="EBeamOnlyWISPartial.txt"
   filename1="EBeamOnlyWIS_DividedByBX1.txt"
   filename2="EBeamOnlyWIS_DividedByBX2.txt"
   filename3="EBeamOnlyWIS_DividedByBX3.txt"
   filename4="EBeamOnlyWIS_DividedByBX4.txt"
   filename5="EBeamOnlyWIS_DividedByBX5.txt"
   
else
   ### for Aluminium window
#    filename="ePlusLaserBkgNewSamplesAluminiumWindow_AllBX.txt"
   ### for previous window
#    filename="ePlusLaserBkgNewSamplesMarch62021_AllBX.txt"
   #### from Sasha's files
#    filename="/nfs/dust/luxe/group/MCProduction/Background/elaser/11032021_9f6b6590_fast_sim_al_window/list_root_hics_background_fast_9f6b6590_al_window.txt"
   ### 2021 e+laser bkg files
   filename="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/EPlusLaserBackgroundAnalyzer/ePlusLaserBackground_list_root_7671ee4c_AllBX.txt"
fi

# #### this block is to read all files in one list
# SECONDS=0
# 
# if [[ $1 == "W" ]]
# then
#     #root -l -b -q process_track_tree_draw_v6.C\(\"${filename1}\"\)
#     #root -l -b -q process_track_tree_draw_v6.C\(\"${filename2}\"\)
#     #root -l -b -q process_track_tree_draw_v6.C\(\"${filename3}\"\)
# #     root -l -b -q process_track_tree_draw_v6.C\(\"${filename4}\"\)
# #     root -l -b -q process_track_tree_draw_v6.C\(\"${filename5}\"\)
#     root -l -b -q process_track_tree_draw_v7.C\(\"${filename}\"\)
# else
#     root -l -b -q process_track_tree_draw_v7.C\(\"${filename}\"\)
# fi
# duration=$SECONDS
# echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
# 
# # exit 1



#### this block is to read one line of a list at a time
echo "background e+laser"
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



# SECONDS=0
# root -l -b -q process_hits_tree_draw_v6.C\(\"${filename}\"\)
duration=$SECONDS
echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
