#### this code mixes the background tracks and signal tracks per bunch crossing
#### run: python3 plotBackgroundFilesFromText.py -l  <event file in text mode>  -b <bx number>
import os
import sys
import time
import pprint
import math, array
from ROOT import *
from collections import OrderedDict
import argparse
    
def energyBins(nbins):
  #//// variable binned in X axis histograms
  logmin           = -6;
  logmax           = 1;
  logbinwidth      = (logmax-logmin)/float(nbins);
  xpoints          = []
  
  for i in range(0, nbins+1):
      #print((logmin + i*logbinwidth), pow( 10,(logmin + i*logbinwidth) ))
      xpoints.append(pow( 10,(logmin + i*logbinwidth) ))
                     
  xpoints.append(2*pow( 10,1))
  return xpoints

def main():
    
    parser = argparse.ArgumentParser(description='Code to get 2D plots')
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="ePlusLaserBackgroundTDR_list_root_7671ee4c_HitBranchesForAllPix_SortedInEvents_Total2p13BX.txt")
    parser.add_argument('-b', action="store", dest="bx", type=float, default=2.13)
    args = parser.parse_args()
    
    inDir = '/Users/arkasantra/AllPix2/InputFiles/HitBranchesTxtFiles'
    
    bkgFileName   = open(inDir+'/'+args.inFile)
    withoutText   = args.inFile.split('.txt')[0]
    rootFile      = withoutText+"_HitsTimePerChipHistogram.root"
    nbx           = args.bx
    
    
    print('BX selected: ',nbx)
    
    outFile       = TFile(inDir+'/'+rootFile, "RECREATE")
    outFile.cd()
    
    ndet  = 16*9;
    npixx = 1024;
    npixy = 512;
    
    nbins  = 450
    xbins  = energyBins(nbins)
    xarray = array.array('d',xbins)
    
    allHistoDict  = {}
    allHistoDict.update({"tracking_planes_hits_timeLayer_0":TH1D("tracking_planes_hits_timeLayer_0","tracking_planes_hits_timeLayer_0", 1000, 0.0, 200.0)})
    allHistoDict.update({"tracking_planes_hits_timeLayer_1":TH1D("tracking_planes_hits_timeLayer_1","tracking_planes_hits_timeLayer_1", 1000, 0.0, 200.0)})
    allHistoDict.update({"tracking_planes_hits_timeLayer_2":TH1D("tracking_planes_hits_timeLayer_2","tracking_planes_hits_timeLayer_2", 1000, 0.0, 200.0)})
    allHistoDict.update({"tracking_planes_hits_timeLayer_3":TH1D("tracking_planes_hits_timeLayer_3","tracking_planes_hits_timeLayer_3", 1000, 0.0, 200.0)})
    
    for i in range(0, ndet):
        allHistoDict.update({"tracking_planes_hits_time_"+str(i):TH1D("tracking_planes_hits_time_"+str(i),"tracking_planes_hits_time_"+str(i), 1000, 0.0, 200.0)})
    
    
    lineCounter   = 0
    ### write the bkg as it is
    for lines in bkgFileName.readlines():
        if '#' in lines:
            continue
        lineCounter += 1
        if(lineCounter%10000==0): print("processed: ", lineCounter)
        ##event  energy  time x  y z  detector pdg_code  track_id  parent_id layer_id det hitcellx hitcelly trackz trackE vtxx vtxy vtxz p_x p_y p_z weight totalHitEDep
        lines           = lines.rstrip()
        eachWord        = lines.split()
        event           = int(eachWord[0])
        time            = float(eachWord[2])
        layer_id        = int(eachWord[10])
        det             = int(eachWord[11])
        
        #print(pdgIdString)
        
        #if(layer_id==0 and det>3):print("detector: ", detector, " layer_id: ", layer_id, " det: ", det, " histogram id: ", layer_id+det*16)
        allHistoDict["tracking_planes_hits_time_"+str(layer_id+det*16)].Fill(time)
        if(layer_id==0): allHistoDict["tracking_planes_hits_timeLayer_"+str(layer_id)].Fill(time)
        if(layer_id==1): allHistoDict["tracking_planes_hits_timeLayer_"+str(layer_id)].Fill(time)
        if(layer_id==2): allHistoDict["tracking_planes_hits_timeLayer_"+str(layer_id)].Fill(time)
        if(layer_id==3): allHistoDict["tracking_planes_hits_timeLayer_"+str(layer_id)].Fill(time)
        
            
        
    for keys in allHistoDict:
        allHistoDict[keys].Scale(1./nbx)
        allHistoDict[keys].Write()
    outFile.Close()
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
