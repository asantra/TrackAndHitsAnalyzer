import os
import sys
import time
import pprint
import math, array
from ROOT import *
from collections import OrderedDict
import argparse
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *


def main():
    inDir = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    parser = argparse.ArgumentParser(description='Code to get 2D plots')
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="signalMC_e0gpc_3.0_trackInfo_EnergyCheck.root")
    args = parser.parse_args()
    
    inFile = TFile(inDir+"/"+args.inFile,"READ")
    directory = "TrueEnergyVsReconstructedEnergyPlots"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse0 = inFile.Get("tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_0")
    tracking_planes_slopeFromHits_signal_delta_track_efitfraction0    = inFile.Get("tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_0")
    tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse1 = inFile.Get("tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_1")
    tracking_planes_slopeFromHits_signal_delta_track_efitfraction1    = inFile.Get("tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_1")
    tracking_planes_signal_delta_track_efitfraction0                  = inFile.Get("tracking_planes_signal_delta_track_efitfraction_positrons_log_0")
    tracking_planes_signal_delta_track_efitfraction1                  = inFile.Get("tracking_planes_signal_delta_track_efitfraction_positrons_log_1")
    tracking_planes_signal_delta_track_efitfraction6                  = inFile.Get("tracking_planes_signal_delta_track_efitfraction_positrons_log_6")
    tracking_planes_signal_delta_track_efitfraction7                  = inFile.Get("tracking_planes_signal_delta_track_efitfraction_positrons_log_7")
    
    
    tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse0_Cloned = tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse0.Clone("tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse0_Cloned")
    tracking_planes_slopeFromHits_signal_delta_track_efitfraction0_Cloned = tracking_planes_slopeFromHits_signal_delta_track_efitfraction0.Clone("tracking_planes_slopeFromHits_signal_delta_track_efitfraction0")
    tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse1_Cloned = tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse1.Clone("tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse1_Cloned")
    tracking_planes_slopeFromHits_signal_delta_track_efitfraction1_Cloned = tracking_planes_slopeFromHits_signal_delta_track_efitfraction1.Clone("tracking_planes_slopeFromHits_signal_delta_track_efitfraction1")
    tracking_planes_signal_delta_track_efitfraction0_Cloned = tracking_planes_signal_delta_track_efitfraction0.Clone("tracking_planes_signal_delta_track_efitfraction0")
    tracking_planes_signal_delta_track_efitfraction1_Cloned = tracking_planes_signal_delta_track_efitfraction1.Clone("tracking_planes_signal_delta_track_efitfraction1")
    tracking_planes_signal_delta_track_efitfraction6_Cloned = tracking_planes_signal_delta_track_efitfraction6.Clone("tracking_planes_signal_delta_track_efitfraction6")
    tracking_planes_signal_delta_track_efitfraction7_Cloned = tracking_planes_signal_delta_track_efitfraction7.Clone("tracking_planes_signal_delta_track_efitfraction7")
    
    ### add the two staves
    tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse0_Cloned.Add(tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse1_Cloned)
    tracking_planes_slopeFromHits_signal_delta_track_efitfraction0_Cloned.Add(tracking_planes_slopeFromHits_signal_delta_track_efitfraction1_Cloned)
    tracking_planes_signal_delta_track_efitfraction0_Cloned.Add(tracking_planes_signal_delta_track_efitfraction1_Cloned)
    tracking_planes_signal_delta_track_efitfraction6_Cloned.Add(tracking_planes_signal_delta_track_efitfraction7_Cloned)
    
    FirstTH1 = [tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse0_Cloned]
    LegendName = ['signal']
    
    logz = False
    LatexName = "signal e^{+}"
    LatexName2 = "x_{Exit} from straight line joining x_{1} and x_{4}"
    LatexName3 = ""
    Draw2DHists(FirstTH1, LegendName, "E_{true} [GeV]", "(E - E_{true})/E_{true}", "Particles/BX", 0, 10.0, -0.9, .9, 0, 20, directory+"/energyDiffFracVsE", logz, LatexName, LatexName2)
    
    
    FirstTH1   = [tracking_planes_slopeFromHits_signal_delta_track_efitfraction0_Cloned]
    LegendName = ["signal"]
    PlotColor  = [4]
    drawline   = False
    logy       = False
    DrawHists(FirstTH1, LegendName, PlotColor,"(E - E_{true})/E_{true}", "Particles/BX", -0.2, 0.2, 0, 225, directory+"/energyDiffHit1Hit4", 1, 1, drawline, logy, LatexName, LatexName2, LatexName3)
    
    
    LatexName2 = "x_{Exit} from x_{1} and true #vec{p}_{1}"
    FirstTH1   = [tracking_planes_signal_delta_track_efitfraction0_Cloned]
    
    DrawHists(FirstTH1, LegendName, PlotColor,"(E - E_{true})/E_{true}", "Particles/BX", -0.2, 0.2, 0, 225, directory+"/energyDiffHit1Momentum", 1, 1, drawline, logy, LatexName, LatexName2, LatexName3)
    
    LatexName2 = "x_{Exit} from x_{4} and true #vec{p}_{4}"
    FirstTH1   = [tracking_planes_signal_delta_track_efitfraction6_Cloned]
    
    DrawHists(FirstTH1, LegendName, PlotColor,"(E - E_{true})/E_{true}", "Particles/BX", -0.2, 0.2, 0, 225, directory+"/energyDiffHit4Momentum", 1, 1, drawline, logy, LatexName, LatexName2, LatexName3)
    
    
if __name__=="__main__":
    main()
