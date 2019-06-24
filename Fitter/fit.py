import os
import sys
import subprocess
from subprocess import call
from array import array
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
    parser.add_option("-f","--fit",default="bkg",help="fit mode [default: %default]")
    parser.add_option("-n","--nmax",default=-1,help="maximum number of entries to be used for signal model [default: %default]")
    
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
    EventId = ROOT.RooRealVar('EventId','EventId',0.,10E+10)
    
    sig = ROOT.RooDataSet('sig','sig',ROOT.RooArgSet(DiPhoMassFit,EventId),ROOT.RooFit.Import(tr['sig']),ROOT.RooFit.WeightVar(WeightFit))
#    sig = ROOT.RooDataSet('sig','sig',ROOT.RooArgSet(DiPhoMassFit),ROOT.RooFit.Import(tr['sig']),ROOT.RooFit.WeightVar(WeightFit))
    data_obs = ROOT.RooDataSet('data_obs','data_obs',ROOT.RooArgSet(DiPhoMassFit),ROOT.RooFit.Import(tr['data_obs']));

#    w.factory('Gaussian::sig(x[-5,5],mu[-3,3],sigma[1])')
#    w.factory('Exponential::bkg(x,tau[-.5,-3,0])')

    getattr(w,'import')(DiPhoMassFit)
    
    getattr(w,'import')(sig)
    getattr(w,'import')(data_obs)
    
    w.writeToFile(options.output,True)
#    w.Print()
    
    fInput.Close()

def makePdf(var, func, ord, par, gaus=None, dm=None, mean=None, sigma=None, mH=None):

    pdf = 0
    
    if func == 'Bernstein':
        
        plist = ROOT.RooArgList()
        for i in range(ord):
            par.append(ROOT.RooRealVar('p'+str(i),'p'+str(i),1.,0.0,10.0))
            plist.add(par[i])

        pdf = ROOT.RooBernstein(func+str(ord),func+str(ord),var,plist)

    elif func == 'Gaus':

        gaussians = ROOT.RooArgList()        
        plist = ROOT.RooArgList()
     
        for i in range(ord+1):
            
            dm.append(ROOT.RooRealVar('Gaus_dm_'+str(i),'Gaus_dm_'+str(i),0.1,-8.,8.))
            mean.append(ROOT.RooFormulaVar('Gaus_mean_'+str(i),'Gaus_mean_'+str(i),"@0+@1",ROOT.RooArgList(mH,dm[i])))
            sigma.append(ROOT.RooRealVar('Gaus_sigma_'+str(i),'Gaus_sigma_'+str(i),2.,0.4,20.))
            gaus.append(ROOT.RooGaussian('Gaus_gaus_'+str(i),'Gaus_gaus_'+str(i),var,mean[i],sigma[i]))
            gaussians.add(gaus[i]);

            if i > 0 and i < ord+1:
                par.append(ROOT.RooRealVar('Gaus_frac_'+str(i),'Gaus_frac_'+str(i),0.1,0.01,0.99))
                plist.add(par[i-1])

        pdf = ROOT.RooAddPdf(func+str(ord),func+str(ord),gaussians,plist,ROOT.kTRUE)
        
    else:
        
        print 'Fit function', func, 'is not defined'
        exit()
    
    return pdf

def bkgModel(var, data_obs):

    dataPdf = {}
    dataPdfPar = {}
    
    ordMinBernstein = 1
    ordMaxBernstein = 10
    for ord in range(ordMinBernstein,ordMaxBernstein):
        dataPdfName = 'Bernstein'+str(ord)
        dataPdfPar[dataPdfName] = []
        dataPdf[dataPdfName] = [makePdf(var,'Bernstein',ord,dataPdfPar[dataPdfName]),ord]

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
        
    dataPlot = var.frame(ROOT.RooFit.Title("Fit"),ROOT.RooFit.Bins(16))
    
    dataPdfFinal = [dataPdfBernstein]
    
    for pdf in dataPdfFinal:
        
        data_obs.plotOn(dataPlot,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.Name('data_obs'),ROOT.RooFit.XErrorSize(0))
        pdf[0].plotOn(dataPlot,ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name(pdf[0].GetName()))
        dataPlot.GetXaxis().SetTitle('Diphoton invariant mass [GeV]')

    bestPdf = dataPdfFinal[0]
        
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

    c1.Print('pics/bkgModel.eps')
    
    return bestPdf[0]

