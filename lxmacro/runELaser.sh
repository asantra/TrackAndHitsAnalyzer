#! /bin/bash

filename=""
filename2=""

if [[ $1 == "W" ]]
then
#    filename="list_root_hics_165gev_w0_3000nm_WIS.txt"
   filename="/nfs/dust/luxe/user/oborysov/hics_list/list_root_hics_165gev_w0_3000nm_jeti40_122020_9550dac4.txt"
else
### electromagnetic particle list
     #filename="/nfs/dust/luxe/group/MCProduction/Signal/g4/IPstrong_V1.1.00/JETI40/e_laser/16.5GeV/lxsim_hics_6cac1288_alw/list/g4/list_root_hics_165gev_w0_3000nm_jeti40_122020_6cac1288.txt"
     filename="signalMC_e0ppw_3.0.txt"
### QGSP physics list
     #filename="/nfs/dust/luxe/user/oborysov/hics_list/list_root_hics_w0_5000nm_qgsp_bert_hp_9a61db54.txt"
     #filename="/nfs/dust/luxe/user/oborysov/hics_list/list_root_hics_w0_8000nm_qgsp_bert_hp_9a61db54.txt"
#      filename="/nfs/dust/luxe/user/oborysov/hics_list/list_root_hics_background_qgsp_9a61db54_0_13.txt"
fi

# ### For Tracks tree:
SECONDS=0
echo "Xi 0.5 JETI40"
root -l -b -q process_track_tree_draw_v9.C\(\"${filename}\"\)
# root -l -b -q process_track_tree_draw_v3.C\(\"${filename2}\"\)
duration=$SECONDS
echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

exit 1



# # 
# SECONDS=0
# echo "w0_8000nm JETI40"
# root -l -b -q process_track_tree_draw_v3.C'("/nfs/dust/ilc/user/oborysov/hics_list/list_root_hics_165gev_w0_8000nm.txt")'
# # do some work
# duration=$SECONDS
# echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
# 
# 
# exit 1

# SECONDS=0
# echo "w0_8000nm Phase2"
# root -l -b -q process_track_tree_draw_v3.C'("/nfs/dust/ilc/user/oborysov/hics_list/list_root_hics_phase2_165gev_w0_8000nm.txt")'
# duration=$SECONDS
# echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

