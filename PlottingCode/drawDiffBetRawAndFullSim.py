import os, sys, time
from ROOT import *
import pprint


def lyrFastSim2FullSim(layerId):
    lyrIDFS = -999
    if(layerId==3):
        lyrIDFS = 1
    elif(layerId==6):
        lyrIDFS = 0
    elif(layerId==9):
        lyrIDFS = 3
    elif(layerId==12):
        lyrIDFS = 2
    elif(layerId==15):
        lyrIDFS = 5
    elif(layerId==18):
        lyrIDFS = 4
    elif(layerId==21):
        lyrIDFS = 7
    elif(layerId==24):
        lyrIDFS = 6
    return lyrIDFS


def main():
    tracksInEachBX = {}
    #### open the text file containing FullSim info
    intextFile = "/Volumes/Study/Weizmann_PostDoc/AllPix2Study/InputFiles/HitBranchesTxtFiles/signalMC_e0ppw_3.0_HitBranchesForAllPix.txt"
    with open(intextFile) as filename:
        for lines in filename.readlines():
            lines = lines.rstrip()
            if "#" in lines:
                continue
            
            eachWord = lines.split()
            ### select only signal
            if(not(int(eachWord[7])==-11 and int(eachWord[8]) == 1)): continue
            bxNumber = eachWord[0]
            ptrackId = eachWord[9]
            layerId  = eachWord[10]
                
            tracksInEachBX.setdefault(ptrackId+"_"+layerId, []).append(lines)
    
    
    
    #pprint.pprint(tracksInEachBX)
    inFile = "/Users/arkasantra/arka/LUXE_Tracker_2021/ALPIDE.FastSim/data/root/raw/elaser/phase0/ppw/3.0/raw_elaser.root" 
    inRootFile = TFile(inFile,"READ")
    inTree = inRootFile.Get("tt")
    
    outFile = TFile("differenceFullSimRaw.root", "RECREATE")
    outFile.cd()
    
    eventCounter = 1
    
    
    
    dictTH1 = {}
    h_DeltaPx           = TH1D("h_DeltaPx_", "h_DeltaPx; (P_{xFullSim} - P_{xRaw}) [GeV]; Entries", 200, -0.4, 0.4)
    h_DeltaPxOverPx     = TH1D("h_DeltaPxOverPx_", "h_DeltaPxOverPx; (P_{xFullSim} - P_{xRaw})/P_{xRaw}; Entries", 500, -1, 1)
    h_DeltaPy           = TH1D("h_DeltaPy_", "h_DeltaPy; (P_{yFullSim} - P_{yRaw}) [GeV]; Entries", 200, -0.04, 0.04)
    h_DeltaPyOverPy     = TH1D("h_DeltaPyOverPy_", "h_DeltaPyOverPy; (P_{yFullSim} - P_{yRaw})/P_{yRaw}; Entries", 500, -1, 1)
    h_DeltaPz           = TH1D("h_DeltaPz_", "h_DeltaPz; (P_{zFullSim} - P_{zRaw}) [GeV]; Entries", 200, -0.05, 0.05)
    h_DeltaPzOverPz     = TH1D("h_DeltaPzOverPz_", "h_DeltaPzOverPz; (P_{zFullSim} - P_{zRaw})/P_{zRaw}; Entries", 500, -0.02, 0.02)
    h_DeltaE            = TH1D("h_DeltaE_", "h_DeltaE; E_{tr,FullSim} - E_{tr,Raw} [GeV]; Entries", 1000, -0.1, 0.1)
    h_DeltaECal         = TH1D("h_DeltaECal_", "h_DeltaECal; E_{tr,FullSim} - E_{tr,Cal} [GeV]; Entries", 1000, -0.1, 0.1)
    h_DeltaEOverE       = TH1D("h_DeltaEOverE_", "h_DeltaEOverE; (E_{tr,FullSim} - E_{tr,Raw})/E_{tr,Raw}; Entries", 500, -0.001, 0.001)
    h_Px_Raw            = TH1D("h_Px_Raw_", "h_Px_Raw; P_{xRaw} [GeV]; Entries", 1000, -0.01, 0.01)
    h_Px_FullSim        = TH1D("h_Px_FullSim_", "h_Px_FullSim; P_{xFullSim} [GeV]; Entries", 1000, -0.4, 0.4)
    
    
    dictTH1 = {"DeltaPx": h_DeltaPx, "DeltaPxOverPx": h_DeltaPxOverPx, "DeltaPy": h_DeltaPy, "DeltaPyOverPy": h_DeltaPyOverPy, "DeltaPz": h_DeltaPz, "DeltaPzOverPz": h_DeltaPzOverPz, "DeltaE": h_DeltaE, "DeltaEOverE": h_DeltaEOverE, "Px_Raw": h_Px_Raw, "Px_FullSim": h_Px_FullSim, "DeltaECal": h_DeltaECal}
    
    
    
    for event in inTree:
        for j in range(event.vx.size()):
            pxRaw = event.px[j]
            pyRaw = event.py[j]
            pzRaw = event.pz[j]
            ERaw = event.E[j]
            
            trkId   = event.trkId[j]
            
            ### look for the same track id in the Sasha's truth file
            
            dictKey = str(trkId)+"_"+str(0)
            if dictKey in tracksInEachBX:
                line   = tracksInEachBX[dictKey]
                eachWord  = line[0].split()
                pxFullSim = float(eachWord[19])
                pyFullSim = float(eachWord[20])
                pzFullSim = float(eachWord[21])
                EFullSim  = float(eachWord[15])
                meGeV = 0.5109989461/1000
                ECal = sqrt(pxFullSim*pxFullSim+pyFullSim*pyFullSim+pzFullSim*pzFullSim+meGeV*meGeV)
                
                #print("Match! with difference: ", x-xFullSim)
                #print("(xFastSim,yFastSim,zFastSim, EFastSim): (",x,",",y,",",z,",",E,")")
                #print("(xFullSim,yFullSim,zFullSim, EFullSim): (",xFullSim,",",yFullSim,",",zFullSim,",",eFullSim,")")
                
                dictTH1["DeltaPx"].Fill(pxFullSim-pxRaw)
                dictTH1["DeltaPxOverPx"].Fill((pxFullSim-pxRaw)/pxRaw)
                dictTH1["DeltaPy"].Fill(pyFullSim-pyRaw)
                dictTH1["DeltaPyOverPy"].Fill((pyFullSim-pyRaw)/pyRaw)
                dictTH1["DeltaPz"].Fill(pzFullSim-pzRaw)
                dictTH1["DeltaPzOverPz"].Fill((pzFullSim-pzRaw)/pzRaw)
                dictTH1["DeltaE"].Fill(EFullSim-ERaw)
                dictTH1["DeltaEOverE"].Fill((EFullSim-ERaw)/ERaw)
                dictTH1["Px_Raw"].Fill(pxRaw)
                dictTH1["Px_FullSim"].Fill(pxFullSim)
                dictTH1["DeltaECal"].Fill(EFullSim-ECal)
                
                #print("pxRaw=",pxRaw," pyRaw=",pyRaw," pzRaw=",pzRaw," ERaw=",ERaw," pxFS=",pxFullSim," pyFS=",pyFullSim," pzFS=",pzFullSim, " EFS=",EFullSim)
                    
        eventCounter += 1
            
    
    for THname in dictTH1:
        dictTH1[THname].Write()
        
    
    
if __name__=="__main__":
    main()

