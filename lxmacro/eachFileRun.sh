#! /bin/bash

root -l -b << EOF
  .L process_hits_tree_draw_v4.C++
  process_hits_tree_draw_v4("$1", "$2")
EOF
