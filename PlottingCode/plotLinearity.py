### setup to make plots for the tracker ###
### This is to plot four particles on top of each other in tracker layer 1 and layer 4. 

import os, sys, glob, time
from ROOT import *
import argparse
import array
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
   c = TCanvas("c","c",900, 900)
   gStyle.SetOptStat(0)
   c.cd()
   c.SetLogx()
   #c.SetGrid()
   if(logx):
     c.SetLogx()
   if(logy):
     c.SetLogy()
   if(logz):
       c.SetLogz()
   if(debug): print ("Set Logy ")
   print(xrange1down, " ", xrange1up, " ", yrange1down, " ", yrange1up)
   line = MakeLine(1,1,5400,5400)
   if(leftLegend):
       #legend1 = LeftLegendMaker()
       legend1 = LegendMaker()
   else:
       #legend1 = LegendMaker()
       legend1 = LegendMaker()
   if(debug): print ("Set Legend ")
   tex1 = TLatex(); tex2 = TLatex(); tex3 = TLatex()
   L = [tex1, tex2, tex3]
   TexMaker(L, doAtlas, doLumi, noRatio, do80, do59)
   stList = []
   FirstTH1[0].GetYaxis().SetRangeUser(yrange1down,yrange1up)
   FirstTH1[0].GetXaxis().SetRangeUser(xrange1down,xrange1up)
   if(debug): print ("Set Ranges ")
   
   

   for i in range(0, len(FirstTH1)):
     #FirstTH1[i].Rebin(10)
     FirstTH1[i].GetYaxis().SetTitleOffset(1.4);
     FirstTH1[i].GetXaxis().SetTitleOffset(1.4);
     FirstTH1[i].GetYaxis().SetNdivisions(8)
     FirstTH1[i].GetYaxis().SetTitle(yAxisName)
     FirstTH1[i].GetXaxis().SetTitle(xAxisName)
     FirstTH1[i].SetLineWidth(1)
     
     #FirstTH1[i] = AxisLabelEtc(FirstTH1[i], yAxisName, xAxisName)
     FirstTH1[i] = SetHistColorEtc(FirstTH1[i], PlotColor[i])
     FirstTH1[i].SetMarkerSize(1.25)
     legend1.AddEntry(FirstTH1[i], LegendName[i], "lp")
     FirstTH1[i].SetLineWidth(2)
     
     
    
   
   if(debug): print ("After for loop ")
   
   gPad.SetTickx()
   gPad.SetTicky()
   
   FirstTH1[0].GetXaxis().SetLimits(xrange1down,xrange1up)
   FirstTH1[0].Draw("ALP")
   if len(FirstTH1) > 1:
       for i in range(1, len(FirstTH1)):
           print(i)
           FirstTH1[i].Draw("LP same")
           gPad.Update()
   
   
   LUXELabel(0.2,0.85,"TDR")
   ### without mean
   Tex = MakeLatex(0.58,0.65,latexName)
   Tex2 = MakeLatex(0.387,0.80,latexName2)
   Tex3 = MakeLatex(0.58,0.53,latexName3)
   gPad.Modified()
   gPad.Update()
   c.Modified()
   c.Update()
   
   if(debug): print ("After first Draw ")
   #WaterMark.Draw("sames")
        
   if(debug): print ("After Draw loop ")
   
   Tex.Draw("sames")
   Tex2.Draw("sames")
   Tex3.Draw("sames")
   if(drawline):
      line.SetLineStyle(5)
      line.SetLineColor(4)
      line.Draw()
   L[0].Draw()
   L[1].Draw()
   L[2].Draw()
   legend1.Draw()
   
   SaveFile(c, CanvasName)
   return [c,L,legend1]




