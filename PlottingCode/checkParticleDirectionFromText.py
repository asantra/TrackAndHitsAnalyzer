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
    


def main():
    
    parser = argparse.ArgumentParser(description='Code to get 2D plots')
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="ePlusLaserBackgroundTDR_list_root_7671ee4c_trackInfo_Total2p13BX.txt")
    parser.add_argument('-b', action="store", dest="bx", type=float, default=2.13)
    args = parser.parse_args()
    
    inDir = '/Users/arkasantra/arka/Sasha_Work/OutputFile'
    #inDir = "/Volumes/Study/Weizmann_PostDoc/Sasha_work/OutputFile/ReprocessedBkgTracksAfterTDR"
    
    bkgFileName   = open(inDir+'/'+args.inFile)
    withoutText   = args.inFile.split('.txt')[0]
    rootFile      = withoutText+"_DirectionCheck.root"
    nbx           = args.bx
    
    print('BX selected: ',nbx)
    
    outFile       = TFile(inDir+'/'+rootFile, "RECREATE")
    outFile.cd()
    
    #print(xarray, " ", len(xarray))
    
    allHistoDict  = {}
    
    allHistoDict.update({"tracking_planes_bkg_track_deltadirectionX_0":TH1D("tracking_planes_bkg_track_deltadirectionX_0","tracking_planes_bkg_track_deltadirectionX_0; track slope (vertex) - track slope (momentum)",500,-100,100)})
    allHistoDict.update({"tracking_planes_bkg_track_deltadirectionX_1":TH1D("tracking_planes_bkg_track_deltadirectionX_1","tracking_planes_bkg_track_deltadirectionX_1; track slope (vertex) - track slope (momentum)",500,-100,100)})
    allHistoDict.update({"tracking_planes_bkg_track_deltadirectionX_8":TH1D("tracking_planes_bkg_track_deltadirectionX_8","tracking_planes_bkg_track_deltadirectionX_8; track slope (vertex) - track slope (momentum)",500,-100,100)})
    allHistoDict.update({"tracking_planes_bkg_track_deltadirectionX_9":TH1D("tracking_planes_bkg_track_deltadirectionX_9","tracking_planes_bkg_track_deltadirectionX_9; track slope (vertex) - track slope (momentum)",500,-100,100)})
    
    
    allHistoDict.update({"tracking_planes_bkg_track_deltadirectionY_0":TH1D("tracking_planes_bkg_track_deltadirectionY_0","tracking_planes_bkg_track_deltadirectionY_0; track slope (vertex) - track slope (momentum)",500,-100,100)})
    allHistoDict.update({"tracking_planes_bkg_track_deltadirectionY_1":TH1D("tracking_planes_bkg_track_deltadirectionY_1","tracking_planes_bkg_track_deltadirectionY_1; track slope (vertex) - track slope (momentum)",500,-100,100)})
    allHistoDict.update({"tracking_planes_bkg_track_deltadirectionY_8":TH1D("tracking_planes_bkg_track_deltadirectionY_8","tracking_planes_bkg_track_deltadirectionY_8; track slope (vertex) - track slope (momentum)",500,-100,100)})
    allHistoDict.update({"tracking_planes_bkg_track_deltadirectionY_9":TH1D("tracking_planes_bkg_track_deltadirectionY_9","tracking_planes_bkg_track_deltadirectionY_9; track slope (vertex) - track slope (momentum)",500,-100,100)})
    
    
    
    #for i in range(0, 16):
        ##### gamma
        #allHistoDict.update({"tracking_planes_background_track_x_gamma_"+str(i):TH1D("tracking_planes_background_track_x_gamma_"+str(i),"tracking_planes_background_track_x_gamma_"+str(i),1300, -650.0, 650.0)})
        
    lineCounter   = 0
    
    
    ### write the bkg as it is
    for lines in bkgFileName.readlines():
        if '#' in lines:
            continue
        lineCounter += 1
        if(lineCounter%100000==0): print("processed: ", lineCounter)
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
        parent_id    = int(eachWord[11])
        pxx          = float(eachWord[12])
        pyy          = float(eachWord[13])
        pzz          = float(eachWord[14])
        
        zproj = 2770.0
        
        xdir = pxx/pzz
        ydir = pyy/pzz
        
        if(staveId==0):
            zz = 3962.0125
            xPosDir = (xPos - vtx_x)/(zz-vtx_z)
            yPosDir = (yPos - vtx_y)/(zz-vtx_z)
            
            allHistoDict["tracking_planes_bkg_track_deltadirectionX_0"].Fill(xPosDir - xdir)
            allHistoDict["tracking_planes_bkg_track_deltadirectionY_0"].Fill(yPosDir - ydir)
            
        if(staveId==1):
            zz = 3950.0125
            xPosDir = (xPos - vtx_x)/(zz-vtx_z)
            yPosDir = (yPos - vtx_y)/(zz-vtx_z)
            
            allHistoDict["tracking_planes_bkg_track_deltadirectionX_1"].Fill(xPosDir - xdir)
            allHistoDict["tracking_planes_bkg_track_deltadirectionY_1"].Fill(yPosDir - ydir)
            
        if(staveId==8):
            zz = 3962.0125
            xPosDir = (xPos - vtx_x)/(zz-vtx_z)
            yPosDir = (yPos - vtx_y)/(zz-vtx_z)
            
            allHistoDict["tracking_planes_bkg_track_deltadirectionX_8"].Fill(xPosDir - xdir)
            allHistoDict["tracking_planes_bkg_track_deltadirectionY_8"].Fill(yPosDir - ydir)
            
        if(staveId==9):
            zz = 3950.0125
            xPosDir = (xPos - vtx_x)/(zz-vtx_z)
            yPosDir = (yPos - vtx_y)/(zz-vtx_z)
            
            allHistoDict["tracking_planes_bkg_track_deltadirectionX_9"].Fill(xPosDir - xdir)
            allHistoDict["tracking_planes_bkg_track_deltadirectionY_9"].Fill(yPosDir - ydir)
        
    for keys in allHistoDict:
        allHistoDict[keys].Scale(1./nbx)
        allHistoDict[keys].Write()
    outFile.Close()
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
