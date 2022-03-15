#! /bin/bash



# For Tracks tree:
echo "e+laser electron only samples"

filename=""

if [[ $1 == "W" ]]
then
   #filename="EBeamOnlyWIS.txt"
#    filename1="EBeamOnlyWIS_DividedByBX1.txt"
#    filename2="EBeamOnlyWIS_DividedByBX2.txt"
#    filename3="EBeamOnlyWIS_DividedByBX3.txt"
#    filename4="EBeamOnlyWIS_DividedByBX4.txt"
    filename="QGSPList_EBeamOnly.txt"
else
#    #filename="EBeamOnly.txt"
#    filename="/nfs/dust/luxe/user/oborysov/hics_list/list_root_hics_background_fast_c99bba6d_0_18_luxe.txt"
#    filename="ePlusLaserBkgNewSamplesMarch62021_AllBX.txt"
#     filename="/nfs/dust/luxe/group/MCProduction/Background/elaser/29102020_lx86a1/Merged/Files/"
#     filename="/nfs/dust/luxe/user/oborysov/hics_list/list_root_hics_background_qgsp_9a61db54_0_13.txt"
#    filename="/nfs/dust/luxe/group/MCProduction/Background/elaser/11032021_9f6b6590_fast_sim_al_window/list_root_hics_background_fast_9f6b6590_al_window.txt"
### 2021 e+laser bkg files
   filename="/afs/desy.de/user/s/santraar/private/Geant4_File_Analyzer/EPlusLaserBackgroundAnalyzer/ePlusLaserBackground_list_root_7671ee4c_AllBX.txt"
fi


#### this block is to read all files in one list
SECONDS=0


# if [[ $1 == "W" ]]
# then
# #     root -l -b -q process_lxtrees_v2.C\(\"${filename1}\"\)
# #     root -l -b -q process_lxtrees_v2.C\(\"${filename2}\"\)
# #     root -l -b -q process_lxtrees_v2.C\(\"${filename3}\"\)
# #     root -l -b -q process_lxtrees_v2.C\(\"${filename4}\"\)
#     root -l -b -q process_lxtrees_background.C\(\"${filename}\"\)
# else
# #     root -l -b -q process_lxtrees_v2.C\(\"${filename}\"\)
#     root -l -b -q process_lxtrees_background_v2.C\(\"${filename}\", "0", \"$filename\"\)
# fi


# #### this block is to read one line of a list at a time
echo "e+laser background"
counter=0
increment=1
rm *HitsProperInfo.txt
rm *HitBranchesForAllPix.txt
rm HitBranchesForAllPix*root
while IFS= read -r line
do
  counter=$(( $counter + $increment ))
  echo "$line  $counter"
  echo "$line">oneFileName.txt
  
  root -l -b -q process_lxtrees_background_v2.C\(\"$line\",\"$counter\",\"$filename\"\)
  if [[ $counter == "10" ]]
  then 
    break
  fi
#   bash eachFileRun.sh oneFileName.txt $counter
done < "$filename"

duration=$SECONDS
echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds."
