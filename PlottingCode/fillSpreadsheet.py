### setup to make plots for the tracker ###
### This is to plot four particles on top of each other in tracker layer 1 and layer 4. 

import os, sys, glob, time
from ROOT import *
import argparse
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint





def main():
    gROOT.SetBatch()
    inputDir            = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inputTracksRootFile = sys.argv[1]
    inRoot              = TFile(inputDir+"/"+inputTracksRootFile, "READ")
    
    histogramNames      = ["tracking_planes_background_track_x_gamma",
                           "tracking_planes_background_track_x_electrons",
                           "tracking_planes_background_track_x_positrons",
                           "tracking_planes_background_track_x_gamma_1GeVCut",
                           "tracking_planes_background_track_x_electrons_1GeVCut",
                           "tracking_planes_background_track_x_positrons_1GeVCut",
                           "tracking_planes_background_track_x_gamma_sumE",
                           "tracking_planes_background_track_x_electrons_sumE",
                           "tracking_planes_background_track_x_positrons_sumE"]
    print("=============================================================")
    print("Working on: ",inputTracksRootFile)
    print("=============================================================")
    for names in histogramNames:
        print("---- Histogram name: ", names)
        #for i in range(8,16):
            #hName         = names+"_"+str(i)
            #hist          = inRoot.Get(hName)
            ##### normalize per BX
            ##hist.Scale(1./17.)
            #integralValue = hist.Integral(0, hist.GetNbinsX()+1)
            #scieNotation  = "{:e}".format(integralValue)

            #print(scieNotation)
        for i in range(0,8):
            hName         = names+"_"+str(i)
            hist          = inRoot.Get(hName)
            ### normalize per BX
            #hist.Scale(1./17.)
            integralValue = hist.Integral(0, hist.GetNbinsX()+1)
            scieNotation  = "{:e}".format(integralValue)

            print(scieNotation)
    
    
    
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print "The total time taken: ", time.time() - start, " s"
