### setup to make plots for the tracker ###

import os, sys, glob, time
from ROOT import *
import argparse
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint





def main():
    gROOT.SetBatch()
    
    parser = argparse.ArgumentParser(description='Code to get 2D plots')
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="ePlusLaserBkg_7671ee4c_Total2p13BX_HitsInfo.txt")
    args = parser.parse_args()
    
    
    inputDir            = "/Users/arkasantra/arka/Sasha_Work/OutputFile/HitsTextFiles" 
    outFile             = TFile("weightFor3.root", "RECREATE")
    outFile.cd()
    weightHist          = TH1F("weightHist", "weightHist", 20, 0,20)
    countTracks = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
    with open(inputDir+"/"+args.inFile) as inText:
        for line in inText.readlines():
            ## bxNumber  hitid  layer_id  det_id  energy  ev_weight  hitcellx  hitcelly pdgIdString  trackEnergyString trackIdString vertexString hitEnergyString true_type
            if "#" in line:
                continue
            line = line.rstrip()
            eachWord = line.split()
            bxNumber = int(eachWord[0])
            layerId  = int(eachWord[2])
            detId    = int(eachWord[3])
            chipId   = layerId+detId*16
            weight   = float(eachWord[5])
            pdg      = eachWord[8]
            trkId    = eachWord[10]
            if weight!= 1.0 and '-11' in pdg and '1' in trkId:
                print("The weight is: ", weight, " pdgIdString: ", pdg, " trkId: ", trkId)
                weightHist.Fill(weight)
            if(chipId%16==0): 
                countTracks[bxNumber] += 1
            
            
    print("The Nhits for each BX is below--- ")
    pprint.pprint(countTracks)
    
    Total = 0
    for key in countTracks:
        Total += countTracks[key]
        
    print("The total is :", Total, " and BX is: ", key)
    print("The average is :", Total/4.0)
            
    outFile.Write()
    outFile.Close()
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print ("The total time taken: ", time.time() - start, " s")
