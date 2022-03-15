#### this code mixes the background tracks and signal tracks per bunch crossing
#### run: python3 plotSignalFilesFromText.py -l  <event file in text mode> -b <bx number>
import os
import sys
import time
import pprint
import math, array
from ROOT import *
from collections import OrderedDict
import argparse
mm2m = 1./1000.0


def xofz(r1,r2,z):
   dz = r2[2]-r1[2]
   dx = r2[0]-r1[0]
   if(dz==0):
        print("ERROR in xofz: dz=0")
        quit()
   a = dx/dz
   b = r1[0]-a*r1[2]
   x = a*z+b
   return x
	
def yofz(r1,r2,z):
    dz = r2[2]-r1[2]
    dy = r2[1]-r1[1]
    if(dz==0):
        print("ERROR in yofz: dz=0")
        quit()
    a = dy/dz
    b = r1[1]-a*r1[2]
    y = a*z+b
    return y

def zofx(r1,r2,x):
    dz = r2[2]-r1[2]
    dx = r2[0]-r1[0]
    if(dx==0):
        print("ERROR in zofx: dx=0")
        quit()
    a = dz/dx
    b = r1[2]-a*r1[0]
    z = a*x+b
    return z
    
### for uniform magentic field
def getESeed(LB, xExit, zMid):
    B = -0.897
    R = (LB-zMid)*LB/xExit + xExit
    p = 0.3*B*R*mm2m
    return p

### for non-uniform magnetic field, the truth E vs xExit is fit
def getESeedFit(xExit, side="positron"):
    if side=="positron":
        p0 = 0.032373009
        p1 = 25.056499
        p2 = -0.0066455313
    else:
        p0 = 8.65967e-3
        p1 = -2.22942e+1
        p2 = -1.14192e-2
        
    E = p0+p1/(p2+(xExit/10.))
    return E
    

def getR(LB, xExit, zMid):
    R = (LB-zMid)*LB/xExit + xExit
    return R*mm2m
    
def getZValues(staveId):
    zPos = -999.0
    if(staveId == 0 or staveId == 8):
        zPos = 3962.0125
    elif(staveId == 1 or staveId == 9):
        zPos = 3950.0125
    elif(staveId == 2 or staveId == 10):
        zPos = 4062.0125
    elif(staveId == 3 or staveId == 11):
        zPos = 4050.0125
    elif(staveId == 4 or staveId == 12):
        zPos = 4162.0125
    elif(staveId == 5 or staveId == 13):
        zPos = 4150.0125
    elif(staveId == 6 or staveId == 14):
        zPos = 4262.0125
    elif(staveId == 7 or staveId == 15):
        zPos = 4262.0125
    else:
        print("No suitable stave found!!! Exiting")
        quit()
    return zPos

