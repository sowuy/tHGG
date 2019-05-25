import os
import sys
import subprocess
import common as c
from subprocess import call
import style
import functions as func
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Analysis script to draw histograms"
    
    parser = OptionParser(usage)
    parser.add_option("-i","--input",default="output.root",help="input file name [default: %default]")
    parser.add_option("-n","--names",default="lepPt",help="list of histogram names [default: %default]")
    parser.add_option("-c","--channel",default="leptonic",help="analysis channel [default: %default]")
    parser.add_option("-o","--output",default="pics",help="output directory [default: %default]")
    parser.add_option("-s","--sys",default="",help="systematics list [default: %default]")
    parser.add_option("-f","--factor",default="1",help="signal scale factor [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

if __name__ == '__main__':
    
    options = main()
                
    ROOT.gROOT.SetBatch()

    style.SetPlotStyle()

    var = options.names.split(',')
    chan = options.channel
    sys = options.sys.split(',')
    nSys = len(sys)

    if os.path.isdir(options.output):
        os.system("rm -rf "+options.output)                
    os.system("mkdir "+options.output)

    fHist = ROOT.TFile.Open(options.input,'read')
    
    for v in var:
        
        c1 = ROOT.TCanvas()

        h = {}
        hSysUp = {}
        hSysDown = {}
        for p in c.processSort:
            h[p] = fHist.Get('h_'+v+'__'+p)

            for isys in range(nSys):
                hSysUp[p] = []
                hSysDown[p] = []                
                hSysUp[p].append(fHist.Get('h_'+v+'__'+p))
                hSysDown[p].append(fHist.Get('h_'+v+'__'+p))
            
                func.addbin(hSysUp[p][isys])
                func.addbin(hSysDown[p][isys]);

        h['data'].SetMarkerSize(0.7)
        h['data'].SetMarkerColor(1)
        h['data'].SetLineColor(1)

        for l in ['StHut','StHct']:
            h[l].SetMarkerSize(0)
            h[l].SetMarkerColor(ROOT.kOrange+2)
            h[l].SetLineColor(ROOT.kOrange+2)
            h[l].SetFillStyle(0)
            h[l].SetLineStyle(1)
            
            h[l].Scale(float(options.factor))
        
        for l in ['TtHut','TtHct']:
            h[l].SetMarkerSize(0)
            h[l].SetMarkerColor(ROOT.kOrange+10)
            h[l].SetLineColor(ROOT.kOrange+10)
            h[l].SetFillStyle(0)
            h[l].SetLineStyle(1)
            
            h[l].Scale(float(options.factor))
        
        h['DiPhotonJets'].SetMarkerSize(0)
        h['DiPhotonJets'].SetMarkerColor(ROOT.kAzure-7)
        h['DiPhotonJets'].SetLineColor(ROOT.kAzure-7)
        h['DiPhotonJets'].SetFillColor(ROOT.kAzure-7)
        h['DiPhotonJets'].SetLineStyle(1)

        h['TTGJets'].SetMarkerSize(0)
        h['TTGJets'].SetMarkerColor(ROOT.kMagenta-9)
        h['TTGJets'].SetLineColor(ROOT.kMagenta-9)
        h['TTGJets'].SetFillColor(ROOT.kMagenta-9)
        h['TTGJets'].SetLineStyle(1)

        h['TGJets'].SetMarkerSize(0)
        h['TGJets'].SetMarkerColor(ROOT.kMagenta-3)
        h['TGJets'].SetLineColor(ROOT.kMagenta-3)
        h['TGJets'].SetFillColor(ROOT.kMagenta-3)
        h['TGJets'].SetLineStyle(1)
        
#        h['QCD'].SetMarkerSize(0)
#        h['QCD'].SetMarkerColor(ROOT.kGreen)
#        h['QCD'].SetLineColor(ROOT.kGreen)
#        h['QCD'].SetFillColor(ROOT.kGreen)
#        h['QCD'].SetLineStyle(1)

        h['GJet'].SetMarkerSize(0)
        h['GJet'].SetMarkerColor(ROOT.kBlue-3)
        h['GJet'].SetLineColor(ROOT.kBlue-3)
        h['GJet'].SetFillColor(ROOT.kBlue-3)
        h['GJet'].SetLineStyle(1)
        
        hSM = ROOT.THStack()
        hNP = ROOT.THStack()
        for p in c.processSort:
            if p == 'data': continue
            if p not in ['StHut','StHct','TtHut','TtHct']:
                hSM.Add(h[p])
            elif p in ['StHut','TtHut']:
                hNP.Add(h[p])
        
        hSM.Draw('hist')
        hNP.Draw('hist noclear same')
        h['data'].Draw('e1 same')    
        
        hSM.GetXaxis().SetTitle(h['data'].GetXaxis().GetTitle())
        hSM.GetYaxis().SetTitle(h['data'].GetYaxis().GetTitle())
    
        maxData = h['data'].GetMaximum()
        maxSM = hSM.GetMaximum()
        maxNP = hNP.GetMaximum()
        hSM.SetMaximum(1.2*max(maxData,maxSM,maxNP))
        hSM.SetMinimum(0.)

        hBG = []
        hBGUp = []
        hBGDown = []
        for p in c.processSort:
            if p not in ['StHut','StHct','TtHut','TtHct','data']:
                hBG.append(h[p])
                hBGUp.append(hSysUp[p])
                hBGDown.append(hSysDown[p])

        hComb = h['DiPhotonJets'].Clone("hComb")
        hSysUpCombSum = hComb.Clone("hSysUpCombSum")
        hSysDownCombSum = hComb.Clone("hSysDownCombSum")
        hSysUpComb = []
        hSysDownComb = []
        
        for isys in range(nSys):
            
            hSysUpComb.append(hComb)
            hSysDownComb.append(hComb)

        for isys in range(nSys):

            func.combSysLinear(hBG,hBGUp,hBGDown,hComb,hSysDownComb,hSysUpComb,isys)
            func.totSys(hComb,hSysDownComb[isys],hSysUpComb[isys]);
	
	func.combSys(hComb,hSysDownComb,hSysUpComb,hSysDownCombSum,hSysUpCombSum,nSys);
	func.totSys(hComb,hSysDownCombSum,hSysUpCombSum);
        
##        hComb.SetLineColor(1)
##        hComb.SetLineStyle(2)
##        hComb.SetFillColor(0)
##        hComb.Draw("hist same")
        
        grMCMerged = func.makeErrorBand(hComb,hSysUpCombSum,hSysDownCombSum)
 
        ROOT.gStyle.SetHatchesLineWidth(5);
        grMCMerged.SetFillStyle(3005)
        grMCMerged.SetFillColor(ROOT.kBlack)
        grMCMerged.Draw("2SAME")
        
        leg = ROOT.TLegend(0.82,0.92,0.995,0.40)
        leg.SetFillColor(253)
        leg.SetBorderSize(0)
        for p in c.processSort:
            if p == 'data': leg.AddEntry(h[p],"Data","lp")
            elif p == 'StHut': leg.AddEntry(h[p],"ST Hut","l")
#            elif p == 'StHct': leg.AddEntry(h[p],"StHct","l")
            elif p == 'TtHut': leg.AddEntry(h[p],"TT Hut","l")
#            elif p == 'TtHct': leg.AddEntry(h[p],"TtHct","l")
            elif p == 'DiPhotonJets': leg.AddEntry(h[p],"#gamma#gamma+jets","f")
            elif p == 'TTGJets': leg.AddEntry(h[p],"t#bar{t}(#gamma)+jets","f")
            elif p == 'TGJets': leg.AddEntry(h[p],"t/#bar{t}#gamma+jets","f")
            elif p == 'QCD': leg.AddEntry(h[p],"QCD","f")
            elif p == 'GJet': leg.AddEntry(h[p],"#gamma+jets","f")
        leg.Draw()
    
        t = style.CMSLABEL()
        
        c1.Print('pics/'+v+'.eps')
