### setup to make plots for the tracker ###

import os, sys, glob, time
from ROOT import *
import argparse
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint
from collections import OrderedDict


def main():
    
    gROOT.SetBatch()
    
    parser = argparse.ArgumentParser(description='Code to get hit plots')
    parser.add_argument('-s', action="store", dest="inSignalFile", type=str, default="signalMC_b1gpc_HitBranchesForAllPix_SortedInEvents_Total10BX_HitsTimePerChipHistogram.root") ### default is phase 2 signal
    parser.add_argument('-b', action="store", dest="inBkgFile", type=str, default="ePlusLaserBackgroundTDR_list_root_7671ee4c_HitBranchesForAllPix_SortedInEvents_Total2p13BX_HitsTimePerChipHistogram.root")
    parser.add_argument('-g', action="store_true", dest="gPlusLaser")
    
    args                = parser.parse_args()
    needPhotonLaser     = args.gPlusLaser
    
    inDirectory         = "/Users/arkasantra/AllPix2/InputFiles/HitBranchesTxtFiles"
    inFileEPlusLaser    = TFile(inDirectory+"/"+args.inSignalFile)
    
    inBkgDirectory      = "/Users/arkasantra/AllPix2/InputFiles/HitBranchesTxtFiles"
    inFileEPlusLaserBkg = TFile(inBkgDirectory+"/"+args.inBkgFile)
    
    
    plotName = ""
    if needPhotonLaser:
        plotName = "gPlusLaserBackgroundAndSignal"
    else:
        plotName = "ePlusLaserBackgroundAndSignal"
    
    #inFileGPlusLaser   = TFile(inDirectory+"/gPlusLaserNewBkgSamples_hits.root")
    
    #directory = "TDR_Signal_Phase1_xi_10.0_TDR_Background_2p13BX_HitTracksPlots"
    directory = "TDR_EPlusLaserSignal_Phase1_xi10.0_10BX_TDR_EPlusLaserBackground_2p13BX_HitTimePlots"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    tracksPlot_EPlusLaser = OrderedDict()
    for hist in inFileEPlusLaser.GetListOfKeys():
        hName = hist.GetName()
        hNameStr = str(hName)
        histTH1 = inFileEPlusLaser.Get(hName)
        tracksPlot_EPlusLaser[hNameStr] = histTH1
    
    
    tracksPlot_EPlusLaserBkg = OrderedDict()
    for hist in inFileEPlusLaserBkg.GetListOfKeys():
        hName = hist.GetName()
        hNameStr = str(hName)
        histTH1 = inFileEPlusLaserBkg.Get(hName)
        tracksPlot_EPlusLaserBkg[hNameStr] = histTH1
    
    #### occupancy in hitcellx, positron side
    FirstTH1          = [];               FirstBkgTH1 = []
    SecondTH1         = [];               SecondBkgTH1 = []
    
    
    
    
    
    LegendName = [];             LegendNameBkg = [];
    SecondLegendName = [];       SecondLegendNameBkg = [];
    latexNameList1 = [];         latexNameList2 = [];
    PlotColor  = [];             PlotColorBkg = [];
    
    Stave0 = []; 
    Stave1 = []; 
    
    chip  = 0
    chip2 = 0
    for keys in tracksPlot_EPlusLaser:
        if ('tracking' not in keys): continue
        if (('log' in keys) or ('xy_edep' in keys)): continue
        if('tracking_planes_hits_timeLayer_0' in keys):
            Stave0.append(tracksPlot_EPlusLaser[keys])
        if('tracking_planes_hits_timeLayer_1' in keys):
            Stave1.append(tracksPlot_EPlusLaser[keys])
        #print(keys)
        chip_Layer0 = int(keys.split('_')[4])
        if(chip_Layer0%16 == 0):
            if('tracking_planes_hits_time_' in keys):FirstTH1.append(tracksPlot_EPlusLaser[keys])
            chip += 1
            LegendName.append("signal")
            latexNameList1.append("chip "+str(chip))
            PlotColor.append(kBlack)
            
        if(chip_Layer0%16 == 1):
            if('tracking_planes_hits_time_' in keys):SecondTH1.append(tracksPlot_EPlusLaser[keys])
            
            chip2 += 1
            SecondLegendName.append("signal")
            latexNameList2.append("chip "+str(chip2))
            
            
    for keys in tracksPlot_EPlusLaserBkg:
        chip_Layer0 = int(keys.split('_')[4])
        if('tracking_planes_hits_timeLayer_0' in keys):
            Stave0.append(tracksPlot_EPlusLaserBkg[keys])
        if('tracking_planes_hits_timeLayer_1' in keys):
            Stave1.append(tracksPlot_EPlusLaserBkg[keys])
        if(chip_Layer0%16 == 0):
            if('tracking_planes_hits_time_' in keys):FirstBkgTH1.append(tracksPlot_EPlusLaserBkg[keys])
            LegendNameBkg.append("background")
            PlotColorBkg.append(2)
            
        if(chip_Layer0%16 == 1):
            if('tracking_planes_hits_time_' in keys):SecondBkgTH1.append(tracksPlot_EPlusLaserBkg[keys])
            SecondLegendNameBkg.append("background")
            
            
            
    ### plot the positron side
    
    xAxisName    = "time [ns]"
    yAxisName    = "Particles/BX"
    xrange1down  = 0.0
    xrange1up    = 100.0
    yrange1down  = 0.6
    yrange1up    = 5e4
    yline1low    = 1.0
    yline1up     = 1.0
    drawline     = False
    logy         = True
    latexName2   = "Tracker Layer 1, Inner Stave"
    
    if needPhotonLaser:
        latexName3   = "positron side"
    else:
        latexName3   = ""
        
    leftLegend   = False
    doAtlas      = False
    doLumi       = False
    noRatio      = False
    do80         = False
    do59         = False
    drawPattern  = ""
    logz         = False
    logx         = False
    
    DrawHists9CanvasOverlay(FirstTH1, FirstBkgTH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageHits_"+plotName+"_Stave0_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    latexName2   = "Tracker Layer 1, Outer Stave"
    DrawHists9CanvasOverlay(SecondTH1, SecondBkgTH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageHits_"+plotName+"_Stave1_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    yrange1down  = 0.2
    latexName2   = "Tracker Layer 1, Inner Stave"
    
    DrawHists(Stave0, ['Signal','Background'], [kBlack,2],xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageHits_"+plotName+"_Layer1Inner_"+directory, yline1low, yline1up, drawline, logy, '', latexName2, latexName3)
    
    
    latexName2   = "Tracker Layer 1, Outer Stave"
    
    DrawHists(Stave1, ['Signal','Background'], [kBlack,2],xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageHits_"+plotName+"_Layer1Outer_"+directory, yline1low, yline1up, drawline, logy, '', latexName2, latexName3)
    
    
if __name__=="__main__":
    main()
