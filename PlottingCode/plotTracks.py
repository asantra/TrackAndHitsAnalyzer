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
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="ePlusLaserBackground_list_root_7671ee4c_First3BX_trackInfo.root")
    args = parser.parse_args()
    
    
    inputDir            = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inputTracksRootFile = args.inFile
    plotSuffixName      = ""
    
    ####  and ("All" not in inputTracksRootFile)
    if (("_" in inputTracksRootFile)):
        eachName            = inputTracksRootFile.split('.')[0].split('_')
        inTracksFile        = TFile(inputDir+"/"+inputTracksRootFile)
        suffixName          = "_".join(eachName[:])
        #outDir              = "DistributionPlotsBackground_LongZAxisRange_"+suffixName  ### LongZAxisRange_
        outDir              = "DistributionPlotsBackground_"+suffixName  ### LongZAxisRange_
        plotSuffixName      = suffixName
    else:
        inTracksFile        = TFile(inputDir+"/"+inputTracksRootFile)
        outDir              = "DistributionPlotsBackground_"+inputTracksRootFile.split('.')[0]
        plotSuffixName      = inputTracksRootFile.split('.')[0]
    
    print("suffixName: ", suffixName)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    baseHistogramNames  = {}
    
    
    ##### select the x axis range for different particles.
    #### for long X axis, use -1000 to 10000 for all the particles.
    xAxisRangeLow_electrons            = 2500
    xAxisRangeHigh_electrons           = 6500
    xAxisRangeLow_positrons            = 3500
    xAxisRangeHigh_positrons           = 5500
    xAxisRangeLow_gamma                = 1000
    xAxisRangeHigh_gamma               = 7000
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
    
    baseHistogramNames["tracking_planes_background_track_e_electrons_log"]        = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-6, 1e4, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_positrons_log"]        = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-6, 1e3, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_gamma_log"]            = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-6, 1e5, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_protons_log"]          = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-6, 1e4, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_neutrons_log"]         = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-6, 1e4, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_muons_log"]            = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-6, 1e4, True, "hist", False, True]
    baseHistogramNames["tracking_planes_background_track_e_pions_log"]            = ["E [GeV]", "Particles/BX", 0.0, 20.0, 1e-6, 1e4, True, "hist", False, True]
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_electrons_log"]  = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_electrons_log"]  = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_electrons_log"]  = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_electrons, xAxisRangeHigh_electrons, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_electrons"]          = ["vtx_z [mm]", "vtx_x [mm]", xAxisRangeLow_electrons, xAxisRangeHigh_electrons, -650.0, 650.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_electrons"]          = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_electrons, xAxisRangeHigh_electrons, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_electrons"]          = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_gamma_log"]      = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_gamma_log"]      = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_gamma_log"]      = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_gamma, xAxisRangeHigh_gamma, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_gamma"]              = ["vtx_z [mm]", "vtx_x [mm]", xAxisRangeLow_gamma, xAxisRangeHigh_gamma, -650.0, 650.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_gamma"]              = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_gamma, xAxisRangeHigh_gamma, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_gamma"]              = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_positrons_log"]  = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_positrons_log"]  = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_positrons_log"]  = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_positrons, xAxisRangeHigh_positrons, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_positrons"]          = ["vtx_z [mm]", "vtx_x [mm]", xAxisRangeLow_positrons, xAxisRangeHigh_positrons, -650.0, 650.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_positrons"]          = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_positrons, xAxisRangeHigh_positrons, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_positrons"]          = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_protons_log"]    = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_protons_log"]    = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_protons_log"]    = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_protons, xAxisRangeHigh_protons, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_protons"]            = ["vtx_z [mm]", "vtx_x [mm]", xAxisRangeLow_protons, xAxisRangeHigh_protons, -650.0, 650.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_protons"]            = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_protons, xAxisRangeHigh_protons, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_protons"]            = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_neutrons_log"]   = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_neutrons_log"]   = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_neutrons_log"]   = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_neutrons, xAxisRangeHigh_neutrons, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_neutrons"]           = ["vtx_z [mm]", "vtx_x [mm]", xAxisRangeLow_neutrons, xAxisRangeHigh_neutrons, -650.0, 650.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_neutrons"]           = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_neutrons, xAxisRangeHigh_neutrons, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_neutrons"]           = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]

    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_muons_log"]      = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_muons_log"]      = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_muons_log"]      = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_muons, xAxisRangeHigh_muons, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_muons"]              = ["vtx_z [mm]", "vtx_x [mm]", xAxisRangeLow_muons, xAxisRangeHigh_muons, -650.0, 650.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_muons"]              = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_muons, xAxisRangeHigh_muons, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_muons"]              = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_pions_log"]      = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_pions_log"]      = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_pions_log"]      = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_pions, xAxisRangeHigh_pions, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_pions"]              = ["vtx_z [mm]", "vtx_x [mm]", xAxisRangeLow_pions, xAxisRangeHigh_pions, -650.0, 650.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_pions"]              = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_pions, xAxisRangeHigh_pions, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_pions"]              = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_pi0_log"]        = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_pi0_log"]        = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_pi0_log"]        = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_pions, xAxisRangeHigh_pions, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_pi0"]                = ["vtx_z [mm]", "vtx_x [mm]", xAxisRangeLow_pions, xAxisRangeHigh_pions, -650.0, 650.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_pi0"]                = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_pions, xAxisRangeHigh_pions, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_pi0"]                = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_charged-particles_log"]  = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_charged-particles_log"]  = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_charged-particles_log"]  = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_chargedparticles, xAxisRangeHigh_chargedparticles, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_charged-particles"]          = ["vertex z position [mm]", "vertex x position [mm]", xAxisRangeLow_chargedparticles, xAxisRangeHigh_chargedparticles, -650.0, 650.0, False, "COL", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_charged-particles"]          = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_chargedparticles, xAxisRangeHigh_chargedparticles, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_charged-particles"]          = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    
    baseHistogramNames["tracking_planes_background_vtx_x_track_e_neutral-particles_log"]  = ["vtx_x [mm]", "E [GeV]", -650.0, 650.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_y_track_e_neutral-particles_log"]  = ["vtx_y [mm]", "E [GeV]", -50.0, 50.0, 1e-6, 20, True, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtx_z_track_e_neutral-particles_log"]  = ["vtx_z [mm]", "E [GeV]", xAxisRangeLow_neutralparticles, xAxisRangeHigh_neutralparticles, 1e-6, 20, True, "COLZ", False, False]
    
    baseHistogramNames["tracking_planes_background_vtxz_vtxx_neutral-particles"]          = ["vertex z position [mm]", "vertex x position [mm]", xAxisRangeLow_neutralparticles, xAxisRangeHigh_neutralparticles, -650.0, 650.0, False, "COL", False, False]
    baseHistogramNames["tracking_planes_background_vtxz_vtxy_neutral-particles"]          = ["vtx_z [mm]", "vtx_y [mm]", xAxisRangeLow_neutralparticles, xAxisRangeHigh_neutralparticles, -50.0, 50.0, False, "COLZ", False, False]
    baseHistogramNames["tracking_planes_background_vtxx_vtxy_neutral-particles"]          = ["vtx_x [mm]", "vtx_y [mm]", -650.0, 650.0, -50.0, 50.0, False, "COLZ", False, False]
    
    
    
    #### non signal plots, have 16 components for each histogram
    histogramDict = {}
    signalHistogramDict = {}
    backgroundHistogramDict = {}
    for name in baseHistogramNames:
        eachBaseHistogramPlot = []
        for i in range(0,16):
            h = inTracksFile.Get(name+"_"+str(i))
            checkType = str(type(h))
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
    
    
    #drawline    = False
    #latexName   = ''
    #latexName2  = ''
    #latexName3  = ''
    #leftLegend  = True
    #doAtlas     = False
    #doLumi      = False
    #noRatio     = False
    #do80        = False
    #do59        = False
    
    #for keys in histogramDict:
        #checkType = str(type(histogramDict[keys][0]))
        #print checkType
        #if (("TH1D" in checkType) or ("TH2D" in checkType)):
            #FirstTH1 = histogramDict[keys]
            #LegendName = []
            #PlotColor  = [2]*8
            #for stave in range(0,len(FirstTH1)):
                #LegendName.append("Stave "+str(stave))
            #eachKey = keys.split('_')
            #if len(eachKey)>7:
                #latexName = eachKey[7]
            #elif len(eachKey)>4:
                #latexName = eachKey[4]
            #else:
                #latexName = "all particle"
            #logy        = False
            #if baseHistogramNames[keys][6]:
                #logy = True
                #print "I am in ", keys 
                
            #DrawHists8Canvas(FirstTH1, LegendName, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8])
            
            
            
    ### signal or background histogram, only one component for each one
    
    #### plotting the signal and background
    drawline    = False
    latexName   = ''
    latexName2  = ''
    latexName3  = ''
    leftLegend  = True
    doAtlas     = False
    doLumi      = False
    noRatio     = False
    do80        = False
    do59        = False
    
    #for keys in signalHistogramDict:
        #if(len(signalHistogramDict[keys])==0):continue
        #checkType = str(type(signalHistogramDict[keys][0]))
        #print checkType
        #if (("TH1D" in checkType) or ("TH2D" in checkType)):
            #FirstTH1 = signalHistogramDict[keys]
            
            #LegendName = []
            #PlotColor  = [2]*8
            #for stave in range(0,len(FirstTH1)):
                #LegendName.append("Stave "+str(stave))
            #eachKey = keys.split('_')
            #if len(eachKey)>7:
                #latexName = eachKey[7]
            #elif len(eachKey)>5:
                #latexName = eachKey[5]
            #else:
                #latexName = "all particle"
            #latexName2 = "Signal"
            #logy        = False
            #if baseHistogramNames[keys][6]:
                #logy = True
                #print "I am in ", keys
            
            #DrawHists8Canvas(FirstTH1, LegendName, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8])
            
            
            
    for keys in backgroundHistogramDict:
        if(len(backgroundHistogramDict[keys])==0):continue
        checkType = str(type(backgroundHistogramDict[keys][0]))
        print(checkType)
        if (("TH1D" in checkType) or ("TH2D" in checkType)):
            FirstTH1 = backgroundHistogramDict[keys]
            
            LegendName = []
            LegendNameCombined = []
            PlotColor  = [4]*8
            for stave in range(0,len(FirstTH1)):
                LegendName.append("Stave "+str(stave))
                LegendNameCombined.append("First layer")
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
                print ("I am in ", keys)
            
            #DrawHists8Canvas(FirstTH1, LegendName, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8])
            
            
            OnlyStave0 = [FirstTH1[0]]
            
            DrawHists(OnlyStave0, LegendName, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_Stave0"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8], baseHistogramNames[keys][9])
            
            Layer1Hist = FirstTH1[0]
            Layer1Hist.Add(FirstTH1[1])
            Stave0And1 = [Layer1Hist]
            
            DrawHists(Stave0And1, LegendNameCombined, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_Stave0And1"+"_"+plotSuffixName, 1, 1, drawline, logy, '', '', '', False, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8], baseHistogramNames[keys][9])
        
        
            OnlyStave7 = [FirstTH1[7]]
            
            LegendName7= [LegendName[7]]
            DrawHists(OnlyStave7, LegendName7, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_Stave7"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8], baseHistogramNames[keys][9])
            
            
            OnlyStave8 = [FirstTH1[8]]
            
            LegendName8= [LegendName[8]]
            DrawHists(OnlyStave8, LegendName8, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_Stave8"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8], baseHistogramNames[keys][9])
            
            
            OnlyStave15 = [FirstTH1[15]]
            
            LegendName15= [LegendName[15]]
            DrawHists(OnlyStave15, LegendName15, PlotColor, baseHistogramNames[keys][0], baseHistogramNames[keys][1], baseHistogramNames[keys][2], baseHistogramNames[keys][3], baseHistogramNames[keys][4], baseHistogramNames[keys][5], outDir+"/"+keys+"_Stave15"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[keys][7], baseHistogramNames[keys][8], baseHistogramNames[keys][9])
    
            
    '''
    ###### drawing with the new function
    
    threeKeyName = ["tracking_planes_vtx_z_gamma", "tracking_planes_vtx_z_electrons", "tracking_planes_vtx_z_positrons"]
    
    FirstTH1    = histogramDict[threeKeyName[0]]
    FirstTH1   += histogramDict[threeKeyName[1]]
    FirstTH1   += histogramDict[threeKeyName[2]]
    
    LegendName1 = []
    PlotColor1  = [2]*8 + [4]*8 + [kGreen+3]*8 + [kGray]*8
    
    
    latexName   = "signal+background"
    latexName2  = ""
    latexName3  = ""
    
    for stave in range(0,8):
        LegendName1.append("#gamma, Stave "+str(stave))
    for stave in range(0,8):
        LegendName1.append("e^{-}, Stave "+str(stave))
    for stave in range(0,8):
        LegendName1.append("e^{+}, Stave "+str(stave))
    
    logy        = False
    if baseHistogramNames[threeKeyName[0]][6]:
        logy = True
        print "I am in ", threeKeyName[0] 
        
    leftLegend = True
        
    DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[threeKeyName[0]][0], baseHistogramNames[threeKeyName[0]][1], baseHistogramNames[threeKeyName[0]][2], baseHistogramNames[threeKeyName[0]][3], baseHistogramNames[threeKeyName[0]][4], baseHistogramNames[threeKeyName[0]][5], outDir+"/"+threeKeyName[0]+"_3Files", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[threeKeyName[0]][7], baseHistogramNames[threeKeyName[0]][8])
    '''
    
    
        
    #leftLegend  = True
    #latexName   = ""
    #latexName2  = ""
    #PlotColor1  = [2]*8 + [4]*8 + [kGreen+3]*8 + [kGray]*8
    #LegendName1 = []
    #for stave in range(0,8):
        #LegendName1.append("#gamma, Bkg, Stave "+str(stave))
    #for stave in range(0,8):
        #LegendName1.append("e^{-}, Bkg, Stave "+str(stave))
    #for stave in range(0,8):
        #LegendName1.append("e^{+}, Bkg, Stave "+str(stave))
    #for stave in range(0,8):
        #LegendName1.append("e^{+}, Sig, Stave "+str(stave))
        
        
    #fourKeyName = ["tracking_planes_background_track_x_gamma", "tracking_planes_background_track_x_electrons", "tracking_planes_background_track_x_positrons", "tracking_planes_signal_track_x_positrons"]
    
    #logy        = False
    #if baseHistogramNames[fourKeyName[0]][6]:
        #logy = True
        #print "I am in ", fourKeyName[0] 
    
    #FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    #FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    #FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    #FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    
    #DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_4Files"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], True)
    
    
    
    
    #fourKeyName = ["tracking_planes_background_track_x_gamma_sumE", "tracking_planes_background_track_x_electrons_sumE", "tracking_planes_background_track_x_positrons_sumE", "tracking_planes_signal_track_x_positrons_sumE"]
    
    #logy        = False
    #if baseHistogramNames[fourKeyName[0]][6]:
        #logy = True
        #print "I am in ", fourKeyName[0] 
    
    #FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    #FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    #FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    #FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    
    #DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_4Files"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], True)
    
    '''
    fourKeyName = ["tracking_planes_background_vtx_z_gamma", "tracking_planes_background_vtx_z_electrons", "tracking_planes_background_vtx_z_positrons", "tracking_planes_signal_vtx_z_positrons"]
    latexName   = ""
    
    
    
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    
    DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_4Files", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], True)
    
    
    
    fourKeyName = ["tracking_planes_background_track_y_gamma", "tracking_planes_background_track_y_electrons", "tracking_planes_background_track_y_positrons", "tracking_planes_signal_track_y_positrons"]
    latexName   = ""
    
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    
    DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_4Files", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], True)
    
    
    
        
    fourKeyName = ["tracking_planes_background_track_e_gamma", "tracking_planes_background_track_e_electrons", "tracking_planes_background_track_e_positrons", "tracking_planes_signal_track_e_positrons"]
    latexName   = ""
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    leftLegend = False
        
    
    DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[3]][2], baseHistogramNames[fourKeyName[3]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_4Files", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], True)
    
    
    
    
    fourKeyName = ["tracking_planes_background_track_e_gamma_zoomed", "tracking_planes_background_track_e_electrons_zoomed", "tracking_planes_background_track_e_positrons_zoomed", "tracking_planes_signal_track_e_positrons_zoomed"]
    latexName   = ""
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    leftLegend = False
        
    
    DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[3]][2], baseHistogramNames[fourKeyName[3]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_4Files", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], True)
    
    
    
    
    
    
    
    fourKeyName = ["tracking_planes_background_track_e_gamma_morezoomed", "tracking_planes_background_track_e_electrons_morezoomed", "tracking_planes_background_track_e_positrons_morezoomed", "tracking_planes_signal_track_e_positrons_morezoomed"]
    latexName   = ""
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    leftLegend = False
        
    
    DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[3]][2], baseHistogramNames[fourKeyName[3]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_4Files", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], True)
    
    
    
    
    ##### draw 4 canvases
    
    ### non signal plots, have 16 components for each histogram
    histogramDict = {}
    
    for name in baseHistogramNames:
        eachBaseHistogramPlot = []
        for i in range(0,16):
            h = inTracksFile.Get(name+"_"+str(i))
            eachBaseHistogramPlot.append(h)
            histogramDict[name] = eachBaseHistogramPlot
            
    LegendName1 = []
    for i in range(0,16):
        LegendName1.append("Stave "+str(i))
        
    sixteenKeyName = ["tracking_planes_background_track_x_gamma"]
    
    latexName    = "#gamma (bkg)"
    FirstTH1     = histogramDict[sixteenKeyName[0]]
    PlotColor1   = [2, 4]*4+[kGreen+3, kMagenta]*4
    
    logy = False
    if baseHistogramNames[sixteenKeyName[0]][6]:
        logy = True
    
    DrawHists4Canvas(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[sixteenKeyName[0]][0], baseHistogramNames[sixteenKeyName[0]][1], baseHistogramNames[sixteenKeyName[0]][2], baseHistogramNames[sixteenKeyName[0]][3], baseHistogramNames[sixteenKeyName[0]][4], baseHistogramNames[sixteenKeyName[0]][5], outDir+"/"+sixteenKeyName[0]+"_4Canvas", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59)
    
    
    sixteenKeyName = ["tracking_planes_background_track_x_electrons"]
    
    latexName    = "e^{-} (bkg)"
    FirstTH1     = histogramDict[sixteenKeyName[0]]
    PlotColor1   = [2, 4]*4+[kGreen+3, kMagenta]*4
    
    DrawHists4Canvas(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[sixteenKeyName[0]][0], baseHistogramNames[sixteenKeyName[0]][1], baseHistogramNames[sixteenKeyName[0]][2], baseHistogramNames[sixteenKeyName[0]][3], baseHistogramNames[sixteenKeyName[0]][4], baseHistogramNames[sixteenKeyName[0]][5], outDir+"/"+sixteenKeyName[0]+"_4Canvas", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59)
    
    
    
    
    
    
    sixteenKeyName = ["tracking_planes_background_track_x_positrons"]
    
    latexName    = "e^{+} (bkg)"
    FirstTH1     = histogramDict[sixteenKeyName[0]]
    PlotColor1   = [2, 4]*4+[kGreen+3, kMagenta]*4
    
    DrawHists4Canvas(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[sixteenKeyName[0]][0], baseHistogramNames[sixteenKeyName[0]][1], baseHistogramNames[sixteenKeyName[0]][2], baseHistogramNames[sixteenKeyName[0]][3], baseHistogramNames[sixteenKeyName[0]][4], baseHistogramNames[sixteenKeyName[0]][5], outDir+"/"+sixteenKeyName[0]+"_4Canvas", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59)
    
    
    sixteenKeyName = ["tracking_planes_background_track_x_gamma_sumE"]
    
    latexName    = "#gamma (bkg)"
    FirstTH1     = histogramDict[sixteenKeyName[0]]
    PlotColor1   = [2, 4]*4+[kGreen+3, kMagenta]*4
    
    DrawHists4Canvas(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[sixteenKeyName[0]][0], baseHistogramNames[sixteenKeyName[0]][1], baseHistogramNames[sixteenKeyName[0]][2], baseHistogramNames[sixteenKeyName[0]][3], baseHistogramNames[sixteenKeyName[0]][4], baseHistogramNames[sixteenKeyName[0]][5], outDir+"/"+sixteenKeyName[0]+"_4Canvas", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59)
    
    
    
    
    
    
    
    sixteenKeyName = ["tracking_planes_background_track_x_electrons_sumE"]
    
    latexName    = "e^{-} (bkg)"
    FirstTH1     = histogramDict[sixteenKeyName[0]]
    PlotColor1   = [2, 4]*4+[kGreen+3, kMagenta]*4
    
    DrawHists4Canvas(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[sixteenKeyName[0]][0], baseHistogramNames[sixteenKeyName[0]][1], baseHistogramNames[sixteenKeyName[0]][2], baseHistogramNames[sixteenKeyName[0]][3], baseHistogramNames[sixteenKeyName[0]][4], baseHistogramNames[sixteenKeyName[0]][5], outDir+"/"+sixteenKeyName[0]+"_4Canvas", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59)
    
    
    sixteenKeyName = ["tracking_planes_background_track_x_positrons_sumE"]
    
    latexName    = "e^{+} (bkg)"
    FirstTH1     = histogramDict[sixteenKeyName[0]]
    PlotColor1   = [2, 4]*4+[kGreen+3, kMagenta]*4
    
    DrawHists4Canvas(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[sixteenKeyName[0]][0], baseHistogramNames[sixteenKeyName[0]][1], baseHistogramNames[sixteenKeyName[0]][2], baseHistogramNames[sixteenKeyName[0]][3], baseHistogramNames[sixteenKeyName[0]][4], baseHistogramNames[sixteenKeyName[0]][5], outDir+"/"+sixteenKeyName[0]+"_4Canvas", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59)
    
    
    
    #threeKeyName = ["tracking_planes_background_track_e_gamma_zoomed", "tracking_planes_background_track_e_electrons_zoomed", "tracking_planes_background_track_e_positrons_zoomed"]
    #latexName   = "background"
    #FirstTH1    = backgroundHistogramDict[threeKeyName[0]]
    #FirstTH1   += backgroundHistogramDict[threeKeyName[1]]
    #FirstTH1   += backgroundHistogramDict[threeKeyName[2]]
    
    #leftLegend = False
        
    
    #DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[threeKeyName[0]][0], baseHistogramNames[threeKeyName[0]][1], baseHistogramNames[threeKeyName[0]][2], baseHistogramNames[threeKeyName[0]][3], baseHistogramNames[threeKeyName[0]][4], baseHistogramNames[threeKeyName[0]][5], outDir+"/"+threeKeyName[0]+"_3Files", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[threeKeyName[0]][7], baseHistogramNames[threeKeyName[0]][8])
    
    
    
    #threeKeyName = ["tracking_planes_background_track_e_gamma_morezoomed", "tracking_planes_background_track_e_electrons_morezoomed", "tracking_planes_background_track_e_positrons_morezoomed"]
    #latexName   = "background"
    #FirstTH1    = backgroundHistogramDict[threeKeyName[0]]
    #FirstTH1   += backgroundHistogramDict[threeKeyName[1]]
    #FirstTH1   += backgroundHistogramDict[threeKeyName[2]]
    
    #leftLegend = False
        
    
    #DrawHists8CanvasManyFiles(FirstTH1, LegendName1, PlotColor1, baseHistogramNames[threeKeyName[0]][0], baseHistogramNames[threeKeyName[0]][1], baseHistogramNames[threeKeyName[0]][2], baseHistogramNames[threeKeyName[0]][3], baseHistogramNames[threeKeyName[0]][4], baseHistogramNames[threeKeyName[0]][5], outDir+"/"+threeKeyName[0]+"_3Files", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[threeKeyName[0]][7], baseHistogramNames[threeKeyName[0]][8])
    
    '''
    
    
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print ("The total time taken: ", time.time() - start, " s")
