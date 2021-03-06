#### this code mixes the background tracks and signal tracks per bunch crossing
#### run: python3 plotBackgroundFilesFromText.py -l  <event file in text mode>  -b <bx number>
import os
import sys
import time
import pprint
import math, array
from ROOT import *
from collections import OrderedDict
import argparse
    
def projectedLine(vtxx, vtxy, vtxz, R=50):
    #Window:   
    z1=3925
    x1=39
    y1=0
    #Dump:      
    z2=7000
    x2=102
    y2=0
    slope = (x2-x1)/(z2-z1)
    intercept = (x1*z2-x2*z1)/(z2-z1)
    x = slope*vtxz+intercept
    return sqrt((vtxx - x)**2 + vtxy**2) < R
    
    
    
def energyBins(nbins):
  #//// variable binned in X axis histograms
  logmin           = -7;
  logmax           = 1;
  logbinwidth      = (logmax-logmin)/float(nbins);
  xpoints          = []
  
  for i in range(0, nbins+1):
      #print((logmin + i*logbinwidth), pow( 10,(logmin + i*logbinwidth) ))
      xpoints.append(pow( 10,(logmin + i*logbinwidth) ))
                     
  xpoints.append(2*pow( 10,1))
  return xpoints

def main():
    
    parser = argparse.ArgumentParser(description='Code to get 2D plots')
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="ePlusLaserBackgroundTDR_list_root_7671ee4c_trackInfo_Total2p13BX.txt")
    parser.add_argument('-b', action="store", dest="bx", type=float, default=2.13)
    args = parser.parse_args()
    
    inDir = '/Users/arkasantra/arka/Sasha_Work/OutputFile'
    #inDir = "/Volumes/Study/Weizmann_PostDoc/Sasha_work/OutputFile/ReprocessedBkgTracksAfterTDR"
    
    bkgFileName   = open(inDir+'/'+args.inFile)
    withoutText   = args.inFile.split('.txt')[0]
    rootFile      = withoutText+".root"
    nbx           = args.bx
    
    #Window:   
    z1=3925
    x1=39
    y1=0
    #Dump:      
    z2=7000
    x2=102
    y2=0
    
    #if 'ePlusLaserBkgNewSamples' in args.inFile:
        #nbx = 298.0
    #elif 'gPlusLaserBkgNewSamples' in args.inFile:
        #nbx = 80.0
    #elif 'fast_9f6b6590_al_window' in args.inFile:
        #nbx = 23.4
    #elif 'fast_9f6b6590_34_35' in args.inFile:
        #nbx = 16.56
    #elif 'ePlusLaserKaptonWindow_hics_background_fast_9f6b6590_0_16' in args.inFile:
        #nbx = 120.0
    #elif 'hics_background_fast_9f6b6590_17_33' in args.inFile:
        #nbx = 141.38
    #elif 'ePlusLaserKaptonWindow' in args.inFile:
        #nbx = 278.0
    
    print('BX selected: ',nbx)
    
    outFile       = TFile(inDir+'/'+rootFile, "RECREATE")
    outFile.cd()
    nbins  = 475
    xbins  = energyBins(nbins)
    xarray = array.array('d',xbins)
    
    #print(xarray, " ", len(xarray))
    
    allHistoDict  = {}
    
    allHistoDict.update({"tracking_planes_bkg_track_x_track_y_dipole_0":TH2D("tracking_planes_bkg_track_x_track_y_dipole_0","tracking_planes_bkg_track_x_track_y_dipole_0",250, -250.0, 250.0, 40, -20,20)})
    allHistoDict.update({"tracking_planes_bkg_track_x_track_y_dipole_1":TH2D("tracking_planes_bkg_track_x_track_y_dipole_1","tracking_planes_bkg_track_x_track_y_dipole_1",250, -250.0, 250.0, 40, -20,20)})
    
    allHistoDict.update({"tracking_planes_bkg_track_x_track_y_dipole_8":TH2D("tracking_planes_bkg_track_x_track_y_dipole_8","tracking_planes_bkg_track_x_track_y_dipole_8",250, -250.0, 250.0, 40, -20,20)})
    allHistoDict.update({"tracking_planes_bkg_track_x_track_y_dipole_9":TH2D("tracking_planes_bkg_track_x_track_y_dipole_9","tracking_planes_bkg_track_x_track_y_dipole_9",250, -250.0, 250.0, 40, -20,20)})
    
    
    
    for i in range(0, 16):
        #### gamma
        allHistoDict.update({"tracking_planes_background_track_x_gamma_"+str(i):TH1D("tracking_planes_background_track_x_gamma_"+str(i),"tracking_planes_background_track_x_gamma_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_gamma_"+str(i):TH1D("tracking_planes_background_track_time_gamma_"+str(i),"tracking_planes_background_track_time_gamma_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_gamma_sumE_"+str(i):TH1D("tracking_planes_background_track_x_gamma_sumE_"+str(i),"tracking_planes_background_track_x_gamma_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_gamma_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_gamma_1GeVCut_"+str(i),"tracking_planes_background_track_x_gamma_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_gamma_log_"+str(i):TH1D("tracking_planes_background_track_e_gamma_log_"+str(i),"tracking_planes_background_track_e_gamma_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_gamma_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_gamma_log_"+str(i),"tracking_planes_background_vtx_z_track_e_gamma_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_gamma_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_gamma_log_"+str(i),"tracking_planes_background_vtx_x_track_e_gamma_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_gamma_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_gamma_"+str(i), "tracking_planes_background_vtxz_vtxx_gamma_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        allHistoDict.update({"tracking_planes_backgrounddump_track_e_gamma_log_"+str(i):TH1D("tracking_planes_backgrounddump_track_e_gamma_log_"+str(i),"tracking_planes_backgrounddump_track_e_gamma_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundwindow_track_e_gamma_log_"+str(i):TH1D("tracking_planes_backgroundwindow_track_e_gamma_log_"+str(i),"tracking_planes_backgroundwindow_track_e_gamma_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundair_track_e_gamma_log_"+str(i):TH1D("tracking_planes_backgroundair_track_e_gamma_log_"+str(i),"tracking_planes_backgroundair_track_e_gamma_log_"+str(i),nbins+1, xarray)})
        
        
                             
        #### positrons
        allHistoDict.update({"tracking_planes_background_track_x_positrons_"+str(i):TH1D("tracking_planes_background_track_x_positrons_"+str(i),"tracking_planes_background_track_x_positrons_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_positrons_"+str(i):TH1D("tracking_planes_background_track_time_positrons_"+str(i),"tracking_planes_background_track_time_positrons_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_positrons_sumE_"+str(i):TH1D("tracking_planes_background_track_x_positrons_sumE_"+str(i),"tracking_planes_background_track_x_positrons_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_positrons_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_positrons_1GeVCut_"+str(i),"tracking_planes_background_track_x_positrons_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_positrons_log_"+str(i):TH1D("tracking_planes_background_track_e_positrons_log_"+str(i),"tracking_planes_background_track_e_positrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_positrons_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_positrons_log_"+str(i),"tracking_planes_background_vtx_z_track_e_positrons_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_positrons_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_positrons_log_"+str(i),"tracking_planes_background_vtx_x_track_e_positrons_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_positrons_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_positrons_"+str(i), "tracking_planes_background_vtxz_vtxx_positrons_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        allHistoDict.update({"tracking_planes_backgrounddump_track_e_positrons_log_"+str(i):TH1D("tracking_planes_backgrounddump_track_e_positrons_log_"+str(i),"tracking_planes_backgrounddump_track_e_positrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundwindow_track_e_positrons_log_"+str(i):TH1D("tracking_planes_backgroundwindow_track_e_positrons_log_"+str(i),"tracking_planes_backgroundwindow_track_e_positrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundair_track_e_positrons_log_"+str(i):TH1D("tracking_planes_backgroundair_track_e_positrons_log_"+str(i),"tracking_planes_backgroundair_track_e_positrons_log_"+str(i),nbins+1, xarray)})
        
        
        #### electrons
        allHistoDict.update({"tracking_planes_background_track_x_electrons_"+str(i):TH1D("tracking_planes_background_track_x_electrons_"+str(i),"tracking_planes_background_track_x_electrons_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_electrons_"+str(i):TH1D("tracking_planes_background_track_time_electrons_"+str(i),"tracking_planes_background_track_time_electrons_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_electrons_sumE_"+str(i):TH1D("tracking_planes_background_track_x_electrons_sumE_"+str(i),"tracking_planes_background_track_x_electrons_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_electrons_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_electrons_1GeVCut_"+str(i),"tracking_planes_background_track_x_electrons_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_electrons_log_"+str(i):TH1D("tracking_planes_background_track_e_electrons_log_"+str(i),"tracking_planes_background_track_e_electrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_electrons_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_electrons_log_"+str(i),"tracking_planes_background_vtx_z_track_e_electrons_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_electrons_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_electrons_log_"+str(i),"tracking_planes_background_vtx_x_track_e_electrons_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_electrons_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_electrons_"+str(i), "tracking_planes_background_vtxz_vtxx_electrons_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        allHistoDict.update({"tracking_planes_backgrounddump_track_e_electrons_log_"+str(i):TH1D("tracking_planes_backgrounddump_track_e_electrons_log_"+str(i),"tracking_planes_backgrounddump_track_e_electrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundwindow_track_e_electrons_log_"+str(i):TH1D("tracking_planes_backgroundwindow_track_e_electrons_log_"+str(i),"tracking_planes_backgroundwindow_track_e_electrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundair_track_e_electrons_log_"+str(i):TH1D("tracking_planes_backgroundair_track_e_electrons_log_"+str(i),"tracking_planes_backgroundair_track_e_electrons_log_"+str(i),nbins+1, xarray)})
        
        
        
        #### protons
        allHistoDict.update({"tracking_planes_background_track_x_protons_"+str(i):TH1D("tracking_planes_background_track_x_protons_"+str(i),"tracking_planes_background_track_x_protons_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_protons_"+str(i):TH1D("tracking_planes_background_track_time_protons_"+str(i),"tracking_planes_background_track_time_protons_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_protons_sumE_"+str(i):TH1D("tracking_planes_background_track_x_protons_sumE_"+str(i),"tracking_planes_background_track_x_protons_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_protons_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_protons_1GeVCut_"+str(i),"tracking_planes_background_track_x_protons_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_protons_log_"+str(i):TH1D("tracking_planes_background_track_e_protons_log_"+str(i),"tracking_planes_background_track_e_protons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_protons_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_protons_log_"+str(i),"tracking_planes_background_vtx_z_track_e_protons_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_protons_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_protons_log_"+str(i),"tracking_planes_background_vtx_x_track_e_protons_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_protons_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_protons_"+str(i), "tracking_planes_background_vtxz_vtxx_protons_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        allHistoDict.update({"tracking_planes_backgrounddump_track_e_protons_log_"+str(i):TH1D("tracking_planes_backgrounddump_track_e_protons_log_"+str(i),"tracking_planes_backgrounddump_track_e_protons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundwindow_track_e_protons_log_"+str(i):TH1D("tracking_planes_backgroundwindow_track_e_protons_log_"+str(i),"tracking_planes_backgroundwindow_track_e_protons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundair_track_e_protons_log_"+str(i):TH1D("tracking_planes_backgroundair_track_e_protons_log_"+str(i),"tracking_planes_backgroundair_track_e_protons_log_"+str(i),nbins+1, xarray)})
        
        
        
        #### neutrons
        allHistoDict.update({"tracking_planes_background_track_x_neutrons_"+str(i):TH1D("tracking_planes_background_track_x_neutrons_"+str(i),"tracking_planes_background_track_x_neutrons_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_neutrons_"+str(i):TH1D("tracking_planes_background_track_time_neutrons_"+str(i),"tracking_planes_background_track_time_neutrons_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_neutrons_sumE_"+str(i):TH1D("tracking_planes_background_track_x_neutrons_sumE_"+str(i),"tracking_planes_background_track_x_neutrons_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_neutrons_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_neutrons_1GeVCut_"+str(i),"tracking_planes_background_track_x_neutrons_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_neutrons_log_"+str(i):TH1D("tracking_planes_background_track_e_neutrons_log_"+str(i),"tracking_planes_background_track_e_neutrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_neutrons_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_neutrons_log_"+str(i),"tracking_planes_background_vtx_z_track_e_neutrons_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_neutrons_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_neutrons_log_"+str(i),"tracking_planes_background_vtx_x_track_e_neutrons_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_neutrons_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_neutrons_"+str(i), "tracking_planes_background_vtxz_vtxx_neutrons_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        allHistoDict.update({"tracking_planes_backgrounddump_track_e_neutrons_log_"+str(i):TH1D("tracking_planes_backgrounddump_track_e_neutrons_log_"+str(i),"tracking_planes_backgrounddump_track_e_neutrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundwindow_track_e_neutrons_log_"+str(i):TH1D("tracking_planes_backgroundwindow_track_e_neutrons_log_"+str(i),"tracking_planes_backgroundwindow_track_e_neutrons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundair_track_e_neutrons_log_"+str(i):TH1D("tracking_planes_backgroundair_track_e_neutrons_log_"+str(i),"tracking_planes_backgroundair_track_e_neutrons_log_"+str(i),nbins+1, xarray)})
        
        
        
        
        #### muons
        allHistoDict.update({"tracking_planes_background_track_x_muons_"+str(i):TH1D("tracking_planes_background_track_x_muons_"+str(i),"tracking_planes_background_track_x_muons_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_muons_"+str(i):TH1D("tracking_planes_background_track_time_muons_"+str(i),"tracking_planes_background_track_time_muons_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_muons_sumE_"+str(i):TH1D("tracking_planes_background_track_x_muons_sumE_"+str(i),"tracking_planes_background_track_x_muons_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_muons_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_muons_1GeVCut_"+str(i),"tracking_planes_background_track_x_muons_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_muons_log_"+str(i):TH1D("tracking_planes_background_track_e_muons_log_"+str(i),"tracking_planes_background_track_e_muons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_muons_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_muons_log_"+str(i),"tracking_planes_background_vtx_z_track_e_muons_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_muons_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_muons_log_"+str(i),"tracking_planes_background_vtx_x_track_e_muons_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_muons_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_muons_"+str(i), "tracking_planes_background_vtxz_vtxx_muons_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        allHistoDict.update({"tracking_planes_backgrounddump_track_e_muons_log_"+str(i):TH1D("tracking_planes_backgrounddump_track_e_muons_log_"+str(i),"tracking_planes_backgrounddump_track_e_muons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundwindow_track_e_muons_log_"+str(i):TH1D("tracking_planes_backgroundwindow_track_e_muons_log_"+str(i),"tracking_planes_backgroundwindow_track_e_muons_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundair_track_e_muons_log_"+str(i):TH1D("tracking_planes_backgroundair_track_e_muons_log_"+str(i),"tracking_planes_backgroundair_track_e_muons_log_"+str(i),nbins+1, xarray)})
        
        
        
        
        #### pions
        allHistoDict.update({"tracking_planes_background_track_x_pions_"+str(i):TH1D("tracking_planes_background_track_x_pions_"+str(i),"tracking_planes_background_track_x_pions_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_pions_"+str(i):TH1D("tracking_planes_background_track_time_pions_"+str(i),"tracking_planes_background_track_time_pions_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_pions_sumE_"+str(i):TH1D("tracking_planes_background_track_x_pions_sumE_"+str(i),"tracking_planes_background_track_x_pions_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_pions_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_pions_1GeVCut_"+str(i),"tracking_planes_background_track_x_pions_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_pions_log_"+str(i):TH1D("tracking_planes_background_track_e_pions_log_"+str(i),"tracking_planes_background_track_e_pions_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_pions_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_pions_log_"+str(i),"tracking_planes_background_vtx_z_track_e_pions_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_pions_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_pions_log_"+str(i),"tracking_planes_background_vtx_x_track_e_pions_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_pions_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_pions_"+str(i), "tracking_planes_background_vtxz_vtxx_pions_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        allHistoDict.update({"tracking_planes_backgrounddump_track_e_pions_log_"+str(i):TH1D("tracking_planes_backgrounddump_track_e_pions_log_"+str(i),"tracking_planes_backgrounddump_track_e_pions_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundwindow_track_e_pions_log_"+str(i):TH1D("tracking_planes_backgroundwindow_track_e_pions_log_"+str(i),"tracking_planes_backgroundwindow_track_e_pions_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundair_track_e_pions_log_"+str(i):TH1D("tracking_planes_backgroundair_track_e_pions_log_"+str(i),"tracking_planes_backgroundair_track_e_pions_log_"+str(i),nbins+1, xarray)})
        
        
        
        #### pions 0
        allHistoDict.update({"tracking_planes_background_track_x_pi0_"+str(i):TH1D("tracking_planes_background_track_x_pi0_"+str(i),"tracking_planes_background_track_x_pi0_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_pi0_"+str(i):TH1D("tracking_planes_background_track_time_pi0_"+str(i),"tracking_planes_background_track_time_pi0_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_pi0_sumE_"+str(i):TH1D("tracking_planes_background_track_x_pi0_sumE_"+str(i),"tracking_planes_background_track_x_pi0_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_pi0_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_pi0_1GeVCut_"+str(i),"tracking_planes_background_track_x_pi0_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_pi0_log_"+str(i):TH1D("tracking_planes_background_track_e_pi0_log_"+str(i),"tracking_planes_background_track_e_pi0_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_pi0_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_pi0_log_"+str(i),"tracking_planes_background_vtx_z_track_e_pi0_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_pi0_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_pi0_log_"+str(i),"tracking_planes_background_vtx_x_track_e_pi0_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_pi0_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_pi0_"+str(i), "tracking_planes_background_vtxz_vtxx_pi0_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        allHistoDict.update({"tracking_planes_backgrounddump_track_e_pi0_log_"+str(i):TH1D("tracking_planes_backgrounddump_track_e_pi0_log_"+str(i),"tracking_planes_backgrounddump_track_e_pi0_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundwindow_track_e_pi0_log_"+str(i):TH1D("tracking_planes_backgroundwindow_track_e_pi0_log_"+str(i),"tracking_planes_backgroundwindow_track_e_pi0_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_backgroundair_track_e_pi0_log_"+str(i):TH1D("tracking_planes_backgroundair_track_e_pi0_log_"+str(i),"tracking_planes_backgroundair_track_e_pi0_log_"+str(i),nbins+1, xarray)})
        
        
        #### charged-particles
        allHistoDict.update({"tracking_planes_background_track_x_charged-particles_"+str(i):TH1D("tracking_planes_background_track_x_charged-particles_"+str(i),"tracking_planes_background_track_x_charged-particles_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_charged-particles_"+str(i):TH1D("tracking_planes_background_track_time_charged-particles_"+str(i),"tracking_planes_background_track_time_charged-particles_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_charged-particles_sumE_"+str(i):TH1D("tracking_planes_background_track_x_charged-particles_sumE_"+str(i),"tracking_planes_background_track_x_charged-particles_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_charged-particles_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_charged-particles_1GeVCut_"+str(i),"tracking_planes_background_track_x_charged-particles_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_charged-particles_log_"+str(i):TH1D("tracking_planes_background_track_e_charged-particles_log_"+str(i),"tracking_planes_background_track_e_charged-particles_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_charged-particles_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_charged-particles_log_"+str(i),"tracking_planes_background_vtx_z_track_e_charged-particles_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_charged-particles_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_charged-particles_log_"+str(i),"tracking_planes_background_vtx_x_track_e_charged-particles_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_charged-particles_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_charged-particles_"+str(i), "tracking_planes_background_vtxz_vtxx_charged-particles_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
        
        
        
        #### neutral-particles
        allHistoDict.update({"tracking_planes_background_track_x_neutral-particles_"+str(i):TH1D("tracking_planes_background_track_x_neutral-particles_"+str(i),"tracking_planes_background_track_x_neutral-particles_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_time_neutral-particles_"+str(i):TH1D("tracking_planes_background_track_time_neutral-particles_"+str(i),"tracking_planes_background_track_time_neutral-particles_"+str(i),500,0.0,5000.0)})
        allHistoDict.update({"tracking_planes_background_track_x_neutral-particles_sumE_"+str(i):TH1D("tracking_planes_background_track_x_neutral-particles_sumE_"+str(i),"tracking_planes_background_track_x_neutral-particles_sumE_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_x_neutral-particles_1GeVCut_"+str(i):TH1D("tracking_planes_background_track_x_neutral-particles_1GeVCut_"+str(i),"tracking_planes_background_track_x_neutral-particles_1GeVCut_"+str(i),1300, -650.0, 650.0)})
        allHistoDict.update({"tracking_planes_background_track_e_neutral-particles_log_"+str(i):TH1D("tracking_planes_background_track_e_neutral-particles_log_"+str(i),"tracking_planes_background_track_e_neutral-particles_log_"+str(i),nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_z_track_e_neutral-particles_log_"+str(i):TH2D("tracking_planes_background_vtx_z_track_e_neutral-particles_log_"+str(i),"tracking_planes_background_vtx_z_track_e_neutral-particles_log_"+str(i),4000, -5000, 15000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtx_x_track_e_neutral-particles_log_"+str(i):TH2D("tracking_planes_background_vtx_x_track_e_neutral-particles_log_"+str(i),"tracking_planes_background_vtx_x_track_e_neutral-particles_log_"+str(i),6000, -3000, 3000, nbins+1, xarray)})
        allHistoDict.update({"tracking_planes_background_vtxz_vtxx_neutral-particles_"+str(i):TH2D("tracking_planes_background_vtxz_vtxx_neutral-particles_"+str(i), "tracking_planes_background_vtxz_vtxx_neutral-particles_"+str(i), 4000, -5000, 15000, 6000, -3000, 3000)})
    
    
    
    lineCounter   = 0
    ### write the bkg as it is
    for lines in bkgFileName.readlines():
        if '#' in lines:
            continue
        lineCounter += 1
        if(lineCounter%100000==0): print("processed: ", lineCounter)
        ### this is to reject bkg particles from calorimeter 
        
        #if(lineCounter > 200000):break
        lines        = lines.rstrip()
        eachWord     = lines.split()
        bxNumber     = int(eachWord[0])
        trackId      = int(eachWord[2])
        pdgId        = int(eachWord[1])
        staveId      = int(eachWord[3])-1000
        xPos         = float(eachWord[4])
        yPos         = float(eachWord[5])
        energyVal    = float(eachWord[6])
        weight       = float(eachWord[7])
        vtx_x        = float(eachWord[8])
        vtx_y        = float(eachWord[9])
        vtx_z        = float(eachWord[10])
        parent_id    = int(eachWord[11])
        pxx          = float(eachWord[12])
        pyy          = float(eachWord[13])
        pzz          = float(eachWord[14])
        physproc     = float(eachWord[15])
        time         = float(eachWord[16])
        
        if (int(eachWord[3])==2000):continue
        
        zproj = 2748.0
        
        
        if(staveId==0):
            zz = 3962.0125
            xproj = pxx/pzz*(zproj-zz) + xPos
            yproj = pyy/pzz*(zproj-zz) + yPos
            allHistoDict["tracking_planes_bkg_track_x_track_y_dipole_0"].Fill(xproj, yproj, weight)
        if(staveId==1):
            zz = 3950.0125
            xproj = pxx/pzz*(zproj-zz) + xPos
            yproj = pyy/pzz*(zproj-zz) + yPos
            allHistoDict["tracking_planes_bkg_track_x_track_y_dipole_1"].Fill(xproj, yproj, weight)
            
        if(staveId==8):
            zz = 3962.0125
            xproj = pxx/pzz*(zproj-zz) + xPos
            yproj = pyy/pzz*(zproj-zz) + yPos
            allHistoDict["tracking_planes_bkg_track_x_track_y_dipole_8"].Fill(xproj, yproj, weight)
        if(staveId==9):
            zz = 3950.0125
            xproj = pxx/pzz*(zproj-zz) + xPos
            yproj = pyy/pzz*(zproj-zz) + yPos
            allHistoDict["tracking_planes_bkg_track_x_track_y_dipole_9"].Fill(xproj, yproj, weight)
        
        
        
        ###electrons
        if(pdgId == 11 and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_electrons_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_electrons_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_electrons_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_electrons_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            
            allHistoDict["tracking_planes_background_track_e_electrons_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_electrons_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_electrons_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_electrons_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            if((vtx_z > 6800 and vtx_z < 8300) and (vtx_x > -1700 and vtx_x < 500)): 
                allHistoDict["tracking_planes_backgrounddump_track_e_electrons_log_"+str(staveId)].Fill(energyVal, weight)
            if((vtx_z > 3850 and vtx_z < 3900) and (vtx_x > -600 and vtx_x < 600)):
                allHistoDict["tracking_planes_backgroundwindow_track_e_electrons_log_"+str(staveId)].Fill(energyVal, weight)
            if(vtx_z > z1 and vtx_z < z2):
                if(projectedLine(vtx_x, vtx_y, vtx_z)):
                    allHistoDict["tracking_planes_backgroundair_track_e_electrons_log_"+str(staveId)].Fill(energyVal, weight)
        
        ###protons and anti-protons
        if((pdgId == 2212 or pdgId == -2212) and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_protons_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_protons_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_protons_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_protons_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            
            allHistoDict["tracking_planes_background_track_e_protons_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_protons_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_protons_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_protons_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            if((vtx_z > 6800 and vtx_z < 8300) and (vtx_x > -1700 and vtx_x < 500)): 
                allHistoDict["tracking_planes_backgrounddump_track_e_protons_log_"+str(staveId)].Fill(energyVal, weight)
            if((vtx_z > 3850 and vtx_z < 3900) and (vtx_x > -600 and vtx_x < 600)):
                allHistoDict["tracking_planes_backgroundwindow_track_e_protons_log_"+str(staveId)].Fill(energyVal, weight)
            if(vtx_z > z1 and vtx_z < z2):
                if(projectedLine(vtx_x, vtx_y, vtx_z)):
                    allHistoDict["tracking_planes_backgroundair_track_e_protons_log_"+str(staveId)].Fill(energyVal, weight)
            
        ### neutrons
        if(pdgId == 2112 and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_neutrons_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_neutrons_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_neutrons_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_neutrons_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            
            allHistoDict["tracking_planes_background_track_e_neutrons_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_neutrons_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_neutrons_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_neutrons_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            if((vtx_z > 6800 and vtx_z < 8300) and (vtx_x > -1700 and vtx_x < 500)): 
                allHistoDict["tracking_planes_backgrounddump_track_e_neutrons_log_"+str(staveId)].Fill(energyVal, weight)
            if((vtx_z > 3850 and vtx_z < 3900) and (vtx_x > -600 and vtx_x < 600)):
                allHistoDict["tracking_planes_backgroundwindow_track_e_neutrons_log_"+str(staveId)].Fill(energyVal, weight)
            if(vtx_z > z1 and vtx_z < z2):
                if(projectedLine(vtx_x, vtx_y, vtx_z)):
                    allHistoDict["tracking_planes_backgroundair_track_e_neutrons_log_"+str(staveId)].Fill(energyVal, weight)
            
        ### muons and anti-muons
        if((pdgId == 13 or pdgId == -13) and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_muons_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_muons_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_muons_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_muons_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            
            allHistoDict["tracking_planes_background_track_e_muons_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_muons_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_muons_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_muons_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            if((vtx_z > 6800 and vtx_z < 8300) and (vtx_x > -1700 and vtx_x < 500)): 
                allHistoDict["tracking_planes_backgrounddump_track_e_muons_log_"+str(staveId)].Fill(energyVal, weight)
            if((vtx_z > 3850 and vtx_z < 3900) and (vtx_x > -600 and vtx_x < 600)):
                allHistoDict["tracking_planes_backgroundwindow_track_e_muons_log_"+str(staveId)].Fill(energyVal, weight)
            if(vtx_z > z1 and vtx_z < z2):
                if(projectedLine(vtx_x, vtx_y, vtx_z)):
                    allHistoDict["tracking_planes_backgroundair_track_e_muons_log_"+str(staveId)].Fill(energyVal, weight)
            
        ### pi+ or pi-
        if((pdgId == 211 or pdgId == -211) and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_pions_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_pions_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_pions_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_pions_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            
            allHistoDict["tracking_planes_background_track_e_pions_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_pions_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_pions_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_pions_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            if((vtx_z > 6800 and vtx_z < 8300) and (vtx_x > -1700 and vtx_x < 500)): 
                allHistoDict["tracking_planes_backgrounddump_track_e_pions_log_"+str(staveId)].Fill(energyVal, weight)
            if((vtx_z > 3850 and vtx_z < 3900) and (vtx_x > -600 and vtx_x < 600)):
                allHistoDict["tracking_planes_backgroundwindow_track_e_pions_log_"+str(staveId)].Fill(energyVal, weight)
            if(vtx_z > z1 and vtx_z < z2):
                if(projectedLine(vtx_x, vtx_y, vtx_z)):
                    allHistoDict["tracking_planes_backgroundair_track_e_pions_log_"+str(staveId)].Fill(energyVal, weight)
            
        ### pi0
        if((pdgId == 111 or pdgId == -111) and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_pi0_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_pi0_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_pi0_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_pi0_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            
            allHistoDict["tracking_planes_background_track_e_pi0_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_pi0_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_pi0_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_pi0_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            if((vtx_z > 6800 and vtx_z < 8300) and (vtx_x > -1700 and vtx_x < 500)): 
                allHistoDict["tracking_planes_backgrounddump_track_e_pi0_log_"+str(staveId)].Fill(energyVal, weight)
            if((vtx_z > 3850 and vtx_z < 3900) and (vtx_x > -600 and vtx_x < 600)):
                allHistoDict["tracking_planes_backgroundwindow_track_e_pi0_log_"+str(staveId)].Fill(energyVal, weight)
            if(vtx_z > z1 and vtx_z < z2):
                if(projectedLine(vtx_x, vtx_y, vtx_z)):
                    allHistoDict["tracking_planes_backgroundair_track_e_pi0_log_"+str(staveId)].Fill(energyVal, weight)
            
        ### positrons
        if(pdgId == -11 and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_positrons_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_positrons_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_positrons_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_positrons_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            allHistoDict["tracking_planes_background_track_e_positrons_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_positrons_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_positrons_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_positrons_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            if((vtx_z > 6800 and vtx_z < 8300) and (vtx_x > -1700 and vtx_x < 500)): 
                allHistoDict["tracking_planes_backgrounddump_track_e_positrons_log_"+str(staveId)].Fill(energyVal, weight)
            if((vtx_z > 3850 and vtx_z < 3900) and (vtx_x > -600 and vtx_x < 600)):
                allHistoDict["tracking_planes_backgroundwindow_track_e_positrons_log_"+str(staveId)].Fill(energyVal, weight)
            if(vtx_z > z1 and vtx_z < z2):
                if(projectedLine(vtx_x, vtx_y, vtx_z)):
                    allHistoDict["tracking_planes_backgroundair_track_e_positrons_log_"+str(staveId)].Fill(energyVal, weight)
            
            
        ### photon
        if(pdgId == 22 and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_gamma_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_gamma_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_gamma_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_gamma_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            allHistoDict["tracking_planes_background_track_e_gamma_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_gamma_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_gamma_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_gamma_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            
            if((vtx_z > 6800 and vtx_z < 8300) and (vtx_x > -1700 and vtx_x < 500)): 
                allHistoDict["tracking_planes_backgrounddump_track_e_gamma_log_"+str(staveId)].Fill(energyVal, weight)
            if((vtx_z > 3850 and vtx_z < 3900) and (vtx_x > -600 and vtx_x < 600)):
                allHistoDict["tracking_planes_backgroundwindow_track_e_gamma_log_"+str(staveId)].Fill(energyVal, weight)
            if(vtx_z > z1 and vtx_z < z2):
                if(projectedLine(vtx_x, vtx_y, vtx_z)):
                    allHistoDict["tracking_planes_backgroundair_track_e_gamma_log_"+str(staveId)].Fill(energyVal, weight)

            
            
        ##### charged particles
        chargedParticles = {-11, 11, 13, -13, 211, -211, 2212, -2212}
        neutralParticles = {22, 2112, 111, -111}
        if((pdgId in chargedParticles) and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_charged-particles_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_charged-particles_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_charged-particles_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_charged-particles_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            allHistoDict["tracking_planes_background_track_e_charged-particles_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_charged-particles_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_charged-particles_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_charged-particles_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
            
         
        ##### neutral particles
        if((pdgId in neutralParticles) and trackId!=1):
            allHistoDict["tracking_planes_background_track_x_neutral-particles_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_time_neutral-particles_"+str(staveId)].Fill(time, weight)
            if(energyVal>1.0):
                allHistoDict["tracking_planes_background_track_x_neutral-particles_1GeVCut_"+str(staveId)].Fill(xPos, weight)
            allHistoDict["tracking_planes_background_track_x_neutral-particles_sumE_"+str(staveId)].Fill(xPos, energyVal*weight)
            allHistoDict["tracking_planes_background_track_e_neutral-particles_log_"+str(staveId)].Fill(energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_z_track_e_neutral-particles_log_"+str(staveId)].Fill(vtx_z, energyVal, weight)
            allHistoDict["tracking_planes_background_vtx_x_track_e_neutral-particles_log_"+str(staveId)].Fill(vtx_x, energyVal, weight)
            allHistoDict["tracking_planes_background_vtxz_vtxx_neutral-particles_"+str(staveId)].Fill(vtx_z, vtx_x, weight)
        
        
    for keys in allHistoDict:
        allHistoDict[keys].Scale(1./nbx)
        allHistoDict[keys].Write()
    outFile.Close()
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
