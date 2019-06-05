import os
import sys
import subprocess
from subprocess import call
import collections
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
    parser.add_option("-c","--channel",default="leptonic",help="channel name [default: %default]")
    
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
#    w.Print()
    
    fInput.Close()

def makePdf(var, func, ord, par):
    
    if func == 'Bernstein':
        
        plist = ROOT.RooArgList()
        for i in range(ord):
            par.append(ROOT.RooRealVar('p'+str(i),'p'+str(i),1.,0.0,10.0))
            plist.add(par[i])

        dataPdf = ROOT.RooBernstein(func+str(ord),func+str(ord),var,plist)

    else:
        
        print 'Fit function', func, 'is not defined'
        exit()
    
    return dataPdf
    
if __name__ == '__main__':
    
    options = main()
                
    ROOT.gROOT.SetBatch()
    
    chan = options.channel
    
    pstyle = style.SetPlotStyle(2)

    if os.path.isdir(options.pics):
        os.system("rm -rf "+options.pics)
    os.system("mkdir "+options.pics)
    
    createModel()

    modelFile = ROOT.TFile.Open(options.output,'READ')
    w = modelFile.Get('model');
 
    DiPhoMassFit = w.var('DiPhoMassFit')
    
    sig = w.data("sig")
    data_obs = w.data("data_obs")

    dataPdf = {}
    dataPdfPar = {}
    
    ordMinBernstein = 1
    ordMaxBernstein = 10
    for ord in range(ordMinBernstein,ordMaxBernstein):
        dataPdfName = 'Bernstein'+str(ord)
        dataPdfPar[dataPdfName] = []
        dataPdf[dataPdfName] = [makePdf(DiPhoMassFit,'Bernstein',ord,dataPdfPar[dataPdfName]),ord]

    dataPdf = collections.OrderedDict(sorted(dataPdf.items(), key=lambda k: k[0]))
    dataPdfPar = collections.OrderedDict(sorted(dataPdfPar.items(), key=lambda k: k[0]))
        
    llh0 = 10E+10
    pval = 0.05
    ord0 = ordMinBernstein-1
    bestBernstein = ''
    for name, pdf in dataPdf.items():
        res = dataPdf[name][0].fitTo(data_obs,ROOT.RooFit.Minimizer("Minuit2","minimize"),ROOT.RooFit.Minos(ROOT.kFALSE),ROOT.RooFit.Hesse(ROOT.kTRUE),\
        ROOT.RooFit.Verbose(ROOT.kFALSE),ROOT.RooFit.Warnings(ROOT.kTRUE),ROOT.RooFit.PrintLevel(-1000),ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(True))
        llh = res.minNll()
        chi2 = 2.*(llh0 - llh)
        ord = dataPdf[name][1]
        delta_dof = ord - ord0
        prob = ROOT.TMath.Prob(chi2,delta_dof)
        if prob > pval:
            bestBernstein = name
            break
        ord0 = ord
        llh0 = llh

    dataPdfBernstein = dataPdf[bestBernstein]
        
    dataPlot = DiPhoMassFit.frame(ROOT.RooFit.Title("Fit"),ROOT.RooFit.Bins(16))
    
    dataPdf = [dataPdfBernstein]
    
    for pdf in dataPdf:
        
        data_obs.plotOn(dataPlot,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.Name('data_obs'),ROOT.RooFit.XErrorSize(0))
        pdf[0].plotOn(dataPlot,ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name(pdf[0].GetName()))
        dataPlot.GetXaxis().SetTitle('Diphoton invariant mass [GeV]')
    
    c1 = ROOT.TCanvas("c1","c1",650,500)

    dataPlot.Draw()
    
    t1, t2, t3 = style.cmslabel(2)
    t1.Draw()
    t3.Draw()
    t = style.channel(chan)
    t.Draw()
    
    leg = ROOT.TLegend(0.65,0.65,0.88,0.83)
    leg.SetFillColor(253)
    leg.SetBorderSize(0)
    leg.AddEntry(dataPlot.findObject('data_obs'),'Data','p')
    leg.AddEntry(dataPlot.findObject(bestBernstein),'Bernstein('+str(dataPdfBernstein[1])+')','l')
    leg.Draw()

    c1.Print('pics/fit.eps')


    
    

