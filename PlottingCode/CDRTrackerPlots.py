### setup to make plots for the tracker ###
### This is to plot four particles on top of each other in tracker layer 1 and layer 4. 

import os, sys, glob, time
from ROOT import *
import argparse
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint


#### This is a special function to draw one canvas with 8 different histograms
def DrawHistsOneCanvas(FirstTH1, LegendName, PlotColor,xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, CanvasName, yline1low, yline1up, drawline=False, logy=False, latexName='', latexName2 = '', latexName3='', leftLegend=False, doAtlas=False, doLumi=False, noRatio=False, do80=False, do59=False, drawPattern="", logz=False, logx=False):
   debug = False
   if(debug): print ("just entering plot code")
   histName = FirstTH1[0].GetName()
   
   if(debug): print ("defining Tex ")
   WaterMark = TexWaterMark('Preliminary')
   c = TCanvas("c","c",1000, 700)
   gStyle.SetOptStat(0)
   c.cd()
   #c.SetGrid()
   if(logx):
     c.SetLogx()
   if(logy):
     c.SetLogy()
   if(logz):
       c.SetLogz()
   if(debug): print ("Set Logy ")
   line = MakeLine(xrange1down,yline1low,xrange1up,yline1up)
   if(leftLegend):
       #legend1 = LeftLegendMaker()
       legend1 = LegendMakerTwoColumn()
   else:
       #legend1 = LegendMaker()
       legend1 = LegendMakerTwoColumn()
   if(debug): print ("Set Legend ")
   tex1 = TLatex(); tex2 = TLatex(); tex3 = TLatex()
   L = [tex1, tex2, tex3]
   TexMaker(L, doAtlas, doLumi, noRatio, do80, do59)
   stList = []
   #FirstTH1[0].GetYaxis().SetRangeUser(yrange1down,yrange1up)
   if(debug): print ("Set Ranges ")
   integralList = []; integralListError = []
   strType = str(type(FirstTH1[0]))
   
   

   for i in range(0, len(FirstTH1)):
     FirstTH1[i].Rebin(10)
     FirstTH1[i].GetYaxis().SetTitleOffset(1.4);
     FirstTH1[i].GetXaxis().SetTitleOffset(1.4);
     FirstTH1[i].GetYaxis().SetNdivisions(8)
     FirstTH1[i].SetYTitle(yAxisName)
     FirstTH1[i].SetXTitle(xAxisName)
     FirstTH1[i].SetLineWidth(2)
     #FirstTH1[i] = AxisLabelEtc(FirstTH1[i], yAxisName, xAxisName)
     FirstTH1[i] = SetHistColorEtc(FirstTH1[i], PlotColor[i])
     FirstTH1[i] = getOverflow(FirstTH1[i])
     FirstTH1[i].GetXaxis().SetRangeUser(xrange1down,xrange1up)
     FirstTH1[i].GetYaxis().SetRangeUser(yrange1down,yrange1up)
     if(i==3 or i==7):
         FirstTH1[i].SetFillColor(PlotColor[i])
         #FirstTH1[i].SetFillStyle(4050)
        
     else:    
         FirstTH1[i].SetFillColor(0)
     
     if(i>3 and i!=7):
         FirstTH1[i].SetLineStyle(7)
     else:
         FirstTH1[i].SetLineStyle(1)
       
     if("TH1" in strType):
        integralList.append(FirstTH1[i].Integral(0, FirstTH1[i].GetNbinsX()+1))
     else:
        xBinMax = FirstTH1[i].GetNbinsX()
        yBinMax = FirstTH1[i].GetNbinsY()
        integralList.append(FirstTH1[i].Integral(0, xBinMax+1, 0, yBinMax+1))
     
     
    
   
   if(debug): print ("After for loop ")
   
   gPad.SetTickx()
   gPad.SetTicky()
   
   if "TH2" in strType:
       drawStyle = drawPattern
   else:
        drawStyle = "hist"
   
   legend1.AddEntry(FirstTH1[0], LegendName[0], "l")
   legend1.AddEntry(FirstTH1[1], LegendName[1], "l")
   legend1.AddEntry(FirstTH1[4], LegendName[4], "l")
   legend1.AddEntry(FirstTH1[5], LegendName[5], "l")
   legend1.AddEntry(FirstTH1[2], LegendName[2], "l")
   legend1.AddEntry(FirstTH1[3], LegendName[3], "f")
   legend1.AddEntry(FirstTH1[6], LegendName[6], "l")
   legend1.AddEntry(FirstTH1[7], LegendName[7], "f")
   
   FirstTH1[3].SetFillColor(PlotColor[3])
   FirstTH1[7].SetFillColor(PlotColor[7])
   FirstTH1[3].Draw(drawStyle)
   FirstTH1[7].Draw(drawStyle+" same")
   FirstTH1[0].Draw(drawStyle+" same")
   FirstTH1[4].Draw(drawStyle+" same")
   FirstTH1[1].Draw(drawStyle+" same")
   FirstTH1[5].Draw(drawStyle+" same")
   FirstTH1[2].Draw(drawStyle+" same")
   FirstTH1[6].Draw(drawStyle+" same")
   FirstTH1[3].GetXaxis().Draw("same")
   LUXELabel(0.2,0.85,"CDR")
   ### without mean
   Tex = MakeLatex(0.58,0.65,latexName)
   Tex2 = MakeLatex(0.387,0.80,latexName2)
   Tex3 = MakeLatex(0.58,0.53,latexName3)
   gPad.Modified()
   gPad.Update()
   c.Modified()
   c.Update()
   if "TH2" in strType:
    pl = FirstTH1[0].GetListOfFunctions().FindObject("palette")
    pl.SetX1NDC(0.905);
    pl.SetX2NDC(0.919);
    pl.SetY1NDC(0.10);
    pl.SetY2NDC(0.90);
    #gPad.Update();
   if(debug): print ("After first Draw ")
   #WaterMark.Draw("sames")
        
   if(debug): print ("After Draw loop ")
   
   Tex.Draw("sames")
   Tex2.Draw("sames")
   Tex3.Draw("sames")
   #if(drawline):
     #line.Draw()
   L[0].Draw()
   L[1].Draw()
   L[2].Draw()
   legend1.Draw()
   
   SaveFile(c, CanvasName)
   return [c,L,legend1]




