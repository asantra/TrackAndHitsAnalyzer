import os, sys
from random import random, uniform
from ROOT import *

## event  energy  time x  y z  detector pdg_code  track_id  parent_id layer_id det hitcellx hitcelly trackz trackE vtxx vtxy vtxz p_x p_y p_z weight totalHitEDep true_type(0=purebkg/1=puresig/2=bkgfromsig)

def main():
    inDir = "/Volumes/Study/Weizmann_PostDoc/AllPix2Study/InputFiles/HitBranchesTxtFiles"
    outRoot = TFile("GEANT4Energy.root", "RECREATE")
    outRoot.cd()
    h_DiffEnergy = TH1D("h_DiffEnergy", "h_DiffEnergy; E_{cal} - E_{tru} [GeV]; Entries", 2000, -2, 2)
    h_Px = TH1D("h_Px", "h_Px; p_{x} [GeV]; Entries", 2000, -2, 2)
    counter = 0
    with open(inDir+"/"+sys.argv[1]) as filename:
        for lines in filename.readlines():
            counter += 1
            lines = lines.rstrip()
            if "#" in lines:
                continue
            if counter%1000 == 0: print("Processed: ", counter)
            eachWord = lines.split()
            
            px = float(eachWord[19])
            py = float(eachWord[20])
            pz = float(eachWord[21])
            me2 = (0.5109989461/1000)*(0.5109989461/1000)
            
            E_cal = sqrt(px*px+py*py+pz*pz+me2)
            E_tru = float(eachWord[15])
                
            h_DiffEnergy.Fill(E_cal - E_tru)
            h_Px.Fill(px)

    outRoot.Write()
    
    
if __name__=="__main__":
    main()




    
