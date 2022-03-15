#! /bin/bash

root -l -b << EOF
  .L process_lxtrees_v4.C++
  process_lxtrees_v4("$1", "$2")
EOF