def DrawTMultiGraph(GrList, LegList, ColorList, title, xAxisTitle, yAxisTitle, xrange1down, xrange1up, yrange1down, yrange1up, yline1low, yline1up, canvasName, latexName='', drawLine=False, logy=False, leftLegend=False, TeVTag=False, latexName2='', doAtlas=False):
    #### these are for MoEDAL Photon fusion theory paper
    #Tex = MakeLatex(0.88,0.65,latexName)
    #Tex2 = MakeLatex(0.88, 0.60, latexName2)
    ### these are for other cases
    Tex = MakeLatex(0.58,0.35,latexName)
    Tex2 = MakeLatex(0.64, 0.30, latexName2)
    ### this is for xsec plots with different kappa
    #Tex = MakeLatex(0.58,0.55,latexName)
    #Tex2 = MakeLatex(0.58, 0.50, latexName2)
    c = TCanvas("c","c",900, 900)
    gStyle.SetOptStat(0)
    c.cd()
    c.SetGrid(0)
    if(logy):
       c.SetLogy()
    c.SetLogx()
    line = MakeLine(xrange1down,yline1low,xrange1up,yline1up)
    
    if(leftLegend):
       legend1 = LeftLegendMaker()
    else:
       #legend1 = LegendMakerTwoColumn()
       legend1 = LegendMaker()
       
    tex1 = TLatex(); tex2 = TLatex(); tex3 = TLatex()
    L = [tex1, tex2, tex3]
    TexMaker(L, doAtlas)
    
    mg = TMultiGraph()
    mg = TMultiGraph('mg',title)
    for i in range(0, len(GrList)):
       GrList[i].GetYaxis().SetTitle('#font[52]{'+yAxisTitle+'}')
       GrList[i].GetXaxis().SetTitle('#font[52]{'+xAxisTitle+'}')
       #GrList[i].GetXaxis().SetNdivisions(5)
       GrList[i].SetTitle("")
       GrList[i] = SetHistColorEtc(GrList[i], ColorList[i])
       #if((len(GrList) > 3) and (i%2==0)):
           #GrList[i].SetLineStyle(2)
           #if(i==0):GrList[i].SetMarkerStyle(kOpenSquare)
           #if(i==2):GrList[i].SetMarkerStyle(kOpenTriangleDown)
           #if(i==4):GrList[i].SetMarkerStyle(kOpenTriangleUp)
       #else:
           #GrList[i].SetLineStyle(1)
       GrList[i].SetMarkerSize(1.5)
       mg.Add(GrList[i])
       legend1.AddEntry(GrList[i],LegList[i],'lp')
    gPad.SetTickx()
    gPad.SetTicky()
    mg.Draw('ALP')
    #mg.GetXaxis().SetTitle('#font[52]{'+xAxisTitle+'}')
    #mg.GetYaxis().SetTitle('#font[52]{'+yAxisTitle+'}')
    mg.GetXaxis().SetTitle(xAxisTitle)
    mg.GetYaxis().SetTitle(yAxisTitle)
    mg.GetXaxis().SetRangeUser(xrange1down, xrange1up)
    mg.GetYaxis().SetRangeUser(yrange1down, yrange1up)
    mg.GetYaxis().SetTitleOffset(1.25)
    mg.GetYaxis().SetLabelSize(0.031)
    mg.GetYaxis().SetTitleSize(0.036)
    mg.GetXaxis().SetTitleSize(0.04)
    mg.GetXaxis().SetLabelSize(0.037)
    #mg.GetYaxis().SetNdivisions(601)
    LUXELabel(0.2,0.85,"TDR")
    Tex.Draw('sames')
    Tex2.Draw('sames')
    legend1.Draw('sames')
    if(drawLine):
       line.Draw()
    L[2].Draw()
    L[1].Draw()
    if(TeVTag):
       #TexTeV = TLatex(0.82,0.915,"#sqrt{s}=13 TeV")#36.075 fb^{-1} (13 TeV)
       TexTeV = TLatex(0.36,0.80,'#sqrt{s}=13 TeV')
       TexTeV.SetNDC()
       TexTeV.SetTextAlign(31)
       TexTeV.SetTextFont(42)
       TexTeV.SetTextSize(0.037)
       TexTeV.SetLineWidth(2) 
       TexTeV.Draw()
    else:
       L[0].Draw()

    SaveFile(c, canvasName)




