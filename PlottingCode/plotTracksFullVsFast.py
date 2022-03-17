### setup to make plots for the tracker ###

import os, sys, glob, time
from ROOT import *
import argparse
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint





def main():
    gROOT.SetBatch()
    
    parser = argparse.ArgumentParser(description='Code to get 2D plots')
    parser.add_argument('-fullsim', action="store", dest="inFileFullSim", type=str, default="ePlusLaserBackgroundTDR_list_root_7671ee4c_trackInfo_Total2p13BX.root")
    parser.add_argument('-fullsimLegend', action="store", dest="fullsimLegend", type=str, default="FullSim")
    parser.add_argument('-fastsim', action="store", dest="inFileFastSim", type=str, default="ePlusLaserBackgroundTDR_list_root_7671ee4c_fast_trackInfo_Total7p45BX.root")
    parser.add_argument('-fastsimLegend', action="store", dest="fastsimLegend", type=str, default="FastSim")
    args = parser.parse_args()
    
    
    inputDir                   = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inputTracksRootFile        = args.inFileFullSim
    inputTracksRootFileFastSim = args.inFileFastSim
    LegendNameEntries          = [args.fullsimLegend, args.fastsimLegend]
    
    
    plotSuffixName      = ""
    
    ####  and ("All" not in inputTracksRootFile)
    if (("_" in inputTracksRootFile)):
        eachName            = inputTracksRootFile.split('.')[0].split('_')
        inTracksFile        = TFile(inputDir+"/"+inputTracksRootFile)
        inTracksFileFastSim = TFile(inputDir+"/"+inputTracksRootFileFastSim)
        suffixName          = "_".join(eachName[:])
        outDir              = "DistributionPlotsBackground_"+LegendNameEntries[0]+"And"+LegendNameEntries[1]+"_"+suffixName  ### LongZAxisRange_
        plotSuffixName      = LegendNameEntries[0]+"And"+LegendNameEntries[1]+"_"+suffixName
    else:
        inTracksFile        = TFile(inputDir+"/"+inputTracksRootFile)
        inTracksFileFastSim = TFile(inputDir+"/"+inputTracksRootFileFastSim)
        outDir              = "DistributionPlotsBackground_"+inputTracksRootFile.split('.')[0]
        plotSuffixName      = inputTracksRootFile.split('.')[0]
    
    print("suffixName: ", suffixName)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    baseHistogramNames         = {}    
    
    ##### select the x axis range for different particles.
    #### for long X axis, use -1000 to 10000 for all the particles.
    xAxisRangeLow_electrons            = -5000
    xAxisRangeHigh_electrons           = 10000
    xAxisRangeLow_positrons            = 3500
    xAxisRangeHigh_positrons           = 5500
    xAxisRangeLow_gamma                = 1000
    xAxisRangeHigh_gamma               = 9000
    xAxisRangeLow_protons              = 3500
    xAxisRangeHigh_protons             = 7000
    xAxisRangeLow_neutrons             = 1000
    xAxisRangeHigh_neutrons            = 9000
    xAxisRangeLow_muons                = 3500
    xAxisRangeHigh_muons               = 6500
    xAxisRangeLow_pions                = 3500
    xAxisRangeHigh_pions               = 6500
    xAxisRangeLow_chargedparticles     = 2000
    xAxisRangeHigh_chargedparticles    = 6500
    xAxisRangeLow_neutralparticles     = 1000
    xAxisRangeHigh_neutralparticles    = 9000
    
    baseHistogramNames["tracking_planes_background_track_e_electrons_log"]        = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_positrons_log"]        = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_gamma_log"]            = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_protons_log"]          = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-3, 1e2, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_neutrons_log"]         = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_muons_log"]            = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-3, 1e2, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_pions_log"]            = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-3, 1e2, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_time_electrons"]         = ["time [ns]", "Particles/BX", 0.0, 500.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_time_positrons"]         = ["time [ns]", "Particles/BX", 0.0, 500.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_time_gamma"]             = ["time [ns]", "Particles/BX", 0.0, 500.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_time_protons"]           = ["time [ns]", "Particles/BX", 0.0, 500.0, 1e-3, 1e2, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_time_neutrons"]          = ["time [ns]", "Particles/BX", 0.0, 500.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_time_muons"]             = ["time [ns]", "Particles/BX", 0.0, 500.0, 1e-3, 1e2, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_time_pions"]             = ["time [ns]", "Particles/BX", 0.0, 500.0, 1e-3, 1e2, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgrounddump_track_e_gamma_log"]        = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundwindow_track_e_gamma_log"]      = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundair_track_e_gamma_log"]         = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgrounddump_track_e_positrons_log"]    = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundwindow_track_e_positrons_log"]  = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundair_track_e_positrons_log"]     = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgrounddump_track_e_electrons_log"]    = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundwindow_track_e_electrons_log"]  = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundair_track_e_electrons_log"]     = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgrounddump_track_e_neutrons_log"]     = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundwindow_track_e_neutrons_log"]   = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundair_track_e_neutrons_log"]      = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-1, 1e7, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgrounddump_track_e_protons_log"]      = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundwindow_track_e_protons_log"]    = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundair_track_e_protons_log"]       = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgrounddump_track_e_muons_log"]        = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundwindow_track_e_muons_log"]      = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundair_track_e_muons_log"]         = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgrounddump_track_e_pions_log"]        = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundwindow_track_e_pions_log"]      = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundair_track_e_pions_log"]         = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgrounddump_track_e_pi0_log"]          = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundwindow_track_e_pi0_log"]        = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_backgroundair_track_e_pi0_log"]           = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-2, 1e5, True, "hist", False, True]
    
    
    
    #### non signal plots, have 16 components for each histogram, FullSim
    histogramDict = {}
    signalHistogramDict = {}
    backgroundHistogramDict = {}
    for name in baseHistogramNames:
        eachBaseHistogramPlot = []
        for i in range(0,16):
            h = inTracksFile.Get(name+"_"+str(i))
            checkType = str(type(h))
            if ("TH1" in checkType): h = h.Rebin(7)
            if (("TH1" in checkType) or ("TH2" in checkType)):
                ### scale by the bx
                #h.Scale(1./23.4)
                eachBaseHistogramPlot.append(h)
            
        if ("signal" in name):
            signalHistogramDict[name] = eachBaseHistogramPlot
        elif("background" in name):
            backgroundHistogramDict[name] = eachBaseHistogramPlot
        else:
            histogramDict[name] = eachBaseHistogramPlot
            
            
            
    #### non signal plots, have 16 components for each histogram, FastSim
    histogramDictFastSim = {}
    signalHistogramDictFastSim = {}
    backgroundHistogramDictFastSim = {}
    for name in baseHistogramNames:
        eachBaseHistogramPlot = []
        for i in range(0,16):
            h = inTracksFileFastSim.Get(name+"_"+str(i))
            checkType = str(type(h))
            if ("TH1" in checkType): h = h.Rebin(7)
            if (("TH1" in checkType) or ("TH2" in checkType)):
                ### scale by the bx
                #h.Scale(1./23.4)
                eachBaseHistogramPlot.append(h)
            
        if ("signal" in name):
            signalHistogramDictFastSim[name] = eachBaseHistogramPlot
        elif("background" in name):
            backgroundHistogramDictFastSim[name] = eachBaseHistogramPlot
        else:
            histogramDictFastSim[name] = eachBaseHistogramPlot
    
    
    
            
    
    #### plotting the signal and background
    drawline    = False
    latexName   = ''
    latexName2  = ''
    latexName3  = ''
    leftLegend  = False
    doAtlas     = False
    doLumi      = False
    noRatio     = False
    do80        = False
    do59        = False
    
    
            
            
    for keys in backgroundHistogramDict:
        for keysFastSim in backgroundHistogramDictFastSim:
            ### check if both key names are same
            if keys!=keysFastSim:
                continue
            ### check if a key is not empty
            if(len(backgroundHistogramDict[keys])==0 or len(backgroundHistogramDictFastSim[keys])==0):continue
            checkType        = str(type(backgroundHistogramDict[keys][0]))
            checkTypeFastSim = str(type(backgroundHistogramDictFastSim[keys][0]))
            if (("TH1D" in checkType and "TH1D" in checkTypeFastSim) or ("TH2D" in checkType and "TH2D" in checkTypeFastSim)):
                ### draw the ratio
                #if True:
                if (('dump' in keys) or ('window' in keys) or ('air' in keys)):
                    
                    print("+++++++++++++++ keys in ratio ", keys, " and for FastSim: ", keysFastSim)
                    if("pi0" in keys): continue
                    FirstTH1        = backgroundHistogramDict[keys]
                    FirstTH1FastSim = backgroundHistogramDictFastSim[keysFastSim]
                    if 'dump' in keys:
                        baseKey = keys.replace("backgrounddump", "background")
                    elif 'window' in keys:
                        baseKey = keys.replace("backgroundwindow", "background")
                    elif 'air' in keys:
                        baseKey = keys.replace("backgroundair", "background")
                    else:
                        continue
                    BaseTH1        = backgroundHistogramDict[baseKey]
                    BaseTH1FastSim = backgroundHistogramDictFastSim[baseKey]
                                    
                    LegendName         = []
                    PlotColor          = [4,4,2,2]*4
                    for stave in range(0,len(FirstTH1)):
                        LegendName.append(LegendNameEntries[0]+", Stave "+str(stave))
                        LegendName.append(LegendNameEntries[1]+", Stave "+str(stave))

                    eachKey = keys.split('_')
                    if len(eachKey)>7:
                        latexName = eachKey[7]
                    elif len(eachKey)>5:
                        latexName = eachKey[5]
                    else:
                        latexName = "all particle"
                    latexName2 = "background"
                    logy        = False
                    if baseHistogramNames[keys][6]:
                        logy = True
                    
                    
                    yAxisUp   = 3e1
                    yAxisDown = 5e-4
                    
                    ### for different staves
                    for i in [0,7,8,15]:
                        OnlyStave0  = [FirstTH1[i], BaseTH1[i], FirstTH1FastSim[i], BaseTH1FastSim[i]]
                        LegendName0 = [LegendName[i*2],LegendName[i*2],LegendName[i*2+1],LegendName[i*2+1]]
                        
                        DrawRatioHists(OnlyStave0, LegendName0, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], yAxisDown, yAxisUp, outDir+"/"+keys+"_Stave"+str(i)+"Ratio_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8], baseHistogramNames[keys][9])
                    
                
                #### draw the distribution
                else:
                    
                
                    print("---------------------- keys ", keys)
                    
                    FirstTH1        = backgroundHistogramDict[keys]
                    FirstTH1FastSim = backgroundHistogramDictFastSim[keysFastSim]
                    
                    LegendName         = []
                    LegendNameCombined = []
                    PlotColor  = [4,2]*8
                    for stave in range(0,len(FirstTH1)):
                        LegendName.append(LegendNameEntries[0]+", Stave "+str(stave))
                        LegendName.append(LegendNameEntries[1]+", Stave "+str(stave))
                        LegendNameCombined.append(LegendNameEntries[0]+", First layer")
                        LegendNameCombined.append(LegendNameEntries[1]+", First layer")
                        
                    eachKey = keys.split('_')
                    if len(eachKey)>7:
                        latexName = eachKey[7]
                    elif len(eachKey)>5:
                        latexName = eachKey[5]
                    else:
                        latexName = "all particle"
                        
                    latexName2 = "background"
                    logy        = False
                    if baseHistogramNames[keys][6]:
                        logy = True                    
                    
                    for i in [0,7,8,15]:
                        OnlyStave0  = [FirstTH1[i], FirstTH1FastSim[i]]
                        LegendName0 = [LegendName[i*2],LegendName[i*2+1]]
                        
                        DrawHists(OnlyStave0, LegendName0, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_Stave"+str(i)+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8], baseHistogramNames[keys][9])
                        
                        if i == 0:
                            Layer1Hist          = FirstTH1[i]
                            Layer1Hist.Add(FirstTH1[i+1])
                            Layer1HistFastSim   = FirstTH1FastSim[i]
                            Layer1HistFastSim.Add(FirstTH1FastSim[i+1])
                            Stave0And1          = [Layer1Hist, Layer1HistFastSim]
                            LegendNameCombined0 = [LegendNameCombined[i*2],LegendNameCombined[i*2+1]]
                            
                            DrawHists(Stave0And1, LegendNameCombined0, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_Stave"+str(i)+"And"+str(i+1)+"_"+plotSuffixName, 1, 1, drawline, logy, '', '', '', False, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8], baseHistogramNames[keys][9])
                    
                
                    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print ("The total time taken: ", time.time() - start, " s")
