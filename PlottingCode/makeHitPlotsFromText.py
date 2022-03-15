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
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="ePlusLaserBkgNewSamplesMarch62021_HitsInfo_SortedInEvents_Total249BX.txt")
    parser.add_argument('-b', action="store", dest="bx", type=float, default=249)
    parser.add_argument('-w', action="store_true", dest="wgt")
    args = parser.parse_args()
    
    inDir = '/Users/arkasantra/arka/Sasha_Work/OutputFile/HitsTextFiles'
    
    bkgFileName   = open(inDir+'/'+args.inFile)
    withoutText   = args.inFile.split('.txt')[0]
    nbx           = args.bx
    needWeight    = args.wgt
    
    if needWeight:
        rootFile      = withoutText+"_AllPlotsWeighted_HitsPerChipHistogram.root"
    else:
        rootFile      = withoutText+"_NoWeight_HitsPerChipHistogram.root"
    
    
    print('BX selected: ',nbx)
    print('output file: ', rootFile)
    
    outFile       = TFile(inDir+'/'+rootFile, "RECREATE")
    outFile.cd()
    
    ndet  = 16*9;
    npixx = 1024;
    npixy = 512;
    
    nbins  = 450
    xbins  = energyBins(nbins)
    xarray = array.array('d',xbins)
    
    allHistoDict  = {}
    for i in range(0, ndet):
        allHistoDict.update({"tracking_planes_hits_x_"+str(i):TH1D("tracking_planes_hits_x_"+str(i),"tracking_planes_hits_x_"+str(i), npixx, 0.0, npixx)})
        #allHistoDict.update({"tracking_planes_hits_time_"+str(i):TH1D("tracking_planes_hits_time_"+str(i),"tracking_planes_hits_time_"+str(i), 100, 0.0, 50.0)})
        allHistoDict.update({"tracking_planes_hits_Edep_"+str(i):TH1D("tracking_planes_hits_Edep_"+str(i),"tracking_planes_hits_Edep_"+str(i), nbins, xarray)})
        allHistoDict.update({"tracking_planes_hits_y_"+str(i):TH1D("tracking_planes_hits_y_"+str(i),"tracking_planes_hits_y_"+str(i), npixy, 0.0, npixy)})
        allHistoDict.update({"tracking_planes_hits_xy_"+str(i):TH2D("tracking_planes_hits_xy_"+str(i),"tracking_planes_hits_xy_"+str(i), npixx, 0.0, npixx, npixy, 0.0, npixy)})
        
        allHistoDict.update({"tracking_planesneutral_hits_x_"+str(i):TH1D("tracking_planesneutral_hits_x_"+str(i),"tracking_planesneutral_hits_x_"+str(i), npixx, 0.0, npixx)})
        allHistoDict.update({"tracking_planesneutral_hits_Edep_"+str(i):TH1D("tracking_planesneutral_hits_Edep_"+str(i),"tracking_planesneutral_hits_Edep_"+str(i), nbins, xarray)})
        allHistoDict.update({"tracking_planesneutral_hits_y_"+str(i):TH1D("tracking_planesneutral_hits_y_"+str(i),"tracking_planesneutral_hits_y_"+str(i), npixy, 0.0, npixy)})
        allHistoDict.update({"tracking_planesneutral_hits_xy_"+str(i):TH2D("tracking_planesneutral_hits_xy_"+str(i),"tracking_planesneutral_hits_xy_"+str(i), npixx, 0.0, npixx, npixy, 0.0, npixy)})
        
        allHistoDict.update({"tracking_planescharged_hits_x_"+str(i):TH1D("tracking_planescharged_hits_x_"+str(i),"tracking_planescharged_hits_x_"+str(i), npixx, 0.0, npixx)})
        allHistoDict.update({"tracking_planescharged_hits_Edep_"+str(i):TH1D("tracking_planescharged_hits_Edep_"+str(i),"tracking_planescharged_hits_Edep_"+str(i), nbins, xarray)})
        allHistoDict.update({"tracking_planescharged_hits_y_"+str(i):TH1D("tracking_planescharged_hits_y_"+str(i),"tracking_planescharged_hits_y_"+str(i), npixy, 0.0, npixy)})
        allHistoDict.update({"tracking_planescharged_hits_xy_"+str(i):TH2D("tracking_planescharged_hits_xy_"+str(i),"tracking_planescharged_hits_xy_"+str(i), npixx, 0.0, npixx, npixy, 0.0, npixy)})
        
        allHistoDict.update({"tracking_planessilicon_hits_x_"+str(i):TH1D("tracking_planessilicon_hits_x_"+str(i),"tracking_planessilicon_hits_x_"+str(i), npixx, 0.0, npixx)})
        allHistoDict.update({"tracking_planessilicon_hits_Edep_"+str(i):TH1D("tracking_planessilicon_hits_Edep_"+str(i),"tracking_planessilicon_hits_Edep_"+str(i), nbins, xarray)})
        allHistoDict.update({"tracking_planessilicon_hits_y_"+str(i):TH1D("tracking_planessilicon_hits_y_"+str(i),"tracking_planessilicon_hits_y_"+str(i), npixy, 0.0, npixy)})
        allHistoDict.update({"tracking_planessilicon_hits_xy_"+str(i):TH2D("tracking_planessilicon_hits_xy_"+str(i),"tracking_planessilicon_hits_xy_"+str(i), npixx, 0.0, npixx, npixy, 0.0, npixy)})
    
    
    lineCounter   = 0
    positronHit   = 0
    totalPosHit   = 0
    ### write the bkg as it is
    for lines in bkgFileName.readlines():
        if '#' in lines:
            continue
        lineCounter += 1
        if(lineCounter%10000==0): print("processed: ", lineCounter)
        ## bxNumber  hitid  layer_id  det_id  energy  ev_weight  hitcellx  hitcelly pdgIdString  energyString trackIdString vertexString hitEnergyString
        lines           = lines.rstrip()
        eachWord        = lines.split()
        event           = int(eachWord[0])
        hitid           = int(eachWord[1])
        layer_id        = int(eachWord[2])
        det             = int(eachWord[3])
        energy          = float(eachWord[4])
        weight          = float(eachWord[5])
        hitcellx        = int(eachWord[6])
        hitcelly        = int(eachWord[7])
        pdgIdString     = eachWord[8]
        hitEnergyString = eachWord[12]
        
        if needWeight:
            plotWeight      = weight
        else:
            plotWeight      = 1.0
        #print(pdgIdString)
        
        #if(layer_id==0 and det>3):print("detector: ", detector, " layer_id: ", layer_id, " det: ", det, " histogram id: ", layer_id+det*16)
        allHistoDict["tracking_planes_hits_x_"+str(layer_id+det*16)].Fill(hitcellx, plotWeight)
        allHistoDict["tracking_planes_hits_Edep_"+str(layer_id+det*16)].Fill(energy, plotWeight)
        allHistoDict["tracking_planes_hits_y_"+str(layer_id+det*16)].Fill(hitcelly, plotWeight)
        allHistoDict["tracking_planes_hits_xy_"+str(layer_id+det*16)].Fill(hitcellx, hitcelly, plotWeight)
        
        if('-11' in pdgIdString and layer_id < 2):
            positronHit += 1
            totalPosHit += pdgIdString.count("-11")
        
        ### neutral particles
        neutralPdgIDSet = {'2112', '22', '111'}
        if(('2112' in pdgIdString) or ('22' in pdgIdString) or ('111' in pdgIdString)):
        #if(not (('-11' in pdgIdString) or ('11' in pdgIdString))):
            allHistoDict["tracking_planesneutral_hits_x_"+str(layer_id+det*16)].Fill(hitcellx, plotWeight)
            allHistoDict["tracking_planesneutral_hits_Edep_"+str(layer_id+det*16)].Fill(energy, plotWeight)
            allHistoDict["tracking_planesneutral_hits_y_"+str(layer_id+det*16)].Fill(hitcelly, plotWeight)
            allHistoDict["tracking_planesneutral_hits_xy_"+str(layer_id+det*16)].Fill(hitcellx, hitcelly, plotWeight)
            
        ### charged particles
        chargedPdgIDSet = {'2212', '1000140280', '1000140290', '1000140300', '-11', '11'}
        if(('2212' in pdgIdString) or ('-11' in pdgIdString) or ('11' in pdgIdString) or ('1000140280' in pdgIdString) or ('1000140290' in pdgIdString) or ('1000140300' in pdgIdString)):
        #if(('-11' in pdgIdString) or ('11' in pdgIdString)):
            allHistoDict["tracking_planescharged_hits_x_"+str(layer_id+det*16)].Fill(hitcellx, plotWeight)
            allHistoDict["tracking_planescharged_hits_Edep_"+str(layer_id+det*16)].Fill(energy, plotWeight)
            allHistoDict["tracking_planescharged_hits_y_"+str(layer_id+det*16)].Fill(hitcelly, plotWeight)
            allHistoDict["tracking_planescharged_hits_xy_"+str(layer_id+det*16)].Fill(hitcellx, hitcelly, plotWeight)
            
        
        if(('1000140280' in pdgIdString) or ('1000140290' in pdgIdString) or ('1000140300' in pdgIdString)):
            allHistoDict["tracking_planessilicon_hits_x_"+str(layer_id+det*16)].Fill(hitcellx, plotWeight)
            allHistoDict["tracking_planessilicon_hits_Edep_"+str(layer_id+det*16)].Fill(energy, plotWeight)
            allHistoDict["tracking_planessilicon_hits_y_"+str(layer_id+det*16)].Fill(hitcelly, plotWeight)
            allHistoDict["tracking_planessilicon_hits_xy_"+str(layer_id+det*16)].Fill(hitcellx, hitcelly, plotWeight)
            
        
    for keys in allHistoDict:
        allHistoDict[keys].Scale(1./nbx)
        allHistoDict[keys].Write()
    outFile.Close()
    
    print("total positron isolated hit: ", positronHit)
    print("total positron combined hit: ", totalPosHit)
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
