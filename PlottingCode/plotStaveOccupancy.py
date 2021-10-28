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
    inDirectory = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inFile100 = TFile(inDirectory+"/SignalFileListBX100_hits.root")
    
    inFile1   = TFile(inDirectory+"/SignalFileListBX1_hits.root")
    
    directory = "OccupancyPlots"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    xyPlot_BX100 = OrderedDict()
    for hist in inFile100.GetListOfKeys():
        hName = hist.GetName()
        hNameStr = str(hName)
        if (("tracking_planes_hits_xy" not in hNameStr) or ("edep" in hNameStr)): continue
        xyPlot_BX100[hName] = inFile100.Get(hName)
    
    #pprint.pprint(xyPlot_BX100)
    FirstTH1   = []
    LegendName = []
    PlotColor  = []
    chip = 0
    for keys in xyPlot_BX100:
        chip_Layer0 = int(keys.split('_')[4])
        if(chip_Layer0%16 == 0):
            #print(keys)
            FirstTH1.append(xyPlot_BX100[keys])
            chip += 1
            LegendName.append("chip "+str(chip))
            PlotColor.append(2)
            
    #pprint.pprint(FirstTH1)
    
    xAxisName    = "cell_X"
    yAxisName    = "cell_Y"
    xrange1down  = 0.0
    xrange1up    = 1024.0
    yrange1down  = 0.0
    yrange1up    = 512.0
    yline1low    = 1.0
    yline1up     = 1.0
    drawline     = False
    logy         = False
    latexName    = ""
    latexName2   = "Tracker Layer 1, Inner Stave"
    latexName3   = "Signal tracks ~100"
    leftLegend   = False
    doAtlas      = False
    doLumi       = False
    noRatio      = False
    do80         = False
    do59         = False
    drawPattern  = "COLZ"
    logz         = False
    
    DrawHists9Canvas(FirstTH1, LegendName, PlotColor, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/XYOccupancy_TrackerLayer1Stave0_SignalTrackMultiplicity100", yline1low, yline1up, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz)
    
    
    xyPlot_BX1 = OrderedDict()
    
    for hist in inFile1.GetListOfKeys():
        hName = hist.GetName()
        hNameStr = str(hName)
        if (("tracking_planes_hits_xy" not in hNameStr) or ("edep" in hNameStr)): continue
        xyPlot_BX1[hName] = inFile1.Get(hName)
        
        
    #pprint.pprint(xyPlot_BX100)
    FirstTH1   = []
    LegendName = []
    PlotColor  = []
    chip = 0
    for keys in xyPlot_BX1:
        chip_Layer0 = int(keys.split('_')[4])
        if(chip_Layer0%16 == 0):
            #print(keys)
            FirstTH1.append(xyPlot_BX1[keys])
            chip += 1
            LegendName.append("chip "+str(chip))
            PlotColor.append(2)
            
            
    latexName3   = "Signal tracks ~2"
    DrawHists9Canvas(FirstTH1, LegendName, PlotColor, xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, directory+"/XYOccupancy_TrackerLayer1Stave0_SignalTrackMultiplicity1", yline1low, yline1up, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz)
    
    
    
if __name__=="__main__":
    main()
