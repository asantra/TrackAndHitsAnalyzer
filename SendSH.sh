#! /bin/bash
targetDir="/srv01/agrp/arkas/gridScript/Sasha_Script"
targetDirPlot="/srv01/agrp/arkas/gridScript/Sasha_Script/makePlots"
sftp arkas@wipp-an1 << EOF
# put -r lx86a1_run_naf_hicsbackground $targetDir
# put -r lxb18e_run_naf_background $targetDir
# put -r AnalyzerSetup/* $targetDirPlot
# put -r lxmacro/*.C $targetDirPlot
# put -r lxmacro/*.h $targetDirPlot
# put -r lxmacro/*.txt $targetDirPlot
# put -r lxmacro/*.sh $targetDirPlot
put -r lx_hics_bacground_naf_7671ee4c_August31_2021 $targetDir
EOF