def main():
    gROOT.LoadMacro("LuxeStyle.C")
    gROOT.LoadMacro("LuxeLabels.C")
    gROOT.SetBatch()
    SetLuxeStyle()
    inputDir            = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inputTracksRootFile = sys.argv[1]
    ### old file, before the normalization fix
    #eLaserHicsRootFile  = "list_root_hics_165gev_w0_3000nm_WIS.root"
    ### new file, after the normalization fix
    #eLaserHicsRootFile  = "list_root_hics_165gev_w0_3000nm_jeti40_122020_9550dac4.root"
    eLaserHicsRootFile  = "list_root_hics_165gev_w0_8000nm_jeti40_122020_9550dac4.root"
    eLaserHicsFile      = TFile(inputDir+"/"+eLaserHicsRootFile)
    
    plotSuffixName      = ""
    if (("_" in inputTracksRootFile) and ("All" not in inputTracksRootFile)):
        eachName            = inputTracksRootFile.split('.')[0].split('_')
        inTracksFile        = TFile(inputDir+"/"+inputTracksRootFile)
        suffixName          = "_".join(eachName[2:])
        outDir              = "DistributionPlotsCDRJan2021_8000nm_"+suffixName
        plotSuffixName      = suffixName
    else:
        inTracksFile        = TFile(inputDir+"/"+inputTracksRootFile)
        outDir              = "DistributionPlotsLikeCDRJan2021_8000nm_"+inputTracksRootFile.split('.')[0]
        plotSuffixName      = inputTracksRootFile.split('.')[0]
    
    
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    baseHistogramNames  = {}
    
    
    baseHistogramNames["tracking_planes_background_track_x_gamma"]                           = ["#it{x} position [mm]", "Particles/BX", 0.0, 600.0, 1e-8, 1e7, True, "hist", False, False]
    baseHistogramNames["tracking_planes_background_track_x_electrons"]                       = ["#it{x} position [mm]", "Particles/BX", 0.0, 600.0, 1e-8, 1e7, True, "hist", False, False]
    baseHistogramNames["tracking_planes_background_track_x_positrons"]                       = ["#it{x} position [mm]", "Particles/BX", 0.0, 600.0, 1e-8, 1e7, True, "hist", False, False]
    baseHistogramNames["tracking_planes_signal_track_x_positrons"]                           = ["#it{x} position [mm]", "Particles/BX", 0.0, 600.0, 1e-8, 1e7, True, "hist", False, False]
    
    baseHistogramNames["tracking_planes_background_track_x_gamma_sumE"]                      = ["#it{x} position [mm]", "#sum E/BX [GeV]", 0.0, 600.0, 1e-10, 1e6, True, "hist", False, False]
    baseHistogramNames["tracking_planes_background_track_x_electrons_sumE"]                  = ["#it{x} position [mm]", "#sum E/BX [GeV]", 0.0, 600.0, 1e-10, 1e6, True, "hist", False, False]
    baseHistogramNames["tracking_planes_background_track_x_positrons_sumE"]                  = ["#it{x} position [mm]", "#sum E/BX [GeV]", 0.0, 600.0, 1e-10, 1e6, True, "hist", False, False]
    baseHistogramNames["tracking_planes_signal_track_x_positrons_sumE"]                      = ["#it{x} position [mm]", "#sum E/BX [GeV]", 0.0, 600.0, 1e-10, 1e6, True, "hist", False, False]
    
    
    
    
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
                #if("signal" in name):
                    #print("I am scaling down")
                    #h.Scale(0.7/1000.0) ### scale down the signal to have effective 8000nm to each BX
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
    latexName2  = 'Tracker layer 1'
    latexName3  = ''
    leftLegend  = True
    doAtlas     = False
    doLumi      = False
    noRatio     = False
    do80        = False
    do59        = False
    
    
    
    PlotColor1  = [2, kBlack, 4, kGray, 2, kBlack, 4, kGray+1]
    
    #### plotting the layer 0, first layer
    LegendName1 = []
    
    LegendName1.append("#gamma, Bkg, Inner stave")
    LegendName1.append("e^{-}, Bkg, Inner stave")
    LegendName1.append("e^{+}, Bkg, Inner stave")
    LegendName1.append("e^{+}, Sig, Inner stave")
    LegendName1.append("#gamma, Bkg, Outer stave")
    LegendName1.append("e^{-}, Bkg, Outer stave")
    LegendName1.append("e^{+}, Bkg, Outer stave")
    LegendName1.append("e^{+}, Sig, Outer stave")
    
    
    
    fourKeyName = ["tracking_planes_background_track_x_gamma_sumE", "tracking_planes_background_track_x_electrons_sumE", "tracking_planes_background_track_x_positrons_sumE", "tracking_planes_signal_track_x_positrons_sumE"]
    
    logy        = False
    if baseHistogramNames[fourKeyName[0]][6]:
        logy = True
        print ("I am in ", fourKeyName[0])
    
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    
    ### overlay e+laser signal on top of electron beam only plot
    if(("electronBackground" in plotSuffixName) or ("EBeamOnly" in plotSuffixName) or ("hics_background" in plotSuffixName) or ("AllEPlusLaser" in plotSuffixName)):
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
    if(("electronBackground" in plotSuffixName) or ("EBeamOnly" in plotSuffixName) or ("hics_background" in plotSuffixName) or ("AllEPlusLaser" in plotSuffixName)):
        FirstTH1   += eLaserSignalHistogramDict[fourKeyName[3]] 
    else:
        FirstTH1   += signalHistogramDict[fourKeyName[3]]
    
    OnlyLayer1 = [FirstTH1[0], FirstTH1[8], FirstTH1[16], FirstTH1[24]]
    OnlyLayer1 += [FirstTH1[1], FirstTH1[9], FirstTH1[17], FirstTH1[25]]        
    
    DrawHistsOneCanvas(OnlyLayer1, LegendName1, PlotColor1, baseHistogramNames[fourKeyName[0]][0], baseHistogramNames[fourKeyName[0]][1], baseHistogramNames[fourKeyName[0]][2], baseHistogramNames[fourKeyName[0]][3], baseHistogramNames[fourKeyName[0]][4], baseHistogramNames[fourKeyName[0]][5], outDir+"/"+fourKeyName[0]+"_Layer1"+"_"+plotSuffixName, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, baseHistogramNames[fourKeyName[0]][7], baseHistogramNames[fourKeyName[0]][8], baseHistogramNames[fourKeyName[0]][9])
    
    latexName2   = 'Tracker layer 4'
    
    
    
    #### plotting the layer 1, first layer
    
    fourKeyName = ["tracking_planes_background_track_x_gamma_sumE", "tracking_planes_background_track_x_electrons_sumE", "tracking_planes_background_track_x_positrons_sumE", "tracking_planes_signal_track_x_positrons_sumE"]
    
    logy        = False
    if baseHistogramNames[fourKeyName[0]][6]:
        logy = True
        print ("I am in ", fourKeyName[0])
    
    FirstTH1    = backgroundHistogramDict[fourKeyName[0]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[1]]
    FirstTH1   += backgroundHistogramDict[fourKeyName[2]]
    ### overlay e+laser signal on top of electron beam only plot
    if(("electronBackground" in plotSuffixName) or ("EBeamOnly" in plotSuffixName) or ("hics_background" in plotSuffixName) or ("AllEPlusLaser" in plotSuffixName)):
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
    if(("electronBackground" in plotSuffixName) or ("EBeamOnly" in plotSuffixName) or ("hics_background" in plotSuffixName) or ("AllEPlusLaser" in plotSuffixName)):
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