def main():
    LB            = 1440
    zDipoleCenter = 2050
    zDipoleExit   = (zDipoleCenter + LB/2.0)
    parser = argparse.ArgumentParser(description='Code to get 2D plots')
    parser.add_argument('-l', action="store", dest="inFile", type=str, default="signalMC_e0gpc_3.0_trackInfo.txt")
    parser.add_argument('-b', action="store", dest="bx", type=float, default=10.0)
    parser.add_argument('-g', action="store_true", dest="needgLaser")
    args = parser.parse_args()
    
    inDir = '/Users/arkasantra/arka/Sasha_Work/OutputFile'
    
    bkgFileName      = open(inDir+'/'+args.inFile)
    
    withoutText   = args.inFile.split('.txt')[0]
    rootFile      = withoutText+"_EnergyCheck.root"
    nbx           = args.bx
    
    print('BX selected: ',nbx)
    
    outFile       = TFile(inDir+'/'+rootFile, "RECREATE")
    outFile.cd()
    
        
    allHistoDict  = {}
    
    ##/// xExit from truth momentum and layer 1
    allHistoDict.update({"tracking_planes_signal_delta_track_e_positrons_log_0":TH1D("tracking_planes_signal_delta_track_e_positrons_log_0","tracking_planes_signal_delta_track_e_positrons_log_0; (Reconstructed E - True E) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_signal_delta_track_e_positrons_log_1":TH1D("tracking_planes_signal_delta_track_e_positrons_log_1","tracking_planes_signal_delta_track_e_positrons_log_1; (Reconstructed E - True E) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efraction_positrons_log_0":TH1D("tracking_planes_signal_delta_track_efraction_positrons_log_0","tracking_planes_signal_delta_track_efraction_positrons_log_0; (Reconstructed E - True E)/True E; Particles/BX",420, -0.21, 0.21)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efraction_positrons_log_1":TH1D("tracking_planes_signal_delta_track_efraction_positrons_log_1","tracking_planes_signal_delta_track_efraction_positrons_log_1; (Reconstructed E - True E)/True E; Particles/BX",420, -0.21, 0.21)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efit_positrons_log_0":TH1D("tracking_planes_signal_delta_track_efit_positrons_log_0","tracking_planes_signal_delta_track_efit_positrons_log_0; (Reconstructed E - True E) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efit_positrons_log_1":TH1D("tracking_planes_signal_delta_track_efit_positrons_log_1","tracking_planes_signal_delta_track_efit_positrons_log_1; (Reconstructed E - True E) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efitfraction_positrons_log_0":TH1D("tracking_planes_signal_delta_track_efitfraction_positrons_log_0","tracking_planes_signal_delta_track_efitfraction_positrons_log_0; (Reconstructed E - True E)/True E; Particles/BX",500, -0.2,0.2)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efitfraction_positrons_log_1":TH1D("tracking_planes_signal_delta_track_efitfraction_positrons_log_1","tracking_planes_signal_delta_track_efitfraction_positrons_log_1; (Reconstructed E - True E)/True E; Particles/BX",500, -0.2,0.2)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efitfractionvse_positrons_log_0":TH2D("tracking_planes_signal_delta_track_efitfractionvse_positrons_log_0","tracking_planes_signal_delta_track_efitfractionvse_positrons_log_0; True E [GeV]; (Reconstructed E - True E)/True E",100,0,20,420, -0.21, 0.21)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efitfractionvse_positrons_log_1":TH2D("tracking_planes_signal_delta_track_efitfractionvse_positrons_log_1","tracking_planes_signal_delta_track_efitfractionvse_positrons_log_1; True E [GeV]; (Reconstructed E - True E)/True E",100,0,20,420, -0.21, 0.21)})
    allHistoDict.update({"tracking_planes_magnetic_field_0":TH1D("tracking_planes_magnetic_field_0","tracking_planes_magnetic_field_0; B_{effective} [T]; Particles/BX",100, -1.2,0)})
    allHistoDict.update({"tracking_planes_magnetic_field_1":TH1D("tracking_planes_magnetic_field_1","tracking_planes_magnetic_field_1; B_{effective} [T]; Particles/BX",100, -1.2,0)})
    
    
    
    ##/// xExit from truth momentum and layer 4
    allHistoDict.update({"tracking_planes_signal_delta_track_efitfraction_positrons_log_6":TH1D("tracking_planes_signal_delta_track_efitfraction_positrons_log_6","tracking_planes_signal_delta_track_efitfraction_positrons_log_6; (Reconstructed E - True E)/True E; Particles/BX",500, -0.2,0.2)})
    allHistoDict.update({"tracking_planes_signal_delta_track_efitfraction_positrons_log_7":TH1D("tracking_planes_signal_delta_track_efitfraction_positrons_log_7","tracking_planes_signal_delta_track_efitfraction_positrons_log_7; (Reconstructed E - True E)/True E; Particles/BX",500, -0.2,0.2)})
    
    
    ##/// xExit from track fit
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_e_positrons_log_0":TH1D("tracking_planes_slopeFromHits_signal_delta_track_e_positrons_log_0","tracking_planes_slopeFromHits_signal_delta_track_e_positrons_log_0; (Reconstructed E - True E) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_e_positrons_log_1":TH1D("tracking_planes_slopeFromHits_signal_delta_track_e_positrons_log_1","tracking_planes_slopeFromHits_signal_delta_track_e_positrons_log_1; (Reconstructed E - True E) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_efraction_positrons_log_0":TH1D("tracking_planes_slopeFromHits_signal_delta_track_efraction_positrons_log_0","tracking_planes_slopeFromHits_signal_delta_track_efraction_positrons_log_0; (Reconstructed E - True E)/True E; Particles/BX",420, -0.21, 0.21)})
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_efraction_positrons_log_1":TH1D("tracking_planes_slopeFromHits_signal_delta_track_efraction_positrons_log_1","tracking_planes_slopeFromHits_signal_delta_track_efraction_positrons_log_1; (Reconstructed E - True E)/True E; Particles/BX",420, -0.21, 0.21)})
    
    
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_efit_positrons_log_0":TH1D("tracking_planes_slopeFromHits_signal_delta_track_efit_positrons_log_0","tracking_planes_slopeFromHits_signal_delta_track_efit_positrons_log_0; (Reconstructed E - True E) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_efit_positrons_log_1":TH1D("tracking_planes_slopeFromHits_signal_delta_track_efit_positrons_log_1","tracking_planes_slopeFromHits_signal_delta_track_efit_positrons_log_1; (Reconstructed E - True E) [GeV]; Particles/BX",100, -10,10)})
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_0":TH1D("tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_0","tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_0; (Reconstructed E - True E)/True E; Particles/BX",420, -0.21, 0.21)})
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_1":TH1D("tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_1","tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_1; (Reconstructed E - True E)/True E; Particles/BX",420, -0.21, 0.21)})
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_0":TH2D("tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_0","tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_0; True E [GeV]; (Reconstructed E - True E)/True E",100,0,20,400, -1, 1)})
    allHistoDict.update({"tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_1":TH2D("tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_1","tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_1; True E [GeV]; (Reconstructed E - True E)/True E",100,0,20,400, -1, 1)})
    
    
    allHistoDict.update({"tracking_planes_slopeFromHits_magnetic_field_0":TH1D("tracking_planes_slopeFromHits_magnetic_field_0","tracking_planes_slopeFromHits_magnetic_field_0; B_{effective} [T]; Particles/BX",100, -1.2,0)})
    allHistoDict.update({"tracking_planes_slopeFromHits_magnetic_field_1":TH1D("tracking_planes_slopeFromHits_magnetic_field_1","tracking_planes_slopeFromHits_magnetic_field_1; B_{effective} [T]; Particles/BX",100, -1.2,0)})
    
    
    lineCounter    = 0
    particleTracks = {}
    
    ### write the bkg as it is
    for lines in bkgFileName.readlines():
        if '#' in lines:
            continue
        lineCounter += 1
        if(lineCounter%10000==0): print("processed: ", lineCounter)
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
        parentId     = int(eachWord[11])
        pxx          = float(eachWord[12])
        pyy          = float(eachWord[13])
        pzz          = float(eachWord[14])
        
        
        eachTrack = {'xPos':xPos, 'yPos':yPos, 'trackId':trackId, 'pdgId':pdgId, 'weight':weight, 'staveId':staveId, 'energyVal':energyVal, 'parentId':parentId, 'vtx_x':vtx_x, 'vtx_y':vtx_y, 'vtx_z':vtx_z, 'pxx':pxx, 'pyy':pyy, 'pzz':pzz}
        
        particleTracks.setdefault(bxNumber, [])
        particleTracks[bxNumber].append(eachTrack)
        
        if(staveId==0):
            zz     = 3962.0125
        elif(staveId==1):
            zz     = 3950.0125
        elif(staveId==6):
            zz     = 4262.0125
        elif(staveId==7):
            zz     = 4250.0125
        else:
            continue
            
        ### slope using the track truth momentum
        
        xExit = pxx/pzz*(zDipoleExit-zz) + xPos
        yExit = pyy/pzz*(zDipoleExit-zz) + yPos
        
        zmid  = zz - xPos*(pzz/pxx)
        
        reconstructE = getESeed(LB, xExit, zmid)
        deltaE = -(energyVal - reconstructE)
        
        reconstructEFit = getESeedFit(xExit)
        deltaEFit       = -(energyVal - reconstructEFit)
        
        R = getR(LB, xExit, zmid) ## R in m
        
        #print("hit 1: ", pos1, "hit2: ", pos2, " energy1: ", energyVal, " energy2: ",energyVal2, " reconstructE: ", reconstructE, " deltaE: ", deltaE, " vtxDiffX: ", abs(vtx_x - vtx_x2), " vtxDiffY: ", abs(vtx_y - vtx_y2))
        
        if(staveId==0):
            allHistoDict["tracking_planes_signal_delta_track_e_positrons_log_0"].Fill(deltaE)
            allHistoDict["tracking_planes_signal_delta_track_efraction_positrons_log_0"].Fill(deltaE/energyVal)
            allHistoDict["tracking_planes_signal_delta_track_efit_positrons_log_0"].Fill(deltaEFit)
            allHistoDict["tracking_planes_signal_delta_track_efitfraction_positrons_log_0"].Fill(deltaEFit/energyVal)
            allHistoDict["tracking_planes_signal_delta_track_efitfractionvse_positrons_log_0"].Fill(energyVal,deltaEFit/energyVal)
            allHistoDict["tracking_planes_magnetic_field_0"].Fill(energyVal/(0.3*R))
        if(staveId==1):
            allHistoDict["tracking_planes_signal_delta_track_e_positrons_log_1"].Fill(deltaE)
            allHistoDict["tracking_planes_signal_delta_track_efraction_positrons_log_1"].Fill(deltaE/energyVal)
            allHistoDict["tracking_planes_signal_delta_track_efit_positrons_log_1"].Fill(deltaEFit)
            allHistoDict["tracking_planes_signal_delta_track_efitfraction_positrons_log_1"].Fill(deltaEFit/energyVal)
            allHistoDict["tracking_planes_signal_delta_track_efitfractionvse_positrons_log_1"].Fill(energyVal,deltaEFit/energyVal)
            allHistoDict["tracking_planes_magnetic_field_1"].Fill(energyVal/(0.3*R))
        if(staveId==6):
            allHistoDict["tracking_planes_signal_delta_track_efitfraction_positrons_log_6"].Fill(deltaEFit/energyVal)
        if(staveId==7):
            allHistoDict["tracking_planes_signal_delta_track_efitfraction_positrons_log_7"].Fill(deltaEFit/energyVal)
            
        
        
    ### loop over each bxnumber
    for bx in particleTracks:
        listLayer1  = []
        listLayer4  = []
        listLayerE1 = []
        listLayerE4 = []
        print("working on bx: ",bx)
        ### loop over all tracks in one bx
        for listValues in particleTracks[bx]:
            if(listValues['trackId']==1 and listValues['pdgId']==-11):
                zValue = getZValues(listValues['staveId'])
                if(listValues['staveId']==0 or listValues['staveId']==1):
                    listLayer1.append({'xPos':listValues['xPos'],'yPos':listValues['yPos'],'zPos':zValue, 'vtx_x':listValues['vtx_x'], 'vtx_y':listValues['vtx_y'], 'vtx_z':listValues['vtx_z'], 'energyVal':listValues['energyVal'], 'staveId':listValues['staveId']})
                if(listValues['staveId']==6 or listValues['staveId']==7):
                    listLayer4.append({'xPos':listValues['xPos'],'yPos':listValues['yPos'],'zPos':zValue, 'vtx_x':listValues['vtx_x'], 'vtx_y':listValues['vtx_y'], 'vtx_z':listValues['vtx_z'], 'energyVal':listValues['energyVal'], 'staveId':listValues['staveId']})
                if(listValues['staveId']==8 or listValues['staveId']==9):
                    listLayerE1.append({'xPos':listValues['xPos'],'yPos':listValues['yPos'],'zPos':zValue, 'vtx_x':listValues['vtx_x'], 'vtx_y':listValues['vtx_y'], 'vtx_z':listValues['vtx_z'], 'energyVal':listValues['energyVal'], 'staveId':listValues['staveId']})
                if(listValues['staveId']==14 or listValues['staveId']==15):
                    listLayerE4.append({'xPos':listValues['xPos'],'yPos':listValues['yPos'],'zPos':zValue, 'vtx_x':listValues['vtx_x'], 'vtx_y':listValues['vtx_y'], 'vtx_z':listValues['vtx_z'], 'energyVal':listValues['energyVal'], 'staveId':listValues['staveId']})
                    
        ### now match point from layer 1 with layer 4 using the vtx_x and vtx_y positions
        points = 1
        for point1 in listLayer1:
            for point4 in listLayer4:
                if(abs(point1['vtx_x'] - point4['vtx_x']) > 0.0000001): continue
                if(abs(point1['vtx_y'] - point4['vtx_y']) > 0.0000001): continue
                if((point4['xPos'] - point1['xPos'])==0): continue
                if((point4['zPos'] - point1['zPos'])==0): continue
            
                #if(points%1000==0): 
                    #print("matched points: ", points)
                    #print('vtx_x in layer 1 : ', point1['vtx_x'], ' in layer 4 : ', point4['vtx_x'])
                    #print('vtx_y in layer 1 : ', point1['vtx_y'], ' in layer 4 : ', point4['vtx_y'])
                
                slopeX = (point4['xPos'] - point1['xPos'])/(point4['zPos'] - point1['zPos'])
                slopeY = (point4['yPos'] - point1['yPos'])/(point4['zPos'] - point1['zPos'])
                
                ### slope using the track hit
                xExit = slopeX*(zDipoleExit-point1['zPos']) + point1['xPos']
                yExit = slopeY*(zDipoleExit-point1['zPos']) + point1['yPos']
                
                zmid  = point1['zPos'] - point1['xPos']*(1.0/slopeX)
                
                reconstructE = getESeed(LB, xExit, zmid)
                deltaE = -(point1['energyVal'] - reconstructE)
                
                reconstructEFit = getESeedFit(xExit)
                deltaEFit       = -(point1['energyVal'] - reconstructEFit)
                
                R = getR(LB, xExit, zmid) 
                
                
                if(point1['staveId']==0):
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_e_positrons_log_0"].Fill(deltaE)
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_efraction_positrons_log_0"].Fill(deltaE/point1['energyVal'])
                    
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_efit_positrons_log_0"].Fill(deltaEFit)
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_0"].Fill(deltaEFit/point1['energyVal'])
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_0"].Fill(point1['energyVal'], deltaEFit/point1['energyVal'])
                    
                    allHistoDict["tracking_planes_slopeFromHits_magnetic_field_0"].Fill(point1['energyVal']/(0.3*R))
                if(point1['staveId']==1):
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_e_positrons_log_1"].Fill(deltaE)
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_efraction_positrons_log_1"].Fill(deltaE/point1['energyVal'])
                    
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_efit_positrons_log_1"].Fill(deltaEFit)
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_efitfraction_positrons_log_1"].Fill(deltaEFit/point1['energyVal'])
                    allHistoDict["tracking_planes_slopeFromHits_signal_delta_track_efitfractionvse_positrons_log_1"].Fill(point1['energyVal'], deltaEFit/point1['energyVal'])
                    
                    allHistoDict["tracking_planes_slopeFromHits_magnetic_field_1"].Fill(point1['energyVal']/(0.3*R))
                points += 1
    
    for keys in allHistoDict:
        allHistoDict[keys].Scale(1./nbx)
        allHistoDict[keys].Write()
    outFile.Close()
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print("--- The time taken: ", time.time() - start, " s")
