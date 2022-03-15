#! /bin/bash

filename=""

if [[ $1 == "W" ]]
then
   filename="list_root_hics_165gev_w0_3000nm_WIS.txt"
else
   filename="/nfs/dust/ilc/user/oborysov/hics_list/list_root_hics_165gev_w0_3000nm.txt"
fi



#### hits tree
SECONDS=0
echo "w0_3000nm JETI40 Hits"
counter=0
increment=1
rm list_root*_HitsInfo.txt
while IFS= read -r line
do
  counter=$(( $counter + $increment ))
  echo "$line  $counter" 
  bash eachFileRun.sh $line $counter
done < "$filename"
duration=$SECONDS
echo "Total time taken for this process ---- $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
