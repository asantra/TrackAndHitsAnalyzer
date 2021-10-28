### setup to make plots for the tracker ###
### This is to plot four particles on top of each other in tracker layer 1 and layer 4. 

import os, sys, glob, time
from ROOT import *
import argparse
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint


def DrawHists(FirstTH1, LegendName, PlotColor,xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, CanvasName, yline1low, yline1up, drawline=False, logy=False, latexName='', latexName2 = '', latexName3='', leftLegend=False, doAtlas=False, doLumi=False, noRatio=False, do80=False, do59=False, drawPattern="", logz=False, logx=False, latexName4=''):
   ##### with mean
   #Tex = MakeLatex(0.40,0.70,latexName)
   #Tex2 = MakeLatex(0.40,0.64,latexName2)
   #Tex3 = MakeLatex(0.40,0.58,latexName3)
   #Tex4 = MakeLatex(0.37,0.57,latexName4)
   debug = False
   if(debug): print "just entering plot code"
   ### without mean
   Tex = MakeLatex(0.39,0.84,latexName)
   Tex2 = MakeLatex(0.39,0.78,latexName2)
   Tex3 = MakeLatex(0.39,0.72,latexName3)
   Tex4 = MakeLatex(0.39,0.66,latexName4)
   
   
   if(debug): print "defining Tex "
   WaterMark = TexWaterMark('Preliminary')
   c = TCanvas("c","c",700, 700)
   gStyle.SetOptStat(0)
   c.cd()
   c.SetGrid(0)
   if(logx):
     c.SetLogx()
   if(logy):
     c.SetLogy()
   if(logz):
       c.SetLogz()
   if(debug): print "Set Logy "
   line = MakeLine(xrange1down,yline1low,xrange1up,yline1up)
   if(leftLegend):
       legend1 = LeftLegendMaker()
   else:
       legend1 = LegendMaker()
       #legend1 = LegendMakerTwoColumn()
   if(debug): print "Set Legend "
   tex1 = TLatex(); tex2 = TLatex(); tex3 = TLatex()
   L = [tex1, tex2, tex3]
   TexMaker(L, doAtlas, doLumi, noRatio, do80, do59)
   stList = []
   #
   if(debug): print "Set Ranges "
   integralList = []; integralListError = []
   strType = str(type(FirstTH1[0]))
   for i in xrange(0, len(FirstTH1)):
     FirstTH1[i].SetLineWidth(1)
     FirstTH1[i] = AxisLabelEtc(FirstTH1[i], yAxisName, xAxisName)
     if("TH1" in strType):
        FirstTH1[i] = SetHistColorEtc(FirstTH1[i], PlotColor[i])
     FirstTH1[i] = getOverflow(FirstTH1[i])
     FirstTH1[i].GetYaxis().SetRangeUser(yrange1down,yrange1up)
     FirstTH1[i].GetXaxis().SetRangeUser(xrange1down,xrange1up)
     
     FirstTH1[i].SetFillColor(0)
     #FirstTH1[0].SetFillColor(0)
     if("TH2D" in strType):
        xBinMax = FirstTH1[i].GetNbinsX()
        yBinMax = FirstTH1[i].GetNbinsY()
        integralList.append(FirstTH1[i].Integral(0, xBinMax+1, 0, yBinMax+1))
     else:
        integralList.append(FirstTH1[i].Integral(0, FirstTH1[i].GetNbinsX()+1))
        
     if(i==0):legend1.AddEntry(FirstTH1[i],LegendName[i]+" ("+str(round(integralList[i],1))+")", "l")
     else: legend1.AddEntry(FirstTH1[i],LegendName[i]+" ("+str(round(integralList[i],1))+")", "l")
     #legend1.AddEntry(FirstTH1[i],LegendName[i], "l")
   
   if(debug): print "After for loop "
   FirstTH1[0].GetXaxis().SetRangeUser(xrange1down,xrange1up)
   if "electrons" in FirstTH1[0].GetName():
       FirstTH1[0].GetZaxis().SetRangeUser(0,40)
   
   gPad.SetTickx()
   gPad.SetTicky()
   #FirstTH1[0].SetFillColor(0)
   
   if "TH2" in strType:
       drawStyle = drawPattern
   else:
        drawStyle = "hist"
   
   FirstTH1[0].Draw(drawStyle) # ce, hist
   
   
   if(debug): print "After first Draw "
   #WaterMark.Draw("sames")
   if(len(FirstTH1)>1):
    for i in xrange(1, len(FirstTH1)):
        FirstTH1[i].Draw(drawStyle+" sames") 
        FirstTH1[i].SetFillColor(0)
        FirstTH1[i].SetLineWidth(2)
        
   if(debug): print "After Draw loop "
   
   Tex.Draw("sames")
   Tex2.Draw("sames")
   Tex3.Draw("sames")
   Tex4.Draw("sames")
   
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
    inputRootFileAl     = "energyRatio_list_root_hics_165gev_w0_3000nm_jeti40_122020_6cac1288SignalPositrons_trackInfoClean.root"
    inputRootFileKp     = "energyRatio_list_root_hics_165gev_w0_3000nm_jeti40_122020_9550dac4SignalPositrons_trackInfoClean.root"
    inFileAl            = TFile(inputDir+"/"+inputRootFileAl)
    inFileKp            = TFile(inputDir+"/"+inputRootFileKp)
    
    hEnergyRatioAl            = inFileAl.Get("hEnergyRatio")
    hEnergyDiffAl             = inFileAl.Get("hEnergyDiff")
    hEnergyIPAl               = inFileAl.Get("hEnergyIP")
    hEnergyTrackerAl          = inFileAl.Get("hEnergyTracker")
    hEnergyDiffVsEipAl        = inFileAl.Get("hEnergyDiffVsEip")
    hDeltaXAl                 = inFileAl.Get("hDeltaX")
    hDeltaXFractionAl         = inFileAl.Get("hDeltaXFraction")
    hDeltaXFractionVsXFieldAl = inFileAl.Get("hDeltaXFractionVsXField")
    hDeltaXFractionVsXSimulationAl = inFileAl.Get("hDeltaXFractionVsXSimulation")
    hDeltaYAl                 = inFileAl.Get("hDeltaY")
    hDeltaYFractionAl         = inFileAl.Get("hDeltaYFraction")
    hDeltaYFractionVsYFieldAl = inFileAl.Get("hDeltaYFractionVsYField")
    hDeltaXMagnetAl           = inFileAl.Get("hDeltaXMagnet")
    hStaveZVsXFieldAl         = inFileAl.Get("hStaveZVsXField")
    hXSimulationVsXFieldAl    = inFileAl.Get("hXSimulationVsXField")
    
    
    hEnergyRatioKp            = inFileKp.Get("hEnergyRatio")
    hEnergyDiffKp             = inFileKp.Get("hEnergyDiff")
    hEnergyIPKp               = inFileKp.Get("hEnergyIP")
    hEnergyTrackerKp          = inFileKp.Get("hEnergyTracker")
    hEnergyDiffVsEipKp        = inFileKp.Get("hEnergyDiffVsEip")
    hDeltaXKp                 = inFileKp.Get("hDeltaX")
    hDeltaXFractionKp         = inFileKp.Get("hDeltaXFraction")
    hDeltaXFractionVsXFieldKp = inFileKp.Get("hDeltaXFractionVsXField")
    hDeltaXFractionVsXSimulationKp = inFileKp.Get("hDeltaXFractionVsXSimulation")
    hDeltaYKp                 = inFileKp.Get("hDeltaY")
    hDeltaYFractionKp         = inFileKp.Get("hDeltaYFraction")
    hDeltaYFractionVsYFieldKp = inFileKp.Get("hDeltaYFractionVsYField")
    hDeltaXMagnetKp           = inFileKp.Get("hDeltaXMagnet")
    hStaveZVsXFieldKp         = inFileKp.Get("hStaveZVsXField")
    hXSimulationVsXFieldKp    = inFileKp.Get("hXSimulationVsXField")
    
    print("Al:", hEnergyDiffAl.Integral())
    print("Kp:", hEnergyDiffKp.Integral())
    
    outDir = "EnergyRatioPlots"
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    
    #### plotting the signal and background
    drawline    = False
    latexName   = 'w_{0}: 3000 nm'
    latexName2  = 'Signal e^{+}'
    latexName3  = ''
    leftLegend  = True
    doAtlas     = False
    doLumi      = False
    noRatio     = False
    do80        = False
    do59        = False
    
    AlDistorted = hEnergyDiffAl.Integral(12, 121)/hEnergyDiffAl.Integral(0, 121)
    KpDistorted = hEnergyDiffKp.Integral(12, 121)/hEnergyDiffKp.Integral(0, 121)
    
    print("Fraction of tracks distorted for Al window: ", round(AlDistorted,3))
    print("Fraction of tracks distorted for Kp window: ", round(KpDistorted,3))
    
    LegendName  = ["Al window", "Kapton window"]
    PlotColor   = [2, 4]
    FirstTH1    = [hEnergyRatioAl, hEnergyRatioKp]
    
    DrawHists(FirstTH1, LegendName, PlotColor, "E_{Tracker}^{Face}/E_{IP}", "Particles/BX", 0.0, 1.2, 2e-3, 8e3, outDir+"/EnergyRatio", 1, 1, False, True, latexName, latexName2, latexName3)
    
    
    
    FirstTH1    = [hEnergyDiffAl, hEnergyDiffKp]
    DrawHists(FirstTH1, LegendName, PlotColor, "1-(E_{Tracker}^{Face}/E_{IP})", "Particles/BX", 0.0, 1.2, 2e-3, 8e3, outDir+"/EnergyDiff", 1, 1, False, True, latexName, latexName2, latexName3)
    
    
    FirstTH1    = [hDeltaXFractionAl, hDeltaXFractionKp]
    DrawHists(FirstTH1, LegendName, PlotColor, "1-(x_{Tracker}^{Face}/x_{Field})", "Particles/BX", -0.2, 0.2, 2e-4, 8e3, outDir+"/DeltaXFraction", 1, 1, False, True, latexName, latexName2, latexName3)
    
    FirstTH1    = [hDeltaYFractionAl, hDeltaYFractionKp]
    DrawHists(FirstTH1, LegendName, PlotColor, "1-(y_{Tracker}^{Face}/y_{Field})", "Particles/BX", -0.5, 0.5, 2e-4, 8e3, outDir+"/DeltaYFraction", 1, 1, False, True, latexName, latexName2, latexName3)
    
    
    
    LegendName  = ["Tracker face", "IP"]
    #PlotColor   = [4, 2]
    h2 = hEnergyIPAl.Clone('h2')
    h2.Reset()
    h2.GetYaxis().SetTitle("#frac{E_{Tracker}}{E_{IP}}")
    h3 = hEnergyIPKp.Clone('h3')
    h3.Reset()
    h3.GetYaxis().SetTitle("#frac{E_{Tracker}}{E_{IP}}")
    h4 = hDeltaXAl.Clone('h4')
    h4.Reset()
    h4.GetYaxis().SetTitle("Al/Kp")
    
    drawline = True
    logy     = True
    
    FirstTH1    = [hEnergyTrackerAl, hEnergyIPAl]
    latexName   = 'w_{0}: 3000 nm; Al window'
    DrawHistsRatio(FirstTH1, LegendName, PlotColor, 0, 14, 2e-3, 8e2, "E [GeV]", outDir+"/EnergyAl", h2, 1.0, 1.0, drawline, logy, latexName, latexName2)
    
    
    FirstTH1    = [hDeltaXAl, hDeltaXKp]
    LegendName  = ["Al window", "Kp window"]
    latexName   = 'w_{0}: 3000 nm'
    latexName2  = 'Signal e^{+}: tracker face'
    DrawHistsRatio(FirstTH1, LegendName, PlotColor, -30, 30, 2e-4, 3e2, "#Delta x(tracker, field) [mm]", outDir+"/DeltaX", h4, 1.0, 1.0, drawline, logy, latexName, latexName2)
    
    h5 = hDeltaXMagnetAl.Clone('h5')
    h5.Reset()
    h5.GetYaxis().SetTitle("Al/Kp")
    FirstTH1    = [hDeltaXMagnetAl, hDeltaXMagnetKp]
    LegendName  = ["Al window", "Kp window"]
    latexName   = 'w_{0}: 3000 nm'
    latexName2 = 'Signal e^{+}: Vacuum exit window'
    DrawHistsRatio(FirstTH1, LegendName, PlotColor, -200, 200, 2e-4, 3e2, "#Delta x(trackExtrapolate, MagneticField) [mm]", outDir+"/DeltaXMagnet", h5, 1.0, 1.0, drawline, logy, latexName, latexName2)
    
    
    
    latexName2  = 'Signal e^{+}'
    LegendName  = ["Tracker face", "IP"]
    FirstTH1    = [hEnergyTrackerKp, hEnergyIPKp]
    latexName   = 'w_{0}: 3000 nm; Kapton window'
    DrawHistsRatio(FirstTH1, LegendName, PlotColor, 0, 14, 2e-3, 8e2, "E [GeV]", outDir+"/EnergyKp", h2, 1.0, 1.0, drawline, logy, latexName, latexName2)
    
    
    FirstTH1    = [hEnergyTrackerKp, hEnergyIPKp]
    latexName   = 'w_{0}: 3000 nm; Kapton window'
    DrawHistsRatio(FirstTH1, LegendName, PlotColor, 0, 14, 2e-3, 8e2, "E [GeV]", outDir+"/EnergyKp", h2, 1.0, 1.0, drawline, logy, latexName, latexName2)
    
    
    FirstTH1    = [hDeltaXFractionAl, hDeltaXFractionKp]
    LegendName  = ["Al window", "Kp window"]
    hDeltaXFractionAl.Rebin(4)
    hDeltaXFractionKp.Rebin(4)
    
    h6 = hDeltaXFractionAl.Clone('h6')
    h6.Reset()
    h6.GetYaxis().SetTitle("Al/Kp")
    
    latexName   = 'w0: 3000 nm'
    DrawHistsRatio(FirstTH1, LegendName, PlotColor, -0.1, 0.1, 2e-4, 8e1, "1-(x^{Face}_{Tracker}/x_{Field})", outDir+"/DeltaXFractionRatio", h6, 1.0, 1.0, drawline, logy, latexName, latexName2)
    
    
    
    
    FirstTH1    = [hDeltaYFractionAl, hDeltaYFractionKp]
    LegendName  = ["Al window", "Kp window"]
    #hDeltaXFractionAl.Rebin(4)
    #hDeltaXFractionKp.Rebin(4)
    
    h7 = hDeltaYFractionAl.Clone('h6')
    h7.Reset()
    h7.GetYaxis().SetTitle("Al/Kp")
    
    latexName   = 'w0: 3000 nm'
    DrawHistsRatio(FirstTH1, LegendName, PlotColor, -0.1, 0.1, 2e-3, 8e2, "1-(y^{Face}_{Tracker}/y_{Field})", outDir+"/DeltaYFractionRatio", h7, 1.0, 1.0, drawline, logy, latexName, latexName2)
    
    
    
    
    
    #### 4 plots in one canvas
    
    FirstTH1    = [hEnergyTrackerAl, hEnergyIPAl, hEnergyTrackerKp, hEnergyIPKp]
    LegendName  = ["E_{Tracker}^{Face} (Al)", "E_{IP} (Al)", "E_{Tracker}^{Face} (Kp)", "E_{IP} (Kp)"]
    PlotColor   = [2, 2, 4, 4]
    
    latexName   = 'w_{0}: 3000 nm'
    
    h2.GetYaxis().SetTitle("Al")
    h3.GetYaxis().SetTitle("Kp")
    
    doSumw2     = False
    TeVTag      = False
    DrawHistsRatioTwo(FirstTH1, LegendName, PlotColor, 0, 14, 2e-3, 2e2, outDir+"/EnergyAlKp", h2, h3, 1.0, 1.0, drawline, logy, doSumw2, TeVTag, latexName, latexName2)
    
    
    
    ### 2D plots
    
    logz       = False
    
    FirstTH1   = [hEnergyDiffVsEipAl]
    LegendName = ["Al window"]
    latexName2 = 'Signal e^{+}; Al window'
    Draw2DHists(FirstTH1, LegendName, "E_{IP} [GeV]", "1 - (#frac{E_{Tracker}^{Face}}{E_{IP}})", "Particles/BX", 0.0, 14.0, 0.0, 1.05, 0, 24, outDir+"/EFracVsE_Al", logz, latexName, latexName2)
    
    FirstTH1   = [hEnergyDiffVsEipKp]
    LegendName = ["Kapton window"]
    latexName2 = 'Signal e^{+}; Kp window'
    Draw2DHists(FirstTH1, LegendName, "E_{IP} [GeV]", "1 - (#frac{E_{Tracker}^{Face}}{E_{IP}})", "Particles/BX", 0.0, 14.0, 0.0, 1.05, 0, 24, outDir+"/EFracVsE_Kp", logz, latexName, latexName2)
    
    
    FirstTH1   = [hDeltaXFractionVsXFieldAl]
    LegendName = ["Al window"]
    latexName2 = 'Signal e^{+}; Al window'
    Draw2DHists(FirstTH1, LegendName, "x_{Field} [mm]", "1 - (#frac{x_{Tracker}^{Face}}{x_{Field}})", "Particles/BX", 0.0, 600.0, -0.2, 0.2, 0, 0.2, outDir+"/DeltaXVsX_Al", logz, latexName, latexName2)
    
    FirstTH1   = [hDeltaXFractionVsXFieldKp]
    LegendName = ["Kp window"]
    latexName2 = 'Signal e^{+}; Kp window'
    Draw2DHists(FirstTH1, LegendName, "x_{Field} [mm]", "1 - (#frac{x_{Tracker}^{Face}}{x_{Field}})", "Particles/BX", 0.0, 600.0, -0.2, 0.2, 0, 0.2, outDir+"/DeltaXVsX_Kp", logz, latexName, latexName2)
    
    
    FirstTH1   = [hDeltaXFractionVsXSimulationAl]
    LegendName = ["Al window"]
    latexName2 = 'Signal e^{+}; Al window'
    Draw2DHists(FirstTH1, LegendName, "x_{Tracker}^{Face} [mm]", "1 - (#frac{x_{Tracker}^{Face}}{x_{Field}})", "Particles/BX", 0.0, 600.0, -0.2, 0.2, 0, 0.2, outDir+"/DeltaXVsXSimul_Al", logz, latexName, latexName2)
    
    FirstTH1   = [hDeltaXFractionVsXSimulationKp]
    LegendName = ["Kp window"]
    latexName2 = 'Signal e^{+}; Kp window'
    Draw2DHists(FirstTH1, LegendName, "x_{Tracker}^{Face} [mm]", "1 - (#frac{x_{Tracker}^{Face}}{x_{Field}})", "Particles/BX", 0.0, 600.0, -0.2, 0.2, 0, 0.2, outDir+"/DeltaXVsXSimul_Kp", logz, latexName, latexName2)
    
    
    FirstTH1   = [hStaveZVsXFieldAl]
    LegendName = ["Al window"]
    latexName2 = 'Signal e^{+}; Al window'
    Draw2DHists(FirstTH1, LegendName, "x_{Field} [mm]", "stave Z [mm]", "Particles/BX", 0.0, 600.0, 3850, 3900, 0, 5, outDir+"/StaveZVsXField_Al", logz, latexName, latexName2)
    
    FirstTH1   = [hXSimulationVsXFieldAl]
    LegendName = ["Al window"]
    latexName2 = 'Signal e^{+}; Al window'
    Draw2DHists(FirstTH1, LegendName, "x_{Field} [mm]", "x_{Tracker}^{Face} [mm]", "Particles/BX", 0.0, 600.0, 0.0, 600.0, 0, 5, outDir+"/XSimulationVsXField_Al", logz, latexName, latexName2)
    
    
    FirstTH1   = [hStaveZVsXFieldKp]
    LegendName = ["Kp window"]
    latexName2 = 'Signal e^{+}; Kp window'
    Draw2DHists(FirstTH1, LegendName, "x_{Field} [mm]", "stave Z [mm]", "Particles/BX", 0.0, 600.0, 3850, 3900, 0, 5, outDir+"/StaveZVsXField_Kp", logz, latexName, latexName2)
    
    FirstTH1   = [hXSimulationVsXFieldKp]
    LegendName = ["Kp window"]
    latexName2 = 'Signal e^{+}; Kp window'
    Draw2DHists(FirstTH1, LegendName, "x_{Field} [mm]", "x_{Tracker}^{Face} [mm]", "Particles/BX", 0.0, 600.0, 0.0, 600.0, 0, 5, outDir+"/XSimulationVsXField_Kp", logz, latexName, latexName2)
    
    
    
    
    FirstTH1   = [hDeltaXFractionVsXSimulationKp]
    LegendName = ["Kp window"]
    latexName2 = 'Signal e^{+}; Kp window'
    Draw2DHists(FirstTH1, LegendName, "x_{Tracker}^{Face} [mm]", "1 - (#frac{x_{Tracker}^{Face}}{x_{Field}})", "Particles/BX", 0.0, 600.0, -0.2, 0.2, 0, 0.2, outDir+"/DeltaXVsXSimul_Kp", logz, latexName, latexName2)
    
    
    FirstTH1   = [hDeltaYFractionVsYFieldAl]
    LegendName = ["Al window"]
    latexName2 = 'Signal e^{+}; Al window'
    Draw2DHists(FirstTH1, LegendName, "y_{Field} [mm]", "1 - (#frac{y_{Tracker}^{Face}}{y_{Field}})", "Particles/BX", -7.5, 7.5, -0.5, 0.5, 0, 50, outDir+"/DeltaYVsY_Al", logz, latexName, latexName2)
    
    FirstTH1   = [hDeltaYFractionVsYFieldKp]
    LegendName = ["Kp window"]
    latexName2 = 'Signal e^{+}; Kp window'
    Draw2DHists(FirstTH1, LegendName, "y_{Field} [mm]", "1 - (#frac{y_{Tracker}^{Face}}{y_{Field}})", "Particles/BX", -7.5, 7.5, -0.5, 0.5, 0, 50, outDir+"/DeltaYVsY_Kp", logz, latexName, latexName2)
    
    
    
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print "The total time taken: ", time.time() - start, " s"
