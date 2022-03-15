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
    parser.add_argument('-s', action="store", dest="inSignalFile", type=str, default="ePlusLaserBackgroundTDR_list_root_7671ee4c_trackInfo_Total2p13BX.root") ### default is phase 2 signal
    parser.add_argument('-g', action="store_true", dest="gPlusLaser")
    
    args                = parser.parse_args()
    needPhotonLaser     = args.gPlusLaser
    
    #inDirectory         = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inDirectory         ="/Volumes/Study/Weizmann_PostDoc/Sasha_work/OutputFile/ReprocessedBkgTracksAfterTDR"
    inFileEPlusLaser    = TFile(inDirectory+"/"+args.inSignalFile)

    directory = "LaserBackground_"+args.inSignalFile.split('.')[0]
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    bkgAtDipole = inFileEPlusLaser.Get("tracking_planes_bkg_track_x_track_y_dipole_0")
    bkgAtDipole_Cloned = bkgAtDipole.Clone("bkgAtDipole_Cloned")
    
    bkgAtDipole1 = inFileEPlusLaser.Get("tracking_planes_bkg_track_x_track_y_dipole_1")
    bkgAtDipole1_Cloned = bkgAtDipole1.Clone("bkgAtDipole1_Cloned")
    
    bkgAtDipole_Cloned.Add(bkgAtDipole1_Cloned)
    
    
    if needPhotonLaser:
        bkgAtDipole8 = inFileEPlusLaser.Get("tracking_planes_bkg_track_x_track_y_dipole_8")
        bkgAtDipole8_Cloned = bkgAtDipole8.Clone("bkgAtDipole8_Cloned")
        
        bkgAtDipole9 = inFileEPlusLaser.Get("tracking_planes_bkg_track_x_track_y_dipole_9")
        bkgAtDipole9_Cloned = bkgAtDipole9.Clone("bkgAtDipole9_Cloned")
        
        bkgAtDipole8_Cloned.Add(bkgAtDipole9_Cloned)
    
        bkgAtDipole_Cloned.Add(bkgAtDipole8_Cloned)
        
        FirstTH1     = [bkgAtDipole_Cloned];
        LegendName   = ["Background"]; 
        PlotColor    = [2];
        latexName    = "#gamma+laser"
        latexName3   = ""
        xrange1down  = -250.0
        xrange1up    = 250.0
        canvasName   = "gLaserBkg"
    else:
        FirstTH1     = [bkgAtDipole_Cloned];
        LegendName   = ["Background"]; 
        PlotColor    = [2];
        latexName    = "#font[22]{e+laser}"
        latexName3   = "#font[22]{positron side}"
        xrange1down  = 0.0
        xrange1up    = 250.0
        canvasName   = "eLaserBkg"
    
    
    
    ### plot the positron side
    
    xAxisName    = "x positions of tracks [mm]"
    yAxisName    = "y positions of tracks [mm]"
    
    yrange1down  = -20.0
    yrange1up    = 20.0
    yline1low    = 1.0
    yline1up     = 1.0
    drawline     = False
    logy         = False
    latexName2   = "#font[22]{Background tracks at dipole exit}"
    
    leftLegend   = False
    doAtlas      = False
    doLumi       = False
    noRatio      = False
    do80         = False
    do59         = False
    drawPattern  = ""
    logz         = False
    logx         = False
    
    
    DrawHists(FirstTH1, LegendName, PlotColor, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/TracksAtDipoleExit_Layer1_"+canvasName, yline1low, yline1up, drawline, logy, latexName, latexName2, latexName3,leftLegend, doAtlas, doLumi, noRatio, do80, do59, "COLZ")
    
    
if __name__=="__main__":
    main()
