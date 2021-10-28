### setup to make plots for the tracker ###
### This is to plot four particles on top of each other in tracker layer 1 and layer 4. 

import os, sys, glob, time
from ROOT import *
import argparse
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint





def main():
    gROOT.LoadMacro("LuxeStyle.C")
    gROOT.LoadMacro("LuxeLabels.C")
    gROOT.SetBatch()
    SetLuxeStyle()
    inputDir            = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inputTracksRootFile = sys.argv[1]
    eLaserHicsRootFile  = "list_root_hics_165gev_w0_3000nm_WIS.root"
    eLaserHicsFile      = TFile(inputDir+"/"+eLaserHicsRootFile)
    
    plotSuffixName      = ""
    if (("_" in inputTracksRootFile) and ("All" not in inputTracksRootFile)):
        eachName            = inputTracksRootFile.split('.')[0].split('_')
        inTracksFile        = TFile(inputDir+"/"+inputTracksRootFile)
        suffixName          = "_".join(eachName[2:])
        outDir              = "DistributionPlotsCDR_"+suffixName
        plotSuffixName      = suffixName
    else:
        inTracksFile        = TFile(inputDir+"/"+inputTracksRootFile)
        outDir              = "DistributionPlotsLikeCDR_"+inputTracksRootFile.split('.')[0]
        plotSuffixName      = inputTracksRootFile.split('.')[0]
    
    
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    baseHistogramNames  = {}
    
    
    baseHistogramNames["tracking_planes_background_track_x_gamma"]                           = ["X positions [mm]", "Particles/BX", 0.0, 600.0, 1e-5, 1e7, True, "hist", False, False]
    baseHistogramNames["tracking_planes_background_track_x_electrons"]                       = ["X positions [mm]", "Particles/BX", 0.0, 600.0, 1e-5, 1e7, True, "hist", False, False]
    baseHistogramNames["tracking_planes_background_track_x_positrons"]                       = ["X positions [mm]", "Particles/BX", 0.0, 600.0, 1e-5, 1e7, True, "hist", False, False]
    baseHistogramNames["tracking_planes_signal_track_x_positrons"]                           = ["X positions [mm]", "Particles/BX", 0.0, 600.0, 1e-5, 1e7, True, "hist", False, False]
    
    baseHistogramNames["tracking_planes_background_track_x_gamma_sumE"]                      = ["X positions [mm]", "#sum E/BX [GeV]", 0.0, 600.0, 1e-5, 1e3, True, "hist", False, False]
    baseHistogramNames["tracking_planes_background_track_x_electrons_sumE"]                  = ["X positions [mm]", "#sum E/BX [GeV]", 0.0, 600.0, 1e-5, 1e3, True, "hist", False, False]
    baseHistogramNames["tracking_planes_background_track_x_positrons_sumE"]                  = ["X positions [mm]", "#sum E/BX [GeV]", 0.0, 600.0, 1e-5, 1e3, True, "hist", False, False]
    baseHistogramNames["tracking_planes_signal_track_x_positrons_sumE"]                      = ["X positions [mm]", "#sum E/BX [GeV]", 0.0, 600.0, 1e-5, 1e3, True, "hist", False, False]
    
    
    
    
    ### non signal plots, have 8 components for each histogram
    histogramDict = {}
    signalHistogramDict = {}
    backgroundHistogramDict = {}
    
    for name in baseHistogramNames:
        eachBaseHistogramPlot = []
        for i in range(0,8):
            h = inTracksFile.Get(name+"_"+str(i))
            checkType = str(type(h))
            if (("TH1" in checkType) or ("TH2" in checkType)):
                eachBaseHistogramPlot.append(h)
            
        if ("signal" in name):
            signalHistogramDict[name] = eachBaseHistogramPlot
        elif("background" in name):
            backgroundHistogramDict[name] = eachBaseHistogramPlot
        else:
            histogramDict[name] = eachBaseHistogramPlot
            
    
    #### elaser hics plots, we want just the signal
    eLaserSignalHistogramDict     = {}
    eLaserBackgroundHistogramDict = {}
    eLaserDict                    = {}
    for name in baseHistogramNames:
        eachBaseHistogramPlot1 = []
        for i in range(0,8):
            h = eLaserHicsFile.Get(name+"_"+str(i))
            checkType = str(type(h))
            if (("TH1" in checkType) or ("TH2" in checkType)):
                eachBaseHistogramPlot1.append(h)
            
        if ("signal" in name):
            eLaserSignalHistogramDict[name]     = eachBaseHistogramPlot1
        elif("background" in name):
            eLaserBackgroundHistogramDict[name] = eachBaseHistogramPlot1
        else:
            eLaserDict[name] = eachBaseHistogramPlot1
            
    ### signal or background histogram, only one component for each one
    
    #### plotting the signal and background
    drawline    = False
    latexName   = ''
    latexName2  = 'Layer 1'
    latexName3  = ''
    leftLegend  = True
    doAtlas     = False
    doLumi      = False
    noRatio     = False
    do80        = False
    do59        = False
    
    
    
    PlotColor1  = [2, 4, kGreen+3, kGray, 2, 4, kGreen+3, kGray+1]
    
    #### plotting the layer 0, first layer
    LegendName1 = []
    for stave in range(0,2):
        LegendName1.append("#gamma, Bkg, Stave "+str(stave))
        LegendName1.append("e^{-}, Bkg, Stave "+str(stave))
        LegendName1.append("e^{+}, Bkg, Stave "+str(stave))
        LegendName1.append("e^{+}, Sig, Stave "+str(stave))
    
    
    
    fourKeyName = ["tracking_planes_background_track_x_gamma_sumE", "tracking_planes_background_track_x_electrons_sumE", "tracking_planes_background_track_x_positrons_sumE", "tracking_planes_signal_track_x_positrons_sumE"]
    
    logy        = False
    if baseHistogramNames[fourKeyName[0]][6]:
        logy = True
        print ("I am in ", fourKeyName[0])
    
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    
    ### overlay e+laser signal on top of electron beam only plot
    if(("electronBackground" in plotSuffixName) or ("EBeamOnly" in plotSuffixName)):
        FirstTH1   += eLaserSignalHistogramDict[fourKeyName[3]] 
    else:
        FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    print (len(FirstTH1))
    OnlyLayer1  = [FirstTH1[0], FirstTH1[8], FirstTH1[16], FirstTH1[24]]
    OnlyLayer1 += [FirstTH1[1], FirstTH1[9], FirstTH1[17], FirstTH1[25]]        
    
    DrawHistsOneCanvas(OnlyLayer1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_Layer1"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], baseHistogramNames[fourKeyName[0]][9])
    
    
    fourKeyName = ["tracking_planes_background_track_x_gamma", "tracking_planes_background_track_x_electrons", "tracking_planes_background_track_x_positrons", "tracking_planes_signal_track_x_positrons"]
    
    
    logy        = False
    if baseHistogramNames[fourKeyName[0]][6]:
        logy = True
        print ("I am in ", fourKeyName[0]) 
    
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    ### overlay e+laser signal on top of electron beam only plot
    if("electronBackground" in plotSuffixName):
        FirstTH1   += eLaserSignalHistogramDict[fourKeyName[3]] 
    else:
        FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    OnlyLayer1 = [FirstTH1[0], FirstTH1[8], FirstTH1[16], FirstTH1[24]]
    OnlyLayer1 += [FirstTH1[1], FirstTH1[9], FirstTH1[17], FirstTH1[25]]        
    
    DrawHistsOneCanvas(OnlyLayer1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_Layer1"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], baseHistogramNames[fourKeyName[0]][9])
    
    
    
    
    
    
    
    latexName2   = 'Layer 4'
    
    #### plotting the layer 1, first layer
    LegendName1 = []
    for stave in range(6,8):
        LegendName1.append("#gamma, Bkg, Stave "+str(stave))
        LegendName1.append("e^{-}, Bkg, Stave "+str(stave))
        LegendName1.append("e^{+}, Bkg, Stave "+str(stave))
        LegendName1.append("e^{+}, Sig, Stave "+str(stave))
    
    
    
    fourKeyName = ["tracking_planes_background_track_x_gamma_sumE", "tracking_planes_background_track_x_electrons_sumE", "tracking_planes_background_track_x_positrons_sumE", "tracking_planes_signal_track_x_positrons_sumE"]
    
    logy        = False
    if baseHistogramNames[fourKeyName[0]][6]:
        logy = True
        print ("I am in ", fourKeyName[0]) 
    
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    ### overlay e+laser signal on top of electron beam only plot
    if("electronBackground" in plotSuffixName):
        FirstTH1   += eLaserSignalHistogramDict[fourKeyName[3]] 
    else:
        FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    OnlyLayer4 = [FirstTH1[6], FirstTH1[14], FirstTH1[22], FirstTH1[30]]
    OnlyLayer4 += [FirstTH1[7], FirstTH1[15], FirstTH1[23], FirstTH1[31]]        
    
    DrawHistsOneCanvas(OnlyLayer4, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_Layer4"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], baseHistogramNames[fourKeyName[0]][9])
    
    
    fourKeyName = ["tracking_planes_background_track_x_gamma", "tracking_planes_background_track_x_electrons", "tracking_planes_background_track_x_positrons", "tracking_planes_signal_track_x_positrons"]
    
    
    logy        = False
    if baseHistogramNames[fourKeyName[0]][6]:
        logy = True
        print ("I am in ", fourKeyName[0]) 
    
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    ### overlay e+laser signal on top of electron beam only plot
    if("electronBackground" in plotSuffixName):
        FirstTH1   += eLaserSignalHistogramDict[fourKeyName[3]] 
    else:
        FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    OnlyLayer4 = [FirstTH1[6], FirstTH1[14], FirstTH1[22], FirstTH1[30]]
    OnlyLayer4 += [FirstTH1[7], FirstTH1[15], FirstTH1[23], FirstTH1[31]]          
    
    DrawHistsOneCanvas(OnlyLayer4, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_Layer4"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], baseHistogramNames[fourKeyName[0]][9])
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print ("The total time taken: ", time.time() - start, " s")
