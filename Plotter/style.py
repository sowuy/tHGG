import ROOT

def SetPlotStyle():

    plotStyle = PlotStyle();
    ROOT.gROOT.SetStyle("PLOT")
    ROOT.gROOT.ForceStyle()

def PlotStyle():

    plotStyle = ROOT.TStyle("PLOT","Plot style")

    icol = 0
    plotStyle.SetFrameBorderMode(icol)
    plotStyle.SetFrameFillColor(icol)
    plotStyle.SetCanvasBorderMode(icol)
    plotStyle.SetCanvasColor(icol)
    plotStyle.SetPadBorderMode(icol)
    plotStyle.SetPadColor(icol)
    plotStyle.SetStatColor(icol)

    plotStyle.SetPaperSize(20,26)

    plotStyle.SetPadTopMargin(0.07)
    plotStyle.SetPadRightMargin(0.2)
    plotStyle.SetPadBottomMargin(0.16)
    plotStyle.SetPadLeftMargin(0.16)
    
    plotStyle.SetTitleXOffset(1.4)
    plotStyle.SetTitleYOffset(1.4)

    font = 42
    tsize = 0.05
    plotStyle.SetTextFont(font)

    plotStyle.SetTextSize(tsize)
    plotStyle.SetLabelFont(font,"x")
    plotStyle.SetTitleFont(font,"x")
    plotStyle.SetLabelFont(font,"y")
    plotStyle.SetTitleFont(font,"y")
    plotStyle.SetLabelFont(font,"z")
    plotStyle.SetTitleFont(font,"z")
  
    plotStyle.SetLabelSize(tsize,"x")
    plotStyle.SetTitleSize(tsize,"x")
    plotStyle.SetLabelSize(tsize,"y")
    plotStyle.SetTitleSize(tsize,"y")
    plotStyle.SetLabelSize(tsize,"z")
    plotStyle.SetTitleSize(tsize,"z")

    plotStyle.SetMarkerStyle(20)
    plotStyle.SetMarkerSize(1.2)
    plotStyle.SetHistLineWidth(2)
    plotStyle.SetLineStyleString(2,"[12 12]")

    plotStyle.SetEndErrorSize(0.)

    plotStyle.SetOptTitle(0)
    plotStyle.SetOptStat(0)
    plotStyle.SetOptFit(0)

    plotStyle.SetPadTickX(1)
    plotStyle.SetPadTickY(1)

    return plotStyle

def CMSLABEL():
    
    tex = ROOT.TLatex(0.1969,0.906825,"CMS")
    tex.SetNDC()
    tex.SetTextAlign(13)
    tex.SetTextFont(61)
    tex.SetTextSize(0.07475)
    tex.SetLineWidth(2)
    tex.Draw()
   
    tex2 = ROOT.TLatex(0.1969,0.817125,"Preliminary")
    tex2.SetNDC()
    tex2.SetTextAlign(13)
    tex2.SetTextFont(52)
    tex2.SetTextSize(0.05681)
    tex2.SetLineWidth(2)
    tex2.Draw()
    
    text1 = ROOT.TLatex(0.80,0.94,"41.5 fb^{-1}, #sqrt{s} = 13 TeV")
    text1.SetNDC()
    text1.SetTextAlign(31)
    text1.SetTextFont(42)
    text1.SetTextSize(0.04875)
    text1.SetLineWidth(2)
    text1.Draw()

    return tex, tex2, text1

def LABEL(lab):

   tex = ROOT.TLatex(0.65,0.906825,lab)
   tex.SetNDC()
   tex.SetTextAlign(13)
   tex.SetTextFont(61)
   tex.SetTextSize(0.07475)
   tex.SetLineWidth(2)
   tex.Draw()

