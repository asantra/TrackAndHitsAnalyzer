### code to check the root file
### run: python modifyTextFiles.py <list of background file names>
import os
import sys
import time
import pprint
import math
from ROOT import *
from collections import OrderedDict
import argparse


def main():
    inFile  = open(sys.argv[1])
    i = 0
    outFile1 = open("ePlusLaserBackground_list_root_7671ee4c_DividedByBX4_HitBranchesForAllPix.txt", "a")
    for lines in inFile.readlines():
        if('#' in lines): continue
        lines         = lines.rstrip()
        allcolumns    = lines.split()
        allcolumns[0] = "3"
        modifyLines   = " ".join(allcolumns)
        if(i%100000==0):print("processed: ",i)
        
        outFile1.write(modifyLines+"\n")
        i += 1
        
        
    outFile1.close()
            
            
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
