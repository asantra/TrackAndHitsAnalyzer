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
    parser.add_argument('-s', action="store", dest="inSignalFile", type=str, default="list_root_hics_165gev_w0_3000nm_jeti40_122020_9550dac4.root") ### default is phase 2 signal
    parser.add_argument('-g', action="store_true", dest="gPlusLaser")
    
    args                = parser.parse_args()
    needPhotonLaser     = args.gPlusLaser
    
    inDirectory         = "/Volumes/Study/Weizmann_PostDoc/Sasha_work/OutputFile"
    #inDirectory         = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inFileEPlusLaser    = TFile(inDirectory+"/"+args.inSignalFile)
    
    

    directory = "LaserSignal_"+args.inSignalFile.split('.')[0]
    
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    signalAtDipole = inFileEPlusLaser.Get("tracking_planes_signal_track_x_track_y_dipole_positrons_0")
    signalAtDipole_Cloned = signalAtDipole.Clone("signalAtDipole_Cloned")
    
    signalAtDipole1 = inFileEPlusLaser.Get("tracking_planes_signal_track_x_track_y_dipole_positrons_1")
    signalAtDipole1_Cloned = signalAtDipole1.Clone("signalAtDipole1_Cloned")
    
    signalAtDipole_Cloned.Add(signalAtDipole1_Cloned)
    
    
    if needPhotonLaser:
        signalAtDipole8 = inFileEPlusLaser.Get("tracking_planes_signal_track_x_track_y_dipole_electrons_8")
        signalAtDipole8_Cloned = signalAtDipole8.Clone("signalAtDipole8_Cloned")
        
        signalAtDipole9 = inFileEPlusLaser.Get("tracking_planes_signal_track_x_track_y_dipole_electrons_9")
        signalAtDipole9_Cloned = signalAtDipole9.Clone("signalAtDipole9_Cloned")
        
        signalAtDipole8_Cloned.Add(signalAtDipole9_Cloned)
    
    
    
    #### occupancy in hitcellx, positron side
    
        signalAtDipole_Cloned.Add(signalAtDipole8_Cloned)
        FirstTH1     = [signalAtDipole_Cloned];
        LegendName   = ["Signal"]; 
        PlotColor    = [2];
        latexName    = "#gamma+laser"
        latexName3   = ""
        xrange1down  = -250.0
        xrange1up    = 250.0
    else:
        FirstTH1     = [signalAtDipole_Cloned];
        LegendName   = ["Signal"]; 
        PlotColor    = [2];
        latexName    = "e+laser"
        latexName3   = "positron side"
        xrange1down  = 0.0
        xrange1up    = 250.0
    
    
    
    ### plot the positron side
    
    xAxisName    = "x positions of tracks [mm]"
    yAxisName    = "y positions of tracks [mm]"
    
    yrange1down  = -20.0
    yrange1up    = 20.0
    yline1low    = 1.0
    yline1up     = 1.0
    drawline     = False
    logy         = False
    latexName2   = "Signal tracks at dipole exit"
    
    
        
    leftLegend   = False
    doAtlas      = False
    doLumi       = False
    noRatio      = False
    do80         = False
    do59         = False
    drawPattern  = ""
    logz         = False
    logx         = False
    
    
    
    DrawHists(FirstTH1, LegendName, PlotColor, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/TracksAtDipoleExit_Layer1", yline1low, yline1up, drawline, logy, latexName, latexName2, latexName3,leftLegend, doAtlas, doLumi, noRatio, do80, do59, "COLZ")
    
    
    
    
    signalEnergy         = inFileEPlusLaser.Get("tracking_planes_signal_track_e_dipole_positrons_log_0")
    signalEnergy_Cloned  = signalAtDipole.Clone("signalEnergy")
    
    signalEnergy1        = inFileEPlusLaser.Get("tracking_planes_signal_track_e_dipole_positrons_log_1")
    signalEnergy1_Cloned = signalAtDipole1.Clone("signalEnergy1")
    
    signalEnergy_Cloned.Add(signalEnergy1_Cloned)
    
    
    ### plot the positron side
    
    xAxisName    = "energy [GeV]"
    yAxisName    = "events/BX"
    xrange1down  = 1e-5
    xrange1up    = 20.0
    yrange1down  = 1e-5
    yrange1up    = 20.0
    yline1low    = 1.0
    yline1up     = 1.0
    drawline     = False
    logy         = True
    latexName2   = "Signal tracks at dipole exit"
    
    if needPhotonLaser:
        latexName3   = "positron side"
    else:
        latexName3   = "energy for track_x > 15 cm"
        
    leftLegend   = False
    doAtlas      = False
    doLumi       = False
    noRatio      = False
    do80         = False
    do59         = False
    drawPattern  = ""
    logz         = False
    logx         = True
    print(signalEnergy_Cloned.GetEntries())
    FirstTH1 = [signalEnergy_Cloned]
    LegendName = ['signal']
    PlotColor = [4]
    
    
    DrawHists(FirstTH1, LegendName, PlotColor, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/TracksAtDipoleExitEnergy_Layer1", yline1low, yline1up, drawline, logy, 'e+laser', latexName2, latexName3,leftLegend, doAtlas, doLumi, noRatio, do80, do59, "hist",logz, logx)
    
    
if __name__=="__main__":
    main()
