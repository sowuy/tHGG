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
    parser.add_option("-o","--output",default="yieldFile_2.txt",help="output yield file [default: %default]")
    #parser.add_option("-i","--inputf",default="/home/ucl/cp3/swuycken/scratch/CMSSW_10_5_0/src/tHGG/Analyzer/uniqueSample/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_0.root",help="Input root file [default: %default]")
    parser.add_option("-s","--sample",default="sample",help="input sample [default: %default]")
    parser.add_option("-x","--xml",default="samples.xml",help="input xml configuration [default: %default]")
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
        #if s.get('id') == options.sample:
            isdata = s.get('isdata')
            for child in s:
                files.append(child.text)

    tr = ROOT.TChain(c.treeName)

    for f in files: tr.Add(f)

    nEntries = tr.GetEntries()
    print 'Number of events:', nEntries

    ie=0
    cut0=0
    cut1=0
    cut2=0
    cut3=0
    cut4=0
    cut0_wNorm=[]
    cut1_wNorm=[]
    cut2_wNorm=[]
    cut3_wNorm=[]
    cut4_wNorm=[]

    for ev in tr:
        ie = ie + 1

        if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
            break

        Jets = []
        JetsBTagLoose = []
        JetsBTagMedium = []
        JetsBTagTight = []
        Leptons = []
        Photons = []
        Event = obj.event(ev,isdata)

        #ttHJet sample weight
        if isdata=="0":
            w = Event.weight * c.lumi / (409426.09375/0.0016)
        elif isdata="1":
            w = 1

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


        nElec = ev.__getattr__("ElecInfo.Size")
        for i in range(int(nElec)):
            l = obj.lepton(ev,i,True,Jets,Photons)
            if l.passed:
                Leptons.append(l)

        nMuon = ev.__getattr__("MuonInfo.Size")
        for i in range(int(nMuon)):
            l = obj.lepton(ev,i,False,Jets,Photons)
            if l.passed:
                Leptons.append(l)

        nJets = len(Jets)
        for j in Jets:
            passedOverlapPhotons = func.overlap(j.eta,j.phi,Photons,0.4)[0]
            passedOverlapLeptons = func.overlap(j.eta,j.phi,Leptons,0.4)[0]
            if not passedOverlapPhotons or not passedOverlapLeptons:
                Jets.remove(j)
            else:
                if j.isBTagLoose:
                    JetsBTagLoose.append(j)
                if j.isBTagMedium:
                    JetsBTagMedium.append(j)
                if j.isBTagTight:
                    JetsBTagTight.append(j)

        nJetSelected = len(Jets)
        nJetBTagSelected = len(JetsBTagMedium)

        Leptons.sort(key=operator.attrgetter('pt'))
        Jets.sort(key=operator.attrgetter('pt'))

        nLepSelected = len(Leptons)

        #YIELDS
        cut0+=1
        #cut0_wNorm.append(w)
        if nLepSelected>=1:
            cut1+=1
            cut1_wNorm.append(w)
        if nJets>=1:
            cut2+=1
            cut2_wNorm.append(w)
        if nJetSelected >=1:
            cut3+=1
            cut3_wNorm.append(w)
        if (Event.diPhoMass>100 and Event.diPhoMass<120) or (Event.diPhoMass<180 and Event.diPhoMass>130):
            cut4+=1
            cut4_wNorm.append(w)



    print "Event :",cut0
    print 'Entries in control region : ', cut4
    print 'Entries with at leat one lepton : ', cut1
    print 'Entries with at leat one jet : ', cut2
    print 'Entries with at leat one jet selected : ', cut3
    print "Event :",sum(cut0_wNorm)
    print 'Entries in control region : ', sum(cut4_wNorm)
    print 'Entries with at leat one lepton : ',sum(cut1_wNorm)
    print 'Entries with at leat one jet : ', sum(cut2_wNorm)
    print 'Entries with at leat one jet selected : ', sum(cut3_wNorm)
