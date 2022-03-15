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
    parser.add_argument('-s', action="store", dest="inSignalFile", type=str, default="signalMC_b1gpc_HitsInfo_SortedInEvents_Total10BX_HitsPerChipHistogram.root") ### default is phase 2 signal
    parser.add_argument('-b', action="store", dest="inBkgFile", type=str, default="ePlusLaserBackgroundTDR_list_root_7671ee4c_HitsInfo_SortedInEvents_Total2p13BX_HitsPerChipHistogram.root")
    parser.add_argument('-g', action="store_true", dest="gPlusLaser")
    
    args                = parser.parse_args()
    needPhotonLaser     = args.gPlusLaser
    
    inDirectory         = "/Users/arkasantra/arka/Sasha_Work/OutputFile/HitsTextFiles"
    inFileEPlusLaser    = TFile(inDirectory+"/"+args.inSignalFile)
    
    inBkgDirectory      = "/Users/arkasantra/arka/Sasha_Work/OutputFile/HitsTextFiles"
    inFileEPlusLaserBkg = TFile(inBkgDirectory+"/"+args.inBkgFile)
    
    
    plotName = ""
    if needPhotonLaser:
        plotName = "gPlusLaserBackgroundAndSignal"
    else:
        plotName = "ePlusLaserBackgroundAndSignal"
    
    #inFileGPlusLaser   = TFile(inDirectory+"/gPlusLaserNewBkgSamples_hits.root")
    
    directory = "TDR_Signal_Phase0_xi_3.0ppw_NoWeight_TDR_Background_2p13BX_HitTracksPlots"
    #directory = "TDR_EPlusLaserSignal_Phase1_xi10.0_10BX_TDR_EPlusLaserBackground_2p13BX_HitTracksPlots_NotWeighted"
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
    FirstNeutralTH1   = [];               FirstBkgNeutralTH1 = []
    SecondNeutralTH1  = [];               SecondBkgNeutralTH1 = []
    FirstChargedTH1   = [];               FirstBkgChargedTH1 = []
    SecondChargedTH1  = [];               SecondBkgChargedTH1 = []
    FirstSiliconTH1   = [];               FirstBkgSiliconTH1 = []
    SecondSiliconTH1  = [];               SecondBkgSiliconTH1 = []
    
    
    #### depositedEnergy, positron side
    FirstETH1   = [];                     FirstBkgETH1 = []
    SecondETH1  = [];                     SecondBkgETH1 = []
    
    
    
    #### occupancy in hitcellx, electron side
    FirstElectronTH1          = [];       FirstElectronBkgTH1 = []
    SecondElectronTH1         = [];       SecondElectronBkgTH1 = []
    FirstElectronNeutralTH1   = [];       FirstElectronBkgNeutralTH1 = []
    SecondElectronNeutralTH1  = [];       SecondElectronBkgNeutralTH1 = []
    FirstElectronChargedTH1   = [];       FirstElectronBkgChargedTH1 = []
    SecondElectronChargedTH1  = [];       SecondElectronBkgChargedTH1 = []
    FirstElectronSiliconTH1   = [];       FirstElectronBkgSiliconTH1 = []
    SecondElectronSiliconTH1  = [];       SecondElectronBkgSiliconTH1 = []
    
    
    #### depositedEnergy, electron side
    FirstElectronETH1   = [];       FirstElectronBkgETH1 = []
    SecondElectronETH1  = [];       SecondElectronBkgETH1 = []
    
    #### 2D plot
    FirstTH2 = [];   FirstBkgTH2 = []
    
    
    LegendName = [];       LegendNameBkg = [];
    SecondLegendName = []; SecondLegendNameBkg = [];
    latexNameList1 = [];   latexNameList2 = [];
    PlotColor  = [];       PlotColorBkg = [];
    
    chip  = 0
    chip2 = 0
    for keys in tracksPlot_EPlusLaser:
        if ('tracking' not in keys): continue
        if (('log' in keys) or ('xy_edep' in keys)): continue
        #print(keys)
        chip_Layer0 = int(keys.split('_')[4])
        if(chip_Layer0%16 == 0):
            if('tracking_planes_hits_x_' in keys):FirstTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planes_hits_Edep' in keys):FirstETH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planesneutral_hits_x_' in keys): FirstNeutralTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planescharged_hits_x_' in keys): FirstChargedTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planessilicon_hits_x_' in keys): FirstSiliconTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planes_hits_xy_' in keys):
                FirstTH2.append(tracksPlot_EPlusLaser[keys])
                binContent   = 0
                binNumberHit = 0
                for i in range(0, tracksPlot_EPlusLaser[keys].GetNbinsX()+1):
                    for j in range(0, tracksPlot_EPlusLaser[keys].GetNbinsY()+1):
                        if(tracksPlot_EPlusLaser[keys].GetBinContent(i,j) > 0):
                            binContent   += tracksPlot_EPlusLaser[keys].GetBinContent(i,j)
                            binNumberHit += 1
                if(binNumberHit!=0): averageOccupancy = binContent/binNumberHit
                else: averageOccupancy = 0
                print("Average occupancy for signal: ", averageOccupancy, " for chipLayer ", chip_Layer0)
            
            chip += 1
            LegendName.append("signal")
            latexNameList1.append("chip "+str(chip))
            PlotColor.append(kBlack)
            
        if(chip_Layer0%16 == 1):
            if('tracking_planes_hits_x_' in keys):SecondTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planes_hits_Edep' in keys):SecondETH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planesneutral_hits_x_' in keys): SecondNeutralTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planescharged_hits_x_' in keys): SecondChargedTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planessilicon_hits_x_' in keys): SecondSiliconTH1.append(tracksPlot_EPlusLaser[keys])
            
            chip2 += 1
            SecondLegendName.append("signal")
            latexNameList2.append("chip "+str(chip2))
            PlotColor.append(kBlack)
            
            
            
        if(chip_Layer0%16 == 8):
            if('tracking_planes_hits_x_' in keys):FirstElectronTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planes_hits_Edep' in keys):FirstElectronETH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planesneutral_hits_x_' in keys): FirstElectronNeutralTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planescharged_hits_x_' in keys): FirstElectronChargedTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planessilicon_hits_x_' in keys): FirstElectronSiliconTH1.append(tracksPlot_EPlusLaser[keys])
            
            
        if(chip_Layer0%16 == 9):
            if('tracking_planes_hits_x_' in keys):SecondElectronTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planes_hits_Edep' in keys):SecondElectronETH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planesneutral_hits_x_' in keys): SecondElectronNeutralTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planescharged_hits_x_' in keys): SecondElectronChargedTH1.append(tracksPlot_EPlusLaser[keys])
            if('tracking_planessilicon_hits_x_' in keys): SecondElectronSiliconTH1.append(tracksPlot_EPlusLaser[keys])
            
            
            
            
            
    for keys in tracksPlot_EPlusLaserBkg:
        if ('tracking' not in keys): continue
        if (('log' in keys) or ('xy_edep' in keys)): continue
        chip_Layer0 = int(keys.split('_')[4])
        
        if(chip_Layer0%16 == 0):
            if('tracking_planes_hits_x_' in keys):FirstBkgTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planes_hits_Edep' in keys):FirstBkgETH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planesneutral_hits_x_' in keys): FirstBkgNeutralTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planescharged_hits_x_' in keys): FirstBkgChargedTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planessilicon_hits_x_' in keys): FirstBkgSiliconTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planes_hits_xy_' in keys):FirstBkgTH2.append(tracksPlot_EPlusLaserBkg[keys])
            
            
            LegendNameBkg.append("background")
            PlotColorBkg.append(2)
            
        if(chip_Layer0%16 == 1):
            if('tracking_planes_hits_x_' in keys):SecondBkgTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planes_hits_Edep' in keys):SecondBkgETH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planesneutral_hits_x_' in keys): SecondBkgNeutralTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planescharged_hits_x_' in keys): SecondBkgChargedTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planessilicon_hits_x_' in keys): SecondBkgSiliconTH1.append(tracksPlot_EPlusLaserBkg[keys])
            
            SecondLegendNameBkg.append("background")
            PlotColorBkg.append(2)
            
            
        if(chip_Layer0%16 == 8):
            if('tracking_planes_hits_x_' in keys):FirstElectronBkgTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planes_hits_Edep' in keys):FirstElectronBkgETH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planesneutral_hits_x_' in keys): FirstElectronBkgNeutralTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planescharged_hits_x_' in keys): FirstElectronBkgChargedTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planessilicon_hits_x_' in keys): FirstElectronBkgSiliconTH1.append(tracksPlot_EPlusLaserBkg[keys])
            
        if(chip_Layer0%16 == 9):
            if('tracking_planes_hits_x_' in keys):SecondElectronBkgTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planes_hits_Edep' in keys):SecondElectronBkgETH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planesneutral_hits_x_' in keys): SecondElectronBkgNeutralTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planescharged_hits_x_' in keys): SecondElectronBkgChargedTH1.append(tracksPlot_EPlusLaserBkg[keys])
            if('tracking_planessilicon_hits_x_' in keys): SecondElectronBkgSiliconTH1.append(tracksPlot_EPlusLaserBkg[keys])
            
            
            
    ### plot the positron side
    
    xAxisName    = "Pixel column number"
    yAxisName    = "Number of pixels (with Edep>0)/BX"
    xrange1down  = 0.0
    xrange1up    = 1030.0
    yrange1down  = 3e-2
    yrange1up    = 7e3
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
    
    latexName2   = "Tracker Layer 1, Inner Stave, Neutral"
    DrawHists9CanvasOverlay(FirstNeutralTH1, FirstBkgNeutralTH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/NeutralParticles_"+plotName+"_Stave0_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    latexName2   = "Tracker Layer 1, Outer Stave, Neutral"
    DrawHists9CanvasOverlay(SecondNeutralTH1, SecondBkgNeutralTH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/NeutralParticles_"+plotName+"_Stave1_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    
    latexName2   = "Tracker Layer 1, Inner Stave, Charged"
    DrawHists9CanvasOverlay(FirstChargedTH1, FirstBkgChargedTH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/ChargedParticles_"+plotName+"_Stave0_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    latexName2   = "Tracker Layer 1, Outer Stave, Charged"
    DrawHists9CanvasOverlay(SecondChargedTH1, SecondBkgChargedTH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/ChargedParticles_"+plotName+"_Stave1_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    
    
    latexName2   = "Tracker Layer 1, Inner Stave, Silicon"
    DrawHists9CanvasOverlay(FirstSiliconTH1, FirstBkgSiliconTH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/SiliconParticles_"+plotName+"_Stave0_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    latexName2   = "Tracker Layer 1, Outer Stave, Silicon"
    DrawHists9CanvasOverlay(SecondSiliconTH1, SecondBkgSiliconTH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/SiliconParticles_"+plotName+"_Stave1_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    
    
    
    xAxisName    = "E_{dep} [GeV]"
    xrange1down  = 1e-7
    xrange1up    = 20.0
    yrange1down  = 1e-1
    yrange1up    = 7e5
    logx         = True
    
    
    latexName2   = "Tracker Layer 1, Inner Stave"
    
    DrawHists9CanvasOverlay(FirstETH1, FirstBkgETH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageEnergyDeposition_"+plotName+"_Stave0_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    latexName2   = "Tracker Layer 1, Outer Stave"
    DrawHists9CanvasOverlay(SecondETH1, SecondBkgETH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageEnergyDeposition_"+plotName+"_Stave1_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
    
    latexName2   = "Tracker Layer 1, Inner Stave"
    logy = False
    leftLegend = True
    DrawHists9Canvas(FirstTH2, LegendName, PlotColor, "x [pixel]", "y [pixel]", 0, 1024, 0, 512, directory+"/AverageHits2DPlotsSignal_"+plotName+"_Stave0_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, "COLZ", logz)
    
    DrawHists9Canvas(FirstBkgTH2, LegendNameBkg, PlotColor, "x [pixel]", "y [pixel]", 0, 1024, 0, 512, directory+"/AverageHits2DPlotsBackground_"+plotName+"_Stave0_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, "COLZ", logz)
    
    
    ### plot the electron side of the tracker only when needed
    if needPhotonLaser:
        xAxisName    = "Pixel column number"
        yAxisName    = "Number of pixels (with Edep>0)/BX"
        xrange1down  = 0.0
        xrange1up    = 1030.0
        yrange1down  = 3e-2
        yrange1up    = 7e3
        yline1low    = 1.0
        yline1up     = 1.0
        drawline     = False
        logy         = True
        #latexName    = ""
        latexName2   = "Tracker Layer 1, Inner Stave"
        latexName3   = "electron side"
        leftLegend   = False
        doAtlas      = False
        doLumi       = False
        noRatio      = False
        do80         = False
        do59         = False
        drawPattern  = ""
        logz         = False
        logx         = False
        
        DrawHists9CanvasOverlay(FirstElectronTH1, FirstElectronBkgTH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageHits_"+plotName+"_Stave0_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        latexName2   = "Tracker Layer 1, Outer Stave"
        DrawHists9CanvasOverlay(SecondElectronTH1, SecondElectronBkgTH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageHits_"+plotName+"_Stave1_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        latexName2   = "Tracker Layer 1, Inner Stave, Neutral"
        DrawHists9CanvasOverlay(FirstElectronNeutralTH1, FirstElectronBkgNeutralTH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/NeutralParticles_"+plotName+"_Stave0_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        latexName2   = "Tracker Layer 1, Outer Stave, Neutral"
        DrawHists9CanvasOverlay(SecondElectronNeutralTH1, SecondElectronBkgNeutralTH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/NeutralParticles_"+plotName+"_Stave1_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        
        latexName2   = "Tracker Layer 1, Inner Stave, Charged"
        DrawHists9CanvasOverlay(FirstElectronChargedTH1, FirstElectronBkgChargedTH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/ChargedParticles_"+plotName+"_Stave0_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        latexName2   = "Tracker Layer 1, Outer Stave, Charged"
        DrawHists9CanvasOverlay(SecondElectronChargedTH1, SecondElectronBkgChargedTH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/ChargedParticles_"+plotName+"_Stave1_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        
        
        latexName2   = "Tracker Layer 1, Inner Stave, Silicon"
        DrawHists9CanvasOverlay(FirstElectronSiliconTH1, FirstElectronBkgSiliconTH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/SiliconParticles_"+plotName+"_Stave0_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        latexName2   = "Tracker Layer 1, Outer Stave, Silicon"
        DrawHists9CanvasOverlay(SecondElectronSiliconTH1, SecondElectronBkgSiliconTH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/SiliconParticles_"+plotName+"_Stave1_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        
        
        
        xAxisName    = "E_{dep} [GeV]"
        xrange1down  = 1e-7
        xrange1up    = 20.0
        yrange1down  = 1e-1
        yrange1up    = 7e5
        logx         = True
        
        
        latexName2   = "Tracker Layer 1, Inner Stave"
        
        DrawHists9CanvasOverlay(FirstElectronETH1, FirstElectronBkgETH1, LegendName, LegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageEnergyDeposition_"+plotName+"_Stave0_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList1, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
        
        latexName2   = "Tracker Layer 1, Outer Stave"
        DrawHists9CanvasOverlay(SecondElectronETH1, SecondElectronBkgETH1, SecondLegendName, SecondLegendNameBkg, PlotColor, PlotColorBkg, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageEnergyDeposition_"+plotName+"_Stave1_ElectronSide_"+directory, yline1low, yline1up, drawline, logy, latexNameList2, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx)
            
    
    '''
    #### for g+laser background
    tracksPlot_GPlusLaser = OrderedDict()
    
    for hist in inFileGPlusLaser.GetListOfKeys():
        hName = hist.GetName()
        hNameStr = str(hName)
        if (("tracking_planes_hits_x_aftervtxcut" not in hNameStr)): continue
        histTH1 = inFileGPlusLaser.Get(hName)
        histTH1.Scale(1./40)
        tracksPlot_GPlusLaser[hName] = histTH1
        
        
    #pprint.pprint(tracksPlot_EPlusLaser)
    FirstTH1   = []
    SecondTH1  = []
    LegendName = []
    PlotColor  = []
    chip  = 0
    chip2 = 0
    for keys in tracksPlot_GPlusLaser:
        chip_Layer0 = int(keys.split('_')[5])
        if(chip_Layer0%16 == 0):
            #print(keys)
            FirstTH1.append(tracksPlot_GPlusLaser[keys])
            chip += 1
            LegendName.append("chip "+str(chip))
            PlotColor.append(2)
            
        if(chip_Layer0%16 == 1):
            #print(keys)
            SecondTH1.append(tracksPlot_GPlusLaser[keys])
            chip2 += 1
            LegendName.append("chip "+str(chip))
            PlotColor.append(2)
            
            
    latexName2   = "Tracker Layer 1, Inner Stave"
    latexName3   = "g+laser background"
    DrawHists9Canvas(FirstTH1, LegendName, PlotColor, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageHits_gPlusLaserBackground_Stave0", yline1low, yline1up, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz)
    
    
    latexName2   = "Tracker Layer 1, Outer Stave"
    latexName3   = "g+laser background"
    DrawHists9Canvas(FirstTH1, LegendName, PlotColor, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/AverageHits_gPlusLaserBackground_Stave1", yline1low, yline1up, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz)
    '''
    
    
if __name__=="__main__":
    main()
