#!/bin/bash
filename="list_root_hics_165gev_w0_3000nm_WIS.txt"
counter=0
increment=1
while IFS= read -r line
do
  echo "$line">check.txt
  counter=$(( $counter + $increment ))
  echo "$counter"
done < "$filename"
