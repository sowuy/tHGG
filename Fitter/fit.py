import os
import sys
import subprocess
from subprocess import call
import math
import ROOT

sys.path.insert(0,'../Plotter/')
import style

ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Analysis script to create histograms"
    
    parser = OptionParser(usage)
    parser.add_option("-i","--input",default="../Plotter/output.root",help="input file name [default: %default]")
    parser.add_option("-o","--output",default="model.root",help="output file name [default: %default]")
    parser.add_option("-p","--pics",default="pics",help="output directory with pictures [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

def createModel():
    
    fInput = ROOT.TFile.Open(options.input,'OPEN')
    
    tr = {}
    trname = ['data_obs','sig']
    for n in trname:
        tr[n] = fInput.Get(n)
    
    w = ROOT.RooWorkspace('model')
    
    DiPhoMassFit = ROOT.RooRealVar('DiPhoMassFit','DiPhoMassFit',100.,180.)
    WeightFit = ROOT.RooRealVar('WeightFit','WeightFit',-10000.,10000.)
    
    sig = ROOT.RooDataSet('sig','sig',ROOT.RooArgSet(DiPhoMassFit),ROOT.RooFit.Import(tr['sig']),ROOT.RooFit.WeightVar(WeightFit))
    data_obs = ROOT.RooDataSet('data_obs','data_obs',ROOT.RooArgSet(DiPhoMassFit),ROOT.RooFit.Import(tr['data_obs']));

#    w.factory('Gaussian::sig(x[-5,5],mu[-3,3],sigma[1])')
#    w.factory('Exponential::bkg(x,tau[-.5,-3,0])')

    getattr(w,'import')(DiPhoMassFit)
    
    getattr(w,'import')(sig)
    getattr(w,'import')(data_obs)
    
    w.writeToFile(options.output,True)
    w.Print()
    
    fInput.Close()
    
if __name__ == '__main__':
    
    options = main()
                
    ROOT.gROOT.SetBatch()
    
    pstyle = style.SetPlotStyle()

    if os.path.isdir(options.pics):
        os.system("rm -rf "+options.pics)
    os.system("mkdir "+options.pics)
    
    createModel()

    modelFile = ROOT.TFile.Open(options.output,'READ')
    w = modelFile.Get('model');
 
    DiPhoMassFit = w.var('DiPhoMassFit')
    
    sig = w.data("sig")
    data_obs = w.data("data_obs")

    a0 = ROOT.RooRealVar('a0','a0',0.1,0.0,1.0)
    a1 = ROOT.RooRealVar('a1','a1',0.1,0.0,1.0)
    a2 = ROOT.RooRealVar('a2','a2',0.1,0.0,1.0)
    a3 = ROOT.RooRealVar('a3','a3',0.1,0.0,1.0)
    a4 = ROOT.RooRealVar('a4','a4',0.1,0.0,1.0)

    dataBernPdf = ROOT.RooBernstein('dataBernPdf','dataBernPdf',DiPhoMassFit,ROOT.RooArgList(a0,a1,a2,a3,a4))
    
    res = dataBernPdf.fitTo(data_obs,ROOT.RooFit.Minimizer("Minuit2","minimize"),ROOT.RooFit.Save(True),ROOT.RooFit.Verbose(False),ROOT.RooFit.SumW2Error(True))
    
    print res.minNll(), res.status(), '0=OK'
    
    dataBernPlot = DiPhoMassFit.frame(ROOT.RooFit.Title("Fit"),ROOT.RooFit.Bins(16))
    data_obs.plotOn(dataBernPlot,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    dataBernPdf.plotOn(dataBernPlot)
    
    c1 = ROOT.TCanvas("c1","c1",650,600)
    dataBernPlot.Draw()

    c1.Print('pics/fit.eps')


    
    

