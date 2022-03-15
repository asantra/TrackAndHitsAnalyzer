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

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def nonintersection(lst1, lst2):
    return list(set(lst1) ^ set(lst2))


def main():
    tracksInEachBX = {}
    tracksInEachStave = {}
    #### open the text file containing FullSim info
    intextFile = "/Volumes/Study/Weizmann_PostDoc/AllPix2Study/InputFiles/HitBranchesTxtFiles/signalMC_e0gpc_5.0_NoExtraVacuumWindow_OneFile_HitBranchesForAllPix.txt"
    positronNumber = 0
    trackIdFullSim = []
    trackIdFastSim = []
    uniqueTrackFullSimStave0 = set()
    uniqueTrackFullSimStave1 = set()
    uniqueTrackFastSimStave0 = set()
    uniqueTrackFastSimStave1 = set()
    
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
            if int(layerId) == 0 or int(layerId) == 1: 
                if int(layerId) == 0:
                    uniqueTrackFullSimStave0.add(int(ptrackId))
                if int(layerId) == 1:
                    uniqueTrackFullSimStave1.add(int(ptrackId))
                    
                positronNumber += 1
                trackIdFullSim.append(int(ptrackId))
    
    print("positron Number in FullSim: ", positronNumber)
    
    morethanone = 0
    for keys in tracksInEachBX:
        if len(tracksInEachBX[keys]) > 1:
            layerIdFullSim = int(keys.split('_')[1])
            if(layerIdFullSim == 0 or layerIdFullSim == 1): morethanone += 1
    
    print("more than one entry on first layer: ", morethanone)
    
    inFile = "/Users/arkasantra/arka/LUXE_Tracker_2021/ALPIDE.FastSim/data/root/dig/elaser/phase0/gpc/5.0/dig_elaser_.root" 
    inRootFile = TFile(inFile,"READ")
    inTree = inRootFile.Get("dig_Pside")
    
    outFile = TFile("differenceFullSimFastSim_elaser_phase0_5p0.root", "RECREATE")
    outFile.cd()
    
    
    
    dictTH1 = {}
    for layers in range(0,7+1):
        h_DeltaX        = TH1D("h_DeltaX_"+str(layers), "h_DeltaX; x_{FullSim} - x_{FastSim} [mm]; Entries", 100, -8, 8)
        h_DeltaXOverX   = TH1D("h_DeltaXOverX_"+str(layers), "h_DeltaXOverX; (x_{FullSim} - x_{FastSim})/x_{FastSim} [mm]; Entries", 500, -0.02, 0.02)
        h_DeltaY        = TH1D("h_DeltaY_"+str(layers), "h_DeltaY; y_{FullSim} - y_{FastSim} [mm]; Entries", 100, -8, 8)
        h_DeltaYOverY   = TH1D("h_DeltaYOverY_"+str(layers), "h_DeltaYOverY; (y_{FullSim} - y_{FastSim})/y_{FastSim} [mm]; Entries", 500, -0.02, 0.02)
        h_DeltaE        = TH1D("h_DeltaE_"+str(layers), "h_DeltaE; E_{tr,FullSim} - E_{tr,FastSim} [mm]; Entries", 1000, -0.1, 0.1)
        h_DeltaEOverE   = TH1D("h_DeltaEOverE_"+str(layers), "h_DeltaEOverE; (E_{tr,FullSim} - E_{tr,FastSim})/E_{tr,FastSim} [mm]; Entries", 500, -0.001, 0.001)
        dictTH1[layers] = {"DeltaX": h_DeltaX, "DeltaXOverX": h_DeltaXOverX, "DeltaY": h_DeltaY, "DeltaYOverY": h_DeltaYOverY, "DeltaE": h_DeltaE, "DeltaEOverE": h_DeltaEOverE}
    
    
    
    for event in inTree:
        matched      = 0
        unmatched    = 0
        for nTrks in range(event.clusters_r.size()):
            for j in range(event.clusters_r[nTrks].size()):
                x = event.clusters_r[nTrks][j].X()*10
                y = event.clusters_r[nTrks][j].Y()*10
                z = event.clusters_r[nTrks][j].Z()*10
                E = event.trkp4[nTrks].E()
                
                trkId   = event.trkID[nTrks]
                layerId = event.clusters_layerid[nTrks][j]
                
                lyrIdFS = lyrFastSim2FullSim(layerId)
                if lyrIdFS==-999: continue
                #### select only the first layer
                if int(lyrIdFS) > 1: continue
            
                if int(lyrIdFS) == 0:
                    uniqueTrackFastSimStave0.add(int(trkId))
                if int(lyrIdFS) == 1:
                    uniqueTrackFastSimStave1.add(int(trkId))
                    
                trackIdFastSim.append(int(trkId))
                
                dictKey = str(trkId)+"_"+str(lyrIdFS)
                if dictKey in tracksInEachBX:
                    if(layerId==3 or layerId==6): matched += 1
                    line   = tracksInEachBX[dictKey]
                    words  = line[0].split()
                    xFullSim = float(words[3])
                    yFullSim = float(words[4])
                    zFullSim = float(words[5])
                    eFullSim = float(words[15])
                    
                    #print("Match! with difference: ", x-xFullSim)
                    #print("(xFastSim,yFastSim,zFastSim, EFastSim): (",x,",",y,",",z,",",E,")")
                    #print("(xFullSim,yFullSim,zFullSim, EFullSim): (",xFullSim,",",yFullSim,",",zFullSim,",",eFullSim,")")
                    
                    dictTH1[lyrIdFS]["DeltaX"].Fill(xFullSim-x)
                    dictTH1[lyrIdFS]["DeltaXOverX"].Fill((xFullSim-x)/x)
                    dictTH1[lyrIdFS]["DeltaY"].Fill(yFullSim-y)
                    dictTH1[lyrIdFS]["DeltaYOverY"].Fill((yFullSim-y)/y)
                    dictTH1[lyrIdFS]["DeltaE"].Fill(eFullSim-E)
                    dictTH1[lyrIdFS]["DeltaEOverE"].Fill((eFullSim-E)/E)
                else:
                    if(layerId==3 or layerId==6): unmatched += 1
                    
     
    print("matched tracks          ", matched)
    print("unmatched tracks        ", unmatched)
    
    
    for keys in dictTH1:
        for THname in dictTH1[keys]:
            dictTH1[keys][THname].Write()
        
        
    intersectionPositron = intersection(trackIdFastSim, trackIdFullSim)
    nonintersectionPositron = nonintersection(trackIdFastSim, trackIdFullSim)
    
    print("positrons in both fullsim and fastsim ", len(intersectionPositron))
    print("positrons not in both fullsim and fastsim ", len(nonintersectionPositron))
    print("non intersection positron tracks ", nonintersectionPositron)
    print("unique positrons in FullSim Stave 0 and 1 ", len(uniqueTrackFullSimStave0), ", ", len(uniqueTrackFullSimStave1))
    print("unique positrons in FastSim Stave 0 and 1 ", len(uniqueTrackFastSimStave0), ", ", len(uniqueTrackFastSimStave1))
    
    
if __name__=="__main__":
    main()