def sigModel(var, sig):

    sigPdf = {}
    sigPdfPar = {}
    sigPdfGaus = {}
    sigPdfDm = {}
    sigPdfMean = {}
    sigPdfSigma = {}
    
    mH = ROOT.RooRealVar("mH","mH",125.,115.,135.)
    mH.setConstant(True)
    
    ordMaxGaus = 4
    for ord in range(ordMaxGaus):
        sigPdfName = 'Gaus'+str(ord)
        sigPdfPar[sigPdfName] = []
        sigPdfGaus[sigPdfName] = []
        sigPdfDm[sigPdfName] = []
        sigPdfMean[sigPdfName] = []
        sigPdfSigma[sigPdfName] = []
        sigPdf[sigPdfName] = [makePdf(var,'Gaus',ord,sigPdfPar[sigPdfName],sigPdfGaus[sigPdfName],\
        sigPdfDm[sigPdfName],sigPdfMean[sigPdfName],sigPdfSigma[sigPdfName],mH),ord]

    sigPdf = collections.OrderedDict(sorted(sigPdf.items(), key=lambda k: k[0]))
    sigPdfPar = collections.OrderedDict(sorted(sigPdfPar.items(), key=lambda k: k[0]))
    sigPdfGaus = collections.OrderedDict(sorted(sigPdfGaus.items(), key=lambda k: k[0]))
    sigPdfDm = collections.OrderedDict(sorted(sigPdfDm.items(), key=lambda k: k[0]))
    sigPdfMean = collections.OrderedDict(sorted(sigPdfMean.items(), key=lambda k: k[0]))
    sigPdfSigma = collections.OrderedDict(sorted(sigPdfSigma.items(), key=lambda k: k[0]))
     
    llh0 = 0
    pval = 0.05
    ord0 = 0
    bestGaus = ''
    for name, pdf in sigPdf.items():        

        print sigPdf[name][0]
        
#        res = sigPdf[name][0].fitTo(sig,ROOT.RooFit.Minimizer("Minuit2","minimize"),\
#        ROOT.RooFit.Minos(ROOT.kFALSE),ROOT.RooFit.Hesse(ROOT.kTRUE),\
#        ROOT.RooFit.Warnings(ROOT.kTRUE),ROOT.RooFit.PrintLevel(-1000),\
#        ROOT.RooFit.SumW2Error(True),\
#        ROOT.RooFit.Save(),\
#        ROOT.RooFit.Range(115.,135.))

        res = sigPdf[name][0].fitTo(sig,ROOT.RooFit.Minimizer("Minuit2","minimize"),\
        ROOT.RooFit.Minos(ROOT.kFALSE),ROOT.RooFit.Hesse(ROOT.kTRUE),\
        ROOT.RooFit.SumW2Error(True),\
        ROOT.RooFit.Save(),\
        ROOT.RooFit.Range(115.,135.))
        
        llh = res.minNll()
        chi2 = 2.*(llh0 - llh)
        ord = sigPdf[name][1]
        delta_dof = (2*(ord+1)+ord)-(2*(ord0+1)+ord0)
        prob = ROOT.TMath.Prob(chi2,delta_dof)
        print prob
        if prob > pval:
            bestGaus = name
            break
        ord0 = ord
        llh0 = llh

    sigPdfGausResult = sigPdf[bestGaus]

    sigPlot = var.frame(ROOT.RooFit.Title("Fit"),ROOT.RooFit.Bins(64),ROOT.RooFit.Range(110,140))
    
    sigPdfFinal = [sigPdfGausResult]

    for pdf in sigPdfFinal:

        sig.plotOn(sigPlot,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.Name('sig'),ROOT.RooFit.XErrorSize(0))
        pdf[0].getVariables().Print("v")
        pdf[0].plotOn(sigPlot,ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name(pdf[0].GetName()))
        sigPlot.GetXaxis().SetTitle('Diphoton invariant mass [GeV]')
        
    bestPdf = sigPdfFinal[0]
        
    c1 = ROOT.TCanvas("c1","c1",650,500)

    sigPlot.Draw()
    
    t1, t2, t3 = style.cmslabel(2)
    t1.Draw()
    t3.Draw()
    t = style.channel(chan)
    t.Draw()
    
    leg = ROOT.TLegend(0.65,0.65,0.88,0.83)
    leg.SetFillColor(253)
    leg.SetBorderSize(0)
    leg.AddEntry(sigPlot.findObject('sig'),'Data','p')
    leg.AddEntry(sigPlot.findObject(bestGaus),'Gaus('+str(sigPdfGausResult[1]+1)+')','l')
    leg.Draw()

    c1.Print('pics/sigModel.eps')

    return bestPdf[0]

