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
mm2m = 1./1000.0

def getESeed(LB, xExit, zMid):
    B = -0.897
    R = (LB-zMid)*LB/xExit + xExit
    p = 0.3*B*R*mm2m
    return p
    
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
    
    outSimplifiedText = open(inDir+'/'+withoutText+"_Layer1Signal.txt","w")
    outSimplifiedText2 = open(inDir+'/'+withoutText+"_Layer4Signal.txt","w")
    nbins  = 450
    xbins  = energyBins(nbins)
    xarray = array.array('d',xbins)
    
    #print(xarray, " ", len(xarray))
    
    allHistoDict  = {}
    
    allHistoDict.update({"tracking_planes_signal_track_x_track_y_dipole_positrons_0":TH2D("tracking_planes_signal_track_x_track_y_dipole_positrons_0", "tracking_planes_signal_track_x_track_y_dipole_positrons_0", 250, 0, 250, 40, -20, 20)})
    allHistoDict.update({"tracking_planes_signal_track_x_track_y_dipole_positrons_1":TH2D("tracking_planes_signal_track_x_track_y_dipole_positrons_1", "tracking_planes_signal_track_x_track_y_dipole_positrons_1", 250, 0, 250, 40, -20, 20)})
    allHistoDict.update({"tracking_planes_signal_track_x_track_y_dipole_positrons_8":TH2D("tracking_planes_signal_track_x_track_y_dipole_positrons_8", "tracking_planes_signal_track_x_track_y_dipole_positrons_8", 250, 0, 250, 40, -20, 20)})
    allHistoDict.update({"tracking_planes_signal_track_x_track_y_dipole_positrons_9":TH2D("tracking_planes_signal_track_x_track_y_dipole_positrons_9", "tracking_planes_signal_track_x_track_y_dipole_positrons_9", 250, 0, 250, 40, -20, 20)})
    allHistoDict.update({"tracking_planes_signal_track_e_dipole_positrons_log_0":TH1D("tracking_planes_signal_track_e_dipole_positrons_log_0","tracking_planes_signal_track_e_dipole_positrons_log_0; Energy [GeV]; Particles/BX",nbins+1, xarray)})
    allHistoDict.update({"tracking_planes_signal_track_e_dipole_positrons_log_1":TH1D("tracking_planes_signal_track_e_dipole_positrons_log_1","tracking_planes_signal_track_e_dipole_positrons_log_1; Energy [GeV]; Particles/BX",nbins+1, xarray)})
    
    allHistoDict.update({"tracking_planes_signal_delta_track_e_positrons_log_0":TH1D("tracking_planes_signal_delta_track_e_positrons_log_0","tracking_planes_signal_delta_track_e_positrons_log_0; (Actual Energy - Reconstructed Energy) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_signal_delta_track_e_positrons_log_1":TH1D("tracking_planes_signal_delta_track_e_positrons_log_1","tracking_planes_signal_delta_track_e_positrons_log_1; (Actual Energy - Reconstructed Energy) [GeV]; Particles/BX",100, -10,10)})
    
    
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
            outSimplifiedText.write(lines)
            outSimplifiedText2.write(lines)
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
        parentId     = float(eachWord[11])
        pxx          = float(eachWord[12])
        pyy          = float(eachWord[13])
        pzz          = float(eachWord[14])
            
        ### positrons
        if(pdgId == -11 and trackId==1):
            if(staveId==0 or staveId==1):
                outSimplifiedText.write(lines+"\n")
            if(staveId==6 or staveId==7):
                outSimplifiedText2.write(lines+"\n")
            zproj = 2770.0
            
            if(staveId==0):
                zz = 3962.0125
                xproj = pxx/pzz*(zproj-zz) + xPos
                yproj = pyy/pzz*(zproj-zz) + yPos
                allHistoDict["tracking_planes_signal_track_x_track_y_dipole_positrons_0"].Fill(xproj, yproj, weight)
                
                
                zmid  = zz - xPos*(pzz/pxx)
                LB    = 1440
                reconstructE = getESeed(LB, xproj, zmid)
                deltaE = (energyVal - reconstructE)
                #print("actual energy: ", energyVal, " reconstructE ", reconstructE, " difference ",deltaE)
                allHistoDict["tracking_planes_signal_delta_track_e_positrons_log_0"].Fill(deltaE)
                
                if(xproj>150):
                   allHistoDict["tracking_planes_signal_track_e_dipole_positrons_log_0"].Fill(energyVal)
                   
                   
            if(staveId==1):
                zz = 3950.0125
                xproj = pxx/pzz*(zproj-zz) + xPos
                yproj = pyy/pzz*(zproj-zz) + yPos
                allHistoDict["tracking_planes_signal_track_x_track_y_dipole_positrons_1"].Fill(xproj, yproj, weight)
                
                zmid  = zz - xPos*(pzz/pxx)
                LB    = 1440
                reconstructE = getESeed(LB, xproj, zmid)
                deltaE = (energyVal - reconstructE)
                allHistoDict["tracking_planes_signal_delta_track_e_positrons_log_1"].Fill(deltaE)
                
                if(xproj>150):
                   allHistoDict["tracking_planes_signal_track_e_dipole_positrons_log_1"].Fill(energyVal)
                   
                   
            if(staveId==8):
                zz = 3962.0125
                xproj = pxx/pzz*(zproj-zz) + xPos
                yproj = pyy/pzz*(zproj-zz) + yPos
                allHistoDict["tracking_planes_signal_track_x_track_y_dipole_positrons_8"].Fill(xproj, yproj, weight)
                
                
            if(staveId==9):
                zz = 3950.0125
                xproj = pxx/pzz*(zproj-zz) + xPos
                yproj = pyy/pzz*(zproj-zz) + yPos
                allHistoDict["tracking_planes_signal_track_x_track_y_dipole_positrons_9"].Fill(xproj, yproj, weight)
                
                
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
    outSimplifiedText.close()
    outSimplifiedText2.close()
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
