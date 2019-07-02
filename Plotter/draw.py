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

    sf = float(options.factor)
    
    ROOT.gROOT.SetBatch()

    pstyle = style.SetPlotStyle(1)

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
            
            if not fHist.GetListOfKeys().Contains('h_'+v+'__'+p):
                print 'Histogram '+'h_'+v+'__'+p+' does not exist'
                exit()

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
            
            if sf > 0: h[l].Scale(sf)
        
        for l in ['TtHut','TtHct']:
            h[l].SetMarkerSize(0)
            h[l].SetMarkerColor(ROOT.kOrange+10)
            h[l].SetLineColor(ROOT.kOrange+10)
            h[l].SetFillStyle(0)
            h[l].SetLineStyle(1)
            
            if sf > 0: h[l].Scale(sf)
        
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

        h['Higgs'].SetMarkerSize(0)
        h['Higgs'].SetMarkerColor(ROOT.kYellow)
        h['Higgs'].SetLineColor(ROOT.kYellow)
        h['Higgs'].SetFillColor(ROOT.kYellow)
        h['Higgs'].SetLineStyle(1)

        h['VJets'].SetMarkerSize(0)
        h['VJets'].SetMarkerColor(ROOT.kYellow+3)
        h['VJets'].SetLineColor(ROOT.kYellow+3)
        h['VJets'].SetFillColor(ROOT.kYellow+3)
        h['VJets'].SetLineStyle(1)

        h['QCD'].SetMarkerSize(0)
        h['QCD'].SetMarkerColor(ROOT.kGreen-3)
        h['QCD'].SetLineColor(ROOT.kGreen-3)
        h['QCD'].SetFillColor(ROOT.kGreen-3)
        h['QCD'].SetLineStyle(1)
        
        h['TT'].SetMarkerSize(0)
        h['TT'].SetMarkerColor(ROOT.kGray)
        h['TT'].SetLineColor(ROOT.kGray)
        h['TT'].SetFillColor(ROOT.kGray)
        h['TT'].SetLineStyle(1)

        h['GJet'].SetMarkerSize(0)
        h['GJet'].SetMarkerColor(ROOT.kBlue-3)
        h['GJet'].SetLineColor(ROOT.kBlue-3)
        h['GJet'].SetFillColor(ROOT.kBlue-3)
        h['GJet'].SetLineStyle(1)
        
        hSM = ROOT.THStack()
        maxSM = 0
        for p in c.processSort:
            if p == 'data': continue
            if p not in ['StHut','StHct','TtHut','TtHct']:
                hSM.Add(h[p])
                maxSM = maxSM + h[p].GetMaximum()

        if sf < 0:
            
            h['StHut'].Scale(maxSM/(h['StHut'].GetMaximum()+h['TtHut'].GetMaximum()))
            h['TtHut'].Scale(maxSM/(h['StHut'].GetMaximum()+h['TtHut'].GetMaximum()))
            h['StHct'].Scale(maxSM/(h['StHct'].GetMaximum()+h['TtHct'].GetMaximum()))
            h['TtHct'].Scale(maxSM/(h['StHct'].GetMaximum()+h['TtHct'].GetMaximum()))
                
        hNP = ROOT.THStack()
        maxNP = 0
        for p in c.processSort:
            if p == 'data': continue
            elif p in ['StHut','TtHut']:
                hNP.Add(h[p])
                maxNP = maxNP + h[p].GetMaximum()
                
        hSM.Draw('hist')
        
        hSM.GetXaxis().SetTitle(h['data'].GetXaxis().GetTitle())
        hSM.GetYaxis().SetTitle(h['data'].GetYaxis().GetTitle())
    
        maxData = h['data'].GetMaximum()
        hSM.SetMaximum(1.2*max(maxData,maxSM,maxNP))
        hSM.SetMinimum(0.)

        hBG = []
        hBGUp = []
        hBGDown = []
        hComb = h['DiPhotonJets'].Clone("hComb")
        for p in c.processSort:
            if p not in ['StHut','StHct','TtHut','TtHct','data']:
                if p not in ['DiPhotonJets']:
                    hComb.Add(h[p])
                hBG.append(h[p])
                hBGUp.append(hSysUp[p])
                hBGDown.append(hSysDown[p])

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
        
#        hComb.SetLineColor(1)
#        hComb.SetLineStyle(2)
#        hComb.SetFillColor(0)
#        hComb.Draw("hist same")
        
        grMCMerged = func.makeErrorBand(hComb,hSysUpCombSum,hSysDownCombSum)

        grMCMerged.SetFillStyle(3354)
        grMCMerged.SetFillColor(ROOT.kGray+1)
        grMCMerged.Draw("2SAME")

        hNP.Draw('hist noclear same')
        h['data'].Draw('e1 same')    
        
        leg = ROOT.TLegend(0.82,0.92,0.990,0.40)
        leg.SetFillColor(253)
        leg.SetBorderSize(0)
        for p in c.processSort:
            if p == 'data': leg.AddEntry(h[p],"Data","p")
            elif p == 'StHut': leg.AddEntry(h[p],"ST Hut","l")
#            elif p == 'StHct': leg.AddEntry(h[p],"StHct","l")
            elif p == 'TtHut': leg.AddEntry(h[p],"TT Hut","l")
#            elif p == 'TtHct': leg.AddEntry(h[p],"TtHct","l")
            elif p == 'DiPhotonJets': leg.AddEntry(h[p],"#gamma#gamma+jets","f")
            elif p == 'QCD': leg.AddEntry(h[p],"QCD","f")
            elif p == 'TTGJets': leg.AddEntry(h[p],"t#bar{t}#gamma(#gamma)+jets","f")
            elif p == 'TGJets': leg.AddEntry(h[p],"t/#bar{t}#gamma+jets","f")
            elif p == 'VJets': leg.AddEntry(h[p],"V(#gamma)+jets","f")
            elif p == 'Higgs': leg.AddEntry(h[p],"Higgs","f")
            elif p == 'TT': leg.AddEntry(h[p],"t#bar{t}","f")
            elif p == 'GJet': leg.AddEntry(h[p],"#gamma+jets","f")
        leg.Draw()
        
        t1, t2, t3 = style.cmslabel(1)
        t1.Draw()
        t3.Draw()
        t = style.channel(chan)
        t.Draw()
        
        c1.Print(options.output+'/'+v+'.eps')
