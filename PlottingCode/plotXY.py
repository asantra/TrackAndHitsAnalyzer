from ROOT import *
import array, os
def MakeLine(xlow, ylow, xup, yup):
  line = TLine(xlow,ylow,xup,yup)
  line.SetLineStyle(1)
  line.SetLineWidth(2)
  return line

def main():
    
    directory = "xyPlotSeedLinearity"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    y = array.array('d', [2.5,
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
    229,
    264,
    327,
    495,
    744,
    1206,
    1679,
    2411,
    3098,
    3417,
    5042])
    
    

    x = array.array('d',[2,
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
    199,
    221.8,
    244,
    287,
    487,
    709,
    994,
    1457,
    1956,
    2496,
    3013,
    3835])
    
    xe = array.array('d',len(x)*[0])
    #print(xe)

    n = len(y)
    g = TGraph(n,x,y)
    g2 = TGraph(n,x,y)
    g.GetXaxis().SetTitle("number of charged particles")
    g.GetXaxis().SetRangeUser(0,5500)
    g.GetYaxis().SetRangeUser(0,5500)
    g.GetYaxis().SetTitle("number of selected tracks")
    g.SetMarkerStyle(kFullTriangleUp)
    g.SetMarkerSize(1)
    g.SetTitle("")
    
    xaxis = g.GetXaxis();

    xaxis.SetLimits(0.,5500.0);           #      // along X
    g.GetHistogram().SetMaximum(5500);   #// along          
    g.GetHistogram().SetMinimum(0);  #//   Y 
    g.GetYaxis().SetTitleOffset(1.45)
    g.GetYaxis().SetTitleSize(0.03)
    g.GetYaxis().SetLabelSize(0.025)


    
    line = MakeLine(0, 0, 5500, 5500)
    line.SetLineStyle(2)
    line.SetLineWidth(1)
    line.SetLineColor(4)

    #g=TGraph(n,x,y)###

    c1 = TCanvas("c1","c1",700,700)
    g.Draw("AP");
    c1.SetTickx()
    c1.SetTicky()
    line.Draw()
    c1.SaveAs(directory+"/xyPlot.pdf")
    c1.SaveAs(directory+"/xyPlot.png")
    
    c2 = TCanvas("c2","c2",700,700)
    
    
    g2.GetXaxis().SetTitle("number of charged particles")
    g2.GetXaxis().SetRangeUser(0,10000)
    g2.GetYaxis().SetRangeUser(0,10000)
    g2.GetYaxis().SetTitle("number of selected tracks")
    g2.SetMarkerStyle(kFullTriangleUp)
    g2.SetMarkerSize(1)
    g2.SetTitle("")
    
    xaxis2 = g2.GetXaxis();

    xaxis2.SetLimits(1.,10000.0);           #      // along X
    g2.GetHistogram().SetMaximum(10000);   #// along          
    g2.GetHistogram().SetMinimum(1);
    
    g2.Draw("AP");
    c2.SetLogx()
    c2.SetLogy()
    c2.SetTickx()
    c2.SetTicky()
    
    
    line2 = MakeLine(0, 0, 10000, 10000)
    line2.SetLineStyle(2)
    line2.SetLineWidth(1)
    line2.SetLineColor(4)
    
    line2.Draw()
    c2.SaveAs(directory+"/xyPlotLog.pdf")
    c2.SaveAs(directory+"/xyPlotLog.png")
    
    
if __name__=="__main__":
    main()