def main():
    gROOT.LoadMacro("LuxeStyle.C")
    gROOT.LoadMacro("LuxeLabels.C")
    gROOT.SetBatch()
    SetLuxeStyle()
    
    directory = "linearityPlots"
    
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    linearX               = [2.0,
    5.5,
    8.5,
    16.5,
    32.5,
    53.3,
    81.8,
    101.3,
    132.5,
    150.5,
    168.3,
    183.5,
    199.0,
    221.8,
    244.0,
    287.0,
    487.0,
    709.0,
    994.0,
    1457.0,
    1956.0,
    2496.0,
    3013.0,
    3835.0]
    
    linearY               = [2.5,
    5.8,
    8.8,
    16.3,
    32.5,
    53.5,
    83.5,
    104.3,
    132.8,
    148.3,
    166.8,
    181.3,
    202.8,
    229.0,
    264.0,
    327.0,
    495.0,
    744.0,
    1206.0,
    1679.0,
    2411.0,
    3098.0,
    3417.0,
    5042.0]
    
    linearYSigLoose       = [0,
    -5,
    -3,
    -2,
    4,
    -1,
    0,
    2,
    4,
    2,
    -2,
    -2,
    1,
    3,
    -9,
    -1,
    0,
    5,
    11,
    5,
    13,
    28,
    26,
    25]
        
    linearYSigTight       = [0.0,
    -4.5,
    -2.9,
    -1.5,
    3.1,
    -1.9,
    0.3,
    1.0,
    3.2,
    1.2,
    -2.2,
    -2.0,
    0.5,
    1.8,
    -10.2,
    -2.1,
    -1.4,
    2.7,
    8.7,
    4.0,
    11.3,
    25.1,
    24.7,
    21.6]
        
    linearYSigBkgLoose    = [25,
    5,
    3,
    -2,
    0,
    0,
    2,
    3,
    0,
    -1,
    -1,
    -1,
    2,
    3,
    8,
    14,
    2,
    5,
    21,
    15,
    23,
    24,
    13,
    31]
        
    linearYSigBkgTight    = [0.0,
    -4.5,
    -2.9,
    -4.5,
    0.0,
    0.0,
    1.8,
    1.5,
    -0.2,
    -2.3,
    -1.5,
    -1.9,
    1.4,
    2.3,
    -7.8,
    3.5,
    -3.1,
    2.0,
    16.1,
    10.3,
    17.8,
    20.9,
    9.6,
    26.3]
        
    
    
    x            = array.array('d',linearX)
    y            = array.array('d',linearY)
    ySigLoose    = array.array('d',linearYSigLoose)
    ySigTight    = array.array('d',linearYSigTight)
    ySigBkgLoose = array.array('d',linearYSigBkgLoose)
    ySigBkgTight = array.array('d',linearYSigBkgTight)
    
    n = len(x)
    
    graphSigLoose    = TGraph(n,x,ySigLoose)
    graphSigTight    = TGraph(n,x,ySigTight)
    graphSigBkgLoose = TGraph(n,x,ySigBkgLoose)
    graphSigBkgTight = TGraph(n,x,ySigBkgTight)
    graphLinear      = TGraph(n,x,y)
    
    
    
    
    
    
    #### plotting the signal and background
    drawline    = True
    logy        = False
    latexName   = ''
    latexName2  = 'Layer 1'
    latexName3  = ''
    leftLegend  = True
    doAtlas     = False
    doLumi      = False
    noRatio     = False
    do80        = False
    do59        = False
    
    
    FirstTH1 = [graphSigLoose, graphSigTight, graphSigBkgLoose, graphSigBkgTight]
    #FirstTH1 = [graphSigBkgTight]
    
    PlotColor  = [2, 4, kGreen+3, kGray]
    
    #### plotting the layer 0, first layer
    LegendName = ["Sig (loose+tight)", "Sig (tight)", "Sig+Bkg (loose+tight)", "Sig+Bkg (tight)"]
    
    #DrawHistsOneCanvas(FirstTH1, LegendName, PlotColor,"True signal track multiplicity", "Relative difference", 0.0, 4000.0, -5, 5, directory+"/relativeDifference", 1, 1, drawline, logy, 'Relative difference')
    
    
    DrawTMultiGraph(FirstTH1, LegendName, PlotColor, '', "True signal track multiplicity", "Relative difference (%)", 0.0, 4000.0, -10, 40, 1, 1, directory+"/relativeDifferenceMultigraph")
    
    FirstTH1   = [graphLinear]
    LegendName = ["Sig+Bkg (loose+tight)"]
    PlotColor  = [kBlack]
    DrawHistsOneCanvas(FirstTH1, LegendName, PlotColor,"True signal track multiplicity", "Reconstructed track multiplicity", 1, 5400.0, 1, 5400.0, directory+"/linearity", 1, 1, drawline, True, '')
    
    
    
    
if __name__=="__main__":
    start = time.time()
    main()
    print ("The total time taken: ", time.time() - start, " s")
