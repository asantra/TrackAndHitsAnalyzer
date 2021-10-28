#### this code mixes the background tracks and signal tracks per bunch crossing
#### run: python3 plotSignalFilesFromText.py -l  <event file in text mode> -b <bx number>
import os
import sys
import time
import pprint
import math, array
from ROOT import *
from collections import OrderedDict
import argparse

#### add diagonal vertex cut
#def checkVtxCut(vtxx, vtxz):
    #if((-45.0 < vtxx <= -25.5 ) and (3800 < vtxz <= 4200)):
        #return True
    #elif((-55.0 < vtxx <= -35.0) and (4200 < vtxz <= 4500)):
        #return True
    #elif((-60.0 < vtxx <= -45.0) and (4500 < vtxz <= 5000)):
        #return True
    #elif((-70 < vtxx <= -50.0) and (5000 < vtxz <= 5500)):
        #return True
    #elif((-75 < vtxx <= -60.0) and (5500 < vtxz <= 6000)):
        #return True 
    #elif((-80 < vtxx <= -65.0) and (5500 < vtxz <= 6000)):
        #return True
    #elif((-90 < vtxx <= -70.0) and (6000 < vtxz <= 6500)):
        #return True
    #elif((-100.0 < vtxx <= -80.0) and (6500 < vtxz <= 7000)):
        #return True
    #else:
        #return False
    
### anything below x, remove it cut
def checkVtxCut(vtxx, vtxz):
    if((vtxx <= -25.5 ) and (3800 < vtxz <= 4200)):
        return True
    elif((vtxx <= -35.0) and (4200 < vtxz <= 4500)):
        return True
    elif((vtxx <= -45.0) and (4500 < vtxz <= 5000)):
        return True
    elif((vtxx <= -50.0) and (5000 < vtxz <= 5500)):
        return True
    elif((vtxx <= -60.0) and (5500 < vtxz <= 6000)):
        return True 
    elif((vtxx <= -65.0) and (5500 < vtxz <= 6000)):
        return True
    elif((vtxx <= -70.0) and (6000 < vtxz <= 6500)):
        return True
    elif((vtxx <= -80.0) and (6500 < vtxz <= 7000)):
        return True
    else:
        return False
    
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
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="signalMC_e0gpc_3.0_trackInfo.txt")
    parser.add_argument('-b', action="store", dest="bx", type=float, default=10.0)
    args = parser.parse_args()
    
    inDir = '/Users/arkasantra/arka/Sasha_Work/OutputFile'
    
    bkgFileName   = open(inDir+'/'+args.inFile)
    withoutText   = args.inFile.split('.txt')[0]
    rootFile      = withoutText+".root"
    nbx           = args.bx
    
    print('BX selected: ',nbx)
    
    outFile       = TFile(inDir+'/'+rootFile, "RECREATE")
    outFile.cd()
    nbins  = 450
    xbins  = energyBins(nbins)
    xarray = array.array('d',xbins)
    
    #print(xarray, " ", len(xarray))
    
    allHistoDict  = {}
    for i in range(0, 16):
        #### positrons
        allHistoDict.update({"tracking_planes_signal_track_x_positrons_"+str(i):TH1D("tracking_planes_signal_track_x_positrons_"+str(i),"tracking_planes_signal_track_x_positrons_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_signal_track_x_positrons_sumE_"+str(i):TH1D("tracking_planes_signal_track_x_positrons_sumE_"+str(i),"tracking_planes_signal_track_x_positrons_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_signal_track_x_positrons_1GeVCut_"+str(i):TH1D("tracking_planes_signal_track_x_positrons_1GeVCut_"+str(i),"tracking_planes_signal_track_x_positrons_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_signal_track_e_positrons_log_"+str(i):TH1D("tracking_planes_signal_track_e_positrons_log_"+str(i),"tracking_planes_signal_track_e_positrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_signal_vtx_z_track_e_positrons_log_"+str(i):TH2D("tracking_planes_signal_vtx_z_track_e_positrons_log_"+str(i),"tracking_planes_signal_vtx_z_track_e_positrons_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_signal_vtx_x_track_e_positrons_log_"+str(i):TH2D("tracking_planes_signal_vtx_x_track_e_positrons_log_"+str(i),"tracking_planes_signal_vtx_x_track_e_positrons_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_signal_vtxz_vtxx_positrons_"+str(i):TH2D("tracking_planes_signal_vtxz_vtxx_positrons_"+str(i), "tracking_planes_signal_vtxz_vtxx_positrons_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        
        
        
    
    
    lineCounter   = 0
    ### write the bkg as it is
    for lines in bkgFileName.readlines():
        if '#' in lines:
            continue
        lineCounter += 1
        if(lineCounter%1000==0): print("processed: ", lineCounter)
        #if(lineCounter > 200000):break
        lines        = lines.rstrip()
        eachWord     = lines.split()
        bxNumber     = int(eachWord[0])
        trackId      = int(eachWord[2])
        pdgId        = int(eachWord[1])
        staveId      = int(eachWord[3])-1000
        xPos         = float(eachWord[4])
        yPos         = float(eachWord[5])
        energyVal    = float(eachWord[6])
        weight       = float(eachWord[7])
        vtx_x        = float(eachWord[8])
        vtx_y        = float(eachWord[9])
        vtx_z        = float(eachWord[10])
        
        failVtxCut = checkVtxCut(vtx_x, vtx_z)
            
        ### positrons
        if(pdgId == -11 and trackId==1):
            allHistoDict["tracking_planes_signal_track_x_positrons_"+str(staveId)].Fill(xPos, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_signal_track_x_positrons_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_signal_track_x_positrons_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            allHistoDict["tracking_planes_signal_track_e_positrons_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_signal_vtx_z_track_e_positrons_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_signal_vtx_x_track_e_positrons_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_signal_vtxz_vtxx_positrons_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
        
        
    for keys in allHistoDict:
        allHistoDict[keys].Scale(1./nbx)
        allHistoDict[keys].Write()
    outFile.Close()
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
