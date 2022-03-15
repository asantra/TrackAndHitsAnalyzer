### code to check the root file
### run: python getGoodBkgFiles.py <list of background file names>
import os
import sys
import time
import pprint
import math
from ROOT import *
from collections import OrderedDict
import argparse


def main():
    gROOT.SetBatch()
    inFile  = open(sys.argv[1])
    #outFile = open("ePlusLaserNewBkgSamples.txt", "w")
    totalNumber = 0
    for lines in inFile.readlines():
        lines        = lines.rstrip()
        if('#' in lines): continue
        #print("I am working on: ",lines)
        
        try:
            rootFile     = TFile(lines, "READ")
            
            
            #### use this part to divide the list into BXs
            #dirAddress   = gDirectory.Get("hist")
            #h0Value      = dirAddress.Get("h0")
            #eventNumber  = h0Value.GetEntries()
            #totalNumber += eventNumber
            #print("totalNumber of electrons: ",totalNumber)
            
            #i = int(totalNumber) // 1500000000
            #print("The division = ", i)
            #if(i>50):
                #break
            #outFile1 = open("ePlusLaserBkg_7671ee4c_DividedByBX"+str(i+1)+".txt", "a")
            #outFile1.write(lines+"\n")
            
            
            #### use this part to know if there is any problem in the Hits tree
            tree = rootFile.Get("Hits")
            hTrackDep = TH1F("hTrackDep", "hTrackDep",100,0,100)
            tree.Draw("trackedep >> hTrackDep")
            entry = hTrackDep.GetEntries()
            print("The entry in Hits tree for line ",lines, " : ",entry)
            
        except:
            print("something wrong here: ", lines)
            
    #outFile1.close()
            
            
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
