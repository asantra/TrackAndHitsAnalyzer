### code to check the root file
### run: python makeSmallList.py <list of background file names>
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
    for lines in inFile.readlines():
        lines        = lines.rstrip()
        if('#' in lines): continue
        print("I am working on: ",lines)
        outFile1 = open("ePlusLaserBkgNewSamples_File"+str(i+1)+".txt", "a")
        outFile1.write(lines+"\n")
        i += 1
        
        
    outFile1.close()
            
            
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
