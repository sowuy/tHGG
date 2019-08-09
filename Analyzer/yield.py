import os
import sys
import math
import operator
import objects as obj
import tree as tr
from array import array
import xml.etree.ElementTree as ET
import functions as func
import utils as ut
import common as c
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Read file and print yields \n,\
            cut 0 = trigger passed \n,\
            cut 1 = at least 1 lepton \n,\
            cut 2 = at least 1 jet \n,\
            cut 3 = at least 1 selected jet \n,\
            cut 4 = control region only"

    parser = OptionParser(usage)
    parser.add_option("-o","--output",default="yieldFile.txt",help="output yield file [default: %default]")
    parser.add_option("-s","--sample",default="ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8",help="input sample [default: %default]")
    #parser.add_option("-s","--sample",default="DoubleEG",help="input sample [default: %default]")
    #parser.add_option("-s","--sample",default="QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8",help="input sample [default: %default]")
    #parser.add_option("-s","--sample",default="QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8",help="input sample [default: %default]")
    #parser.add_option("-s","--sample",default="QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8",help="input sample [default: %default]")
    parser.add_option("-x","--xml",default="sample_test_NTU.xml",help="input xml configuration [default: %default]")
    parser.add_option("-n","--nmax",default=-1,help="max number of events [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    ROOT.gROOT.SetBatch()

    sys.stdout= open(options.output,'w')


    files=[]
    xmlTree = ET.parse(options.xml)
    for s in xmlTree.findall('sample'):
        if s.get('id') == options.sample:
            isdata = s.get('isdata')
            xsec = s.get('xsec')
            stat = s.get('stat')

            for child in s:
                files.append(child.text)

    tr = ROOT.TChain(c.treeName)

    for f in files: tr.Add(f)

    nEntries = tr.GetEntries()

    if options.nmax!="-1" :
        print 'Number of events:', options.nmax
    else:
        print 'Number of events:', nEntries
    print 'Luminosity:', c.lumi
    print 'xsec:',xsec
    #print 'stat:',stat



    cut0=0
    cut1=0
    cut2=0
    cut3=0
    cut4=0
    cut5=0
    cut2_succ=0
    cut3_succ=0
    cut4_succ=0
    cut5_succ=0

    nEntries_wNorm=0
    cut0_wNorm=[]
    cut1_wNorm=[]
    cut2_wNorm=[]
    cut3_wNorm=[]
    cut4_wNorm=[]
    cut5_wNorm=[]
    cut2_wNorm_succ=[]
    cut3_wNorm_succ=[]
    cut4_wNorm_succ=[]
    cut5_wNorm_succ=[]
    stat = 0
    ieT=0
    for ev in tr:
        ieT = ieT + 1
        #if (ieT > int(options.nmax) and (int(options.nmax) >= 0)):
        #    break
        Event = obj.event(ev,isdata)
        stat += Event.weight
    print "stat : ",stat
    ie=0
    for ev in tr:
        ie = ie + 1
        #if ie!=9741:
        #    continue
        if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
            break

        Jets = []
        JetsBTagLoose = []
        JetsBTagMedium = []
        JetsBTagTight = []
        Leptons = []
        Electrons = []
        Muons = []
        Photons = []
        Event = obj.event(ev,isdata)

        #ttHJet sample weight
        if isdata=="0":
            w = Event.weight * c.lumi /(stat/float(xsec))
            #print "ie = %d, yields = %11.7f"%(ie,w)
        elif isdata=="1":
            w = 1
        nEntries_wNorm+=w

        passTrig = Event.trig
        if passTrig == False:
            continue


        nJet = ev.__getattr__("jets_size")
        for i in range(int(nJet)):
            j = obj.jet(ev,i)
            if j.passed:
                Jets.append(j)

        for i in range(2):
            p = obj.photon(ev,i)
            if p.passed:
                Photons.append(p)

        nPho = len(Photons)
        if nPho < 2: continue

        nElec = ev.__getattr__("ElecInfo.Size")
        for i in range(int(nElec)):
            l = obj.lepton(ev,i,True,Jets,Photons)
            if l.passed:
                Leptons.append(l)
                Electrons.append(l)

        nMuon = ev.__getattr__("MuonInfo.Size")
        for i in range(int(nMuon)):
            l = obj.lepton(ev,i,False,Jets,Photons)
            if l.passed:
                Leptons.append(l)
                Muons.append(l)

        Leptons.sort(key=operator.attrgetter('pt'))
        nLepSelected = len(Leptons)
        jetsToRemove=[]
        nJets = len(Jets)
        #print Jets[0].pt,Jets[1].pt,Jets[2].pt
        #print "[INFO_0] nJets = %d (before for loop)"%(nJets)
        for j in Jets:
            #print j
            #if ie==10643:
            #print 'index',jet
            #print 'Entry number: ', ie
            #print "(%d) Pt = %6.2f, Eta = %6.2f, Phi = %6.2f, Energy = %6.2f (jet)\n"%(indexJ,j.pt, j.eta, j.phi,j.E)
            #indexL = 0
            #if nLepSelected>0:
            #    for l in Leptons:
            #        print "(%d) Pt = %6.2f, Eta = %6.2f, Phi = %6.2f, Energy = %6.2f, deltaR = %6.2f (lepton)\n"%(indexL, l.pt, l.eta, l.phi,l.E,ut.deltaR(j.eta,j.phi,l.eta,l.phi))
            #        indexL+=1

            passedOverlapPhotons = func.overlap(j.eta,j.phi,Photons,0.4)[0]
            passedOverlapLeptons = func.overlap(j.eta,j.phi,Leptons,0.4)[0]
            #print testL,passedOverlapLeptons
            if not passedOverlapPhotons or not passedOverlapLeptons:
                jetsToRemove.append(j)
            else:
                if j.isBTagLoose:
                    JetsBTagLoose.append(j)
                if j.isBTagMedium:
                    JetsBTagMedium.append(j)
                if j.isBTagTight:
                    JetsBTagTight.append(j)
        for k in jetsToRemove:
            Jets.remove(k)

        nJetSelected = len(Jets)
        nJetBTagSelected = len(JetsBTagMedium)

        Jets.sort(key=operator.attrgetter('pt'))
        #YIELDS
        cut0+=1
        cut0_wNorm.append(w)
        if nLepSelected>=1:
            cut1+=1
            cut1_wNorm.append(w)
            if nJets>=1:
                cut2_succ+=1
                cut2_wNorm_succ.append(w)
                if nJetSelected >=1:
                    cut3_succ+=1
                    cut3_wNorm_succ.append(w)
                    if (Event.diPhoMass>100 and Event.diPhoMass<120) or (Event.diPhoMass<180 and Event.diPhoMass>130):
                        cut4_succ+=1
                        cut4_wNorm_succ.append(w)
                        if nJetBTagSelected>0:
                            cut5_succ+=1
                            cut5_wNorm_succ.append(w)

        if nJets>=1:
            cut2+=1
            cut2_wNorm.append(w)
        if nJetSelected >=1:
            cut3+=1
            cut3_wNorm.append(w)
        if (Event.diPhoMass>100 and Event.diPhoMass<120) or (Event.diPhoMass<180 and Event.diPhoMass>130):
            cut4+=1
            cut4_wNorm.append(w)
        if nJetBTagSelected>0:
            cut5+=1
            cut5_wNorm.append(w)



    #print 'Individual selection'
    print "Pass trigger:",cut0
    print 'cut1 : ', cut1
    print 'cut2 : ', cut2
    print 'cut3 : ', cut3
    print 'cut4 : ', cut4
    print 'cut5 : ', cut5
    #print 'Normalized to lumi'
    print "Number of events :",nEntries_wNorm
    print "Pass trigger :",sum(cut0_wNorm)
    print 'cut1 : ',sum(cut1_wNorm)
    print 'cut2 : ', sum(cut2_wNorm)
    print 'cut3 : ', sum(cut3_wNorm)
    print 'cut4 : ', sum(cut4_wNorm)
    print 'cut5 : ', sum(cut5_wNorm)
    #print "--------------------------------------------------"
    #print 'Successive selection'
    print 'cut2 successive : ', cut2_succ
    print 'cut3 successive : ', cut3_succ
    print 'cut4 successive : ', cut4_succ
    print 'cut5 successive : ', cut5_succ
    #print 'Normalized to lumi'
    print 'cut2 successive : ', sum(cut2_wNorm_succ)
    print 'cut3 successive : ', sum(cut3_wNorm_succ)
    print 'cut4 successive : ', sum(cut4_wNorm_succ)
    print 'cut5 successive : ', sum(cut5_wNorm_succ)
    sys.stdout.close()
