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
    
    #pprint.pprint(tracksInEachBX)
    inFile = "/Users/arkasantra/arka/LUXE_Tracker_2021/ALPIDE.FastSim/data/root/dig/elaser/phase0/ppw/3.0/dig_elaser_SoftEdgeMagField.root" 
    inRootFile = TFile(inFile,"READ")
    inTree = inRootFile.Get("dig_Pside")
    
    
    inSharpFile     = "/Users/arkasantra/arka/LUXE_Tracker_2021/ALPIDE.FastSim/data/root/dig/elaser/phase0/ppw/3.0/dig_elaser_SharpEdgeMagField.root" 
    inSharpRootFile = TFile(inSharpFile,"READ")
    inSharpTree     = inSharpRootFile.Get("dig_Pside")
    
    outFile = TFile("differenceSoftEdgeSharpEdgeMagField.root", "RECREATE")
    outFile.cd()
    
    dictTH1 = {}
    h_DeltaX           = TH1D("h_DeltaX", "h_DeltaX; (x_{Sharp} - x_{Soft}) [mm]; Entries", 200, -2, 2)
    h_DeltaE           = TH1D("h_DeltaE", "h_DeltaE; (E_{Sharp} - E_{Soft}) [mm]; Entries", 200, -2, 2)
    
    
    dictTH1 = {"DeltaX": h_DeltaX, "DeltaE": h_DeltaE}
    
    
    dictSoftMagField = {}
    for event in inTree:
        for nTrks in range(event.clusters_r.size()):
            for j in range(event.clusters_r[nTrks].size()):
                x = event.clusters_r[nTrks][j].X()*10
                y = event.clusters_r[nTrks][j].Y()*10
                z = event.clusters_r[nTrks][j].Z()*10
                E = event.trkp4[nTrks].E()
                
                trkId   = event.trkID[nTrks]
                layerId = event.clusters_layerid[nTrks][j]
                
                if(layerId==6):
                    dictSoftMagField[trkId] = {"x":x, "y":y, "z":z, "E":E}
                    
                    
    dictSharpMagField = {}
    for eventS in inSharpTree:
        for nTrksS in range(eventS.clusters_r.size()):
            for j in range(eventS.clusters_r[nTrksS].size()):
                x = eventS.clusters_r[nTrksS][j].X()*10
                y = eventS.clusters_r[nTrksS][j].Y()*10
                z = eventS.clusters_r[nTrksS][j].Z()*10
                E = eventS.trkp4[nTrksS].E()
                
                trkIdS   = eventS.trkID[nTrksS]
                layerIdS = eventS.clusters_layerid[nTrksS][j]
                
                if(layerIdS==6):
                    dictSharpMagField[trkIdS] = {"x":x, "y":y, "z":z, "E":E}
            

            
    for key in dictSoftMagField:
        if key in dictSharpMagField:
            xSoft  = dictSoftMagField[key]["x"]
            xSharp = dictSharpMagField[key]["x"]
            eSoft  = dictSoftMagField[key]["E"]
            eSharp = dictSharpMagField[key]["E"]
            dictTH1["DeltaX"].Fill(xSharp - xSoft)
            dictTH1["DeltaE"].Fill(eSharp - eSoft)
                    
            
    
    for THname in dictTH1:
        dictTH1[THname].Write()
        
    
    
if __name__=="__main__":
    main()