def combModel(var, bkg, sig, data_obs):

    c1 = ROOT.TCanvas("c1","c1",650,500)

    fsig = ROOT.RooRealVar("fsig","signal fraction",0.5,0.,1.)
    combPdf = ROOT.RooAddPdf("comb","comb",ROOT.RooArgList(sig,bkg),ROOT.RooArgList(fsig))


#    res = combPdf.fitTo(data_obs,ROOT.RooFit.Minimizer("Minuit2","minimize"),\
#    ROOT.RooFit.Minos(ROOT.kFALSE),ROOT.RooFit.Hesse(ROOT.kTRUE),\
#    ROOT.RooFit.SumW2Error(True),\
#    ROOT.RooFit.Save(),\
#    ROOT.RooFit.Range(115.,135.))
    
    combPlot = var.frame(ROOT.RooFit.Title("Fit"),ROOT.RooFit.Bins(64),ROOT.RooFit.Range(110,140))
#    combPdf.plotOn(combPlot)
    
    combPdf.getVariables().Print("v")
    
    combPdf.plotOn(combPlot,ROOT.RooFit.Components(ROOT.RooArgSet(bkg)),ROOT.RooFit.LineStyle(2))
#    combPdf.plotOn(combPlot,ROOT.RooFit.Components(sig),ROOT.RooFit.LineStyle(2),ROOT.RooFit.LineColor(2))
    
#    combPlot.Draw()
    
    t1, t2, t3 = style.cmslabel(2)
    t1.Draw()
    t3.Draw()
    t = style.channel(chan)
    t.Draw()
    
    leg = ROOT.TLegend(0.65,0.65,0.88,0.83)
    leg.SetFillColor(253)
    leg.SetBorderSize(0)
#    leg.AddEntry(combPlot.findObject('sig'),'Data','p')
#    leg.AddEntry(combPlot.findObject(bestGaus),'Gaus('+str(sigPdfGausResult[1]+1)+')','l')
    leg.Draw()

    c1.Print('pics/combModel.eps')
    
    return combPdf

if __name__ == '__main__':
    
    options = main()
                
    ROOT.gROOT.SetBatch()
    
    chan = options.channel    
        
    dofit = options.fit.split(',')
    
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

    if int(options.nmax) > 0:
        print 'Reduce input stats to '+options.nmax+' for the signal model'
        sig = sig.reduce('EventId < '+options.nmax)
    sig = sig.reduce(ROOT.RooArgSet(DiPhoMassFit))
    
    if 'bkg' in dofit: bkgPdf = bkgModel(DiPhoMassFit,data_obs)    
    if 'sig' in dofit: sigPdf = sigModel(DiPhoMassFit,sig)
    if 'bkg' and 'sig' in dofit:
        combPdf = combModel(DiPhoMassFit,bkgPdf,sigPdf,data_obs)
        

    
    

