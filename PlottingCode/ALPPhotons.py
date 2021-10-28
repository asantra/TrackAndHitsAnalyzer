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
   Tex = MakeLatex(0.37,0.84,latexName)
   Tex2 = MakeLatex(0.37,0.78,latexName2)
   Tex3 = MakeLatex(0.37,0.72,latexName3)
   Tex4 = MakeLatex(0.37,0.66,latexName4)
   
   
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
     
     FirstTH1[0].SetFillColor(PlotColor[0])
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
   #legend1.Draw()
   
   SaveFile(c, CanvasName)
   return [c,L,legend1]



def main():
    gROOT.LoadMacro("LuxeStyle.C")
    gROOT.LoadMacro("LuxeLabels.C")
    gROOT.SetBatch()
    SetLuxeStyle()
    inputDir            = "/Users/arkasantra/arka/Sasha_Work/OutputFile"
    inputRootFile       = "PhotonAcceptanceFiles_photons_from_gbeam_JETI40_025fs_6500nm_ALPMass0.20893GeV_oneOverLambda0.00005011872_0.0GeVPhotonCut_V2.root"
    alpFile             = TFile(inputDir+"/"+inputRootFile)
    
    
    outDir = "ALPEnergy"
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    h_OutgoingPhotonE = alpFile.Get("h_OutgoingPhotonE")
    
    #### plotting the signal and background
    drawline    = False
    latexName   = ''
    latexName2  = 'Layer 1'
    latexName3  = ''
    leftLegend  = True
    doAtlas     = False
    doLumi      = False
    noRatio     = False
    do80        = False
    do59        = False
    
    
    FirstTH1   = [h_OutgoingPhotonE]
    PlotColor  = [kGray]
    
    
    DrawHists(FirstTH1, [''], PlotColor, "E [GeV]", "Number of photons", 0.0, 16.0, 1e5, 1e16, outDir+"/ALPPhotonEnergy", 1, 1, False, True, 'ALP#rightarrow#gamma#gamma')
    
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print "The total time taken: ", time.time() - start, " s"
