import os
import sys
import math
import operator
import objects as obj
import tree as tr
from array import array
import numpy as np
import xml.etree.ElementTree as ET
import functions as func
import utils as ut
import common as c
import ROOT
import toprec as top

ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Analysis script to select tH FCNC events"

    parser = OptionParser(usage)
    parser.add_option("-s","--sample",default="sample",help="input sample [default: %default]")
    parser.add_option("-x","--xml",default="samples.xml",help="input xml configuration [default: %default]")
    parser.add_option("-p","--pdf",default="pdf.root",help="input file with pdfs [default: %default]")
    parser.add_option("-r","--run",default="",help="special run mode [default: %default]")
    parser.add_option("-t","--toprec",default=0,help="do top reconstruction [default: %default]")
    parser.add_option("-o","--output",default="output.root",help="output file name [default: %default]")
    parser.add_option("-n","--nmax",default=-1,help="max number of events [default: %default]")
    parser.add_option("-m","--mcPuFile",default="data/MCPileUp.root",help="mc pile up file name [default: %default]")
    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    ROOT.gROOT.SetBatch()

    mcpuFile = ROOT.TFile.Open(options.mcPuFile)
    h_pu = mcpuFile.Get("puhist")

    outFile = ROOT.TFile.Open(options.output,"RECREATE")

    run = options.run

    if run == '':
        tLep = tr.tree('leptonic')
        tHad = tr.tree('hadronic')
        tAll = tr.tree('all')
    elif run == 'pdf':
        tLep = tr.tree('pdf')
    else:
        print 'Run mode', run, 'is not defined'
        exit()

    files=[]
    xmlTree = ET.parse(options.xml)
    for s in xmlTree.findall('sample'):
        if s.get('id') == options.sample:
            isdata = s.get('isdata')
            for child in s:
                files.append(child.text)

    tr = ROOT.TChain(c.treeName)

    for f in files: tr.Add(f)


    nEntries = tr.GetEntries()
    print 'Number of events:', nEntries

    if options.toprec:
        trec = top.toprec(options.pdf)

    ie = 0

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
        Gen = obj.gen(ev)
        Met = obj.met(ev)
#        tLep.count(Event.weightb)
        tLep.count(Event.weight)


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

        higgs = obj.higgs(Photons[0],Photons[1])

        #if nJetBTagSelected == 0: continue

        if run == '':

            for t in [tLep,tHad,tAll]:
                t.evNVtx[0] = Event.nVtx
                t.evPuFactor[0] = Event.puReweightingFactor(h_pu)
                t.evWeight[0] = Event.weight
                t.evWeightb[0] = Event.weightb
                t.evNJet[0] = nJetSelected
                t.evNBLJet[0] = len(JetsBTagLoose)
                t.evNBMJet[0] = len(JetsBTagMedium)
                t.evNBTJet[0] = len(JetsBTagTight)
                t.evNLep[0] = nLepSelected

                t.diPhoMass[0] = Event.diPhoMass
                t.diPhoPt[0] = Event.diPhoPt
                t.diPhoMVA[0] = Event.diPhoMVA

                t.phoLeadIsGenMatched[0] = Photons[0].isGenMatched
                t.phoLeadIDMVA[0] = Photons[0].IDMVA
                t.phoLeadpT[0] = Photons[0].pt
                t.phoLeadEta[0] = Photons[0].eta
                t.phoLeadPhi[0] = Photons[0].phi

                t.phoSubLeadIsGenMatched[0] = Photons[1].isGenMatched
                t.phoSubLeadIDMVA[0] = Photons[1].IDMVA
                t.phoSubLeadpT[0] = Photons[1].pt
                t.phoSubLeadEta[0] = Photons[1].eta
                t.phoSubLeadPhi[0] = Photons[1].phi


                t.higgsPt[0] = higgs.pt
                t.higgsEta[0] = higgs.eta
                t.higgsPhi[0] = higgs.phi

                if nJetSelected > 0:

                    t.jet1Pt[0] = Jets[0].pt
                    t.jet1Eta[0] = Jets[0].eta
                    t.jet1Phi[0] = Jets[0].phi
                    t.jet1E[0] = Jets[0].E
                    t.jet1Btag[0] = Jets[0].btag
                    t.jet1deltaRLeadPho[0] = ut.deltaR(Jets[0].eta,Jets[0].phi,Photons[0].eta,Photons[0].phi)
                    t.jet1deltaRSubLeadPho[0] = ut.deltaR(Jets[0].eta,Jets[0].phi,Photons[1].eta,Photons[1].phi)
                    t.jet1deltaRHiggs[0] = ut.deltaR(Jets[0].eta,Jets[0].phi,higgs.eta,higgs.phi)
                    if nLepSelected >= 1:
                        t.jet1deltaRLep[0] = ut.deltaR(Jets[0].eta,Jets[0].phi,Leptons[0].eta,Leptons[0].phi)

                if nJetSelected > 1:

                    t.jet2Pt[0] = Jets[1].pt
                    t.jet2Eta[0] = Jets[1].eta
                    t.jet2Phi[0] = Jets[1].phi
                    t.jet2E[0] = Jets[1].E
                    t.jet2Btag[0] = Jets[1].btag
                    t.jet2deltaRLeadPho[0] = ut.deltaR(Jets[1].eta,Jets[1].phi,Photons[0].eta,Photons[0].phi)
                    t.jet2deltaRSubLeadPho[0] = ut.deltaR(Jets[1].eta,Jets[1].phi,Photons[1].eta,Photons[1].phi)
                    t.jet2deltaRHiggs[0] = ut.deltaR(Jets[1].eta,Jets[1].phi,higgs.eta,higgs.phi)
                    if nLepSelected >= 1:
                        t.jet2deltaRLep[0] = ut.deltaR(Jets[1].eta,Jets[1].phi,Leptons[0].eta,Leptons[0].phi)

            #tAll.setweight(w)
            tAll.fill()

            if nJetSelected > 2:

                tHad.jet3Pt[0] = Jets[2].pt
                tHad.jet3Eta[0] = Jets[2].eta
                tHad.jet3Phi[0] = Jets[2].phi
                tHad.jet3E[0] = Jets[2].E
                tHad.jet3Btag[0] = Jets[2].btag
                tHad.jet3deltaRLeadPho[0] = ut.deltaR(Jets[2].eta,Jets[2].phi,Photons[0].eta,Photons[0].phi)
                tHad.jet3deltaRSubLeadPho[0] = ut.deltaR(Jets[2].eta,Jets[2].phi,Photons[1].eta,Photons[1].phi)
                tHad.jet3deltaRHiggs[0] = ut.deltaR(Jets[2].eta,Jets[2].phi,higgs.eta,higgs.phi)

            if nJetSelected > 3:

                tHad.jet4Pt[0] = Jets[3].pt
                tHad.jet4Eta[0] = Jets[3].eta
                tHad.jet4Phi[0] = Jets[3].phi
                tHad.jet4E[0] = Jets[3].E
                tHad.jet4Btag[0] = Jets[3].btag
                tHad.jet4deltaRLeadPho[0] = ut.deltaR(Jets[3].eta,Jets[3].phi,Photons[0].eta,Photons[0].phi)
                tHad.jet4deltaRSubLeadPho[0] = ut.deltaR(Jets[3].eta,Jets[3].phi,Photons[1].eta,Photons[1].phi)
                tHad.jet4deltaRHiggs[0] = ut.deltaR(Jets[3].eta,Jets[3].phi,higgs.eta,higgs.phi)

            if nLepSelected >= 1:

                tLep.lepPt[0] = Leptons[0].pt
                tLep.lepEta[0] = Leptons[0].eta
                tLep.lepPhi[0] = Leptons[0].phi
                tLep.lepE[0] = Leptons[0].E
                tLep.lepCharge[0] = Leptons[0].charge
                tLep.lepIsElec[0] = Leptons[0].isElec
                tLep.lepDrlpMin[0] = Leptons[0].drlpMin
                tLep.lepPhMllMin[0] = func.zveto(Leptons[0],Photons,91.2,777)[1]
                tLep.lepDeltaRLeadPho[0] = ut.deltaR(Leptons[0].eta,Leptons[0].phi,Photons[0].eta,Photons[0].phi)
                tLep.lepDeltaRSubLeadPho[0] = ut.deltaR(Leptons[0].eta,Leptons[0].phi,Photons[1].eta,Photons[1].phi)
                tLep.lepDeltaRHiggs[0] = ut.deltaR(Leptons[0].eta,Leptons[0].phi,higgs.eta,higgs.phi)

                if nJetSelected >= 1:

                    '''if options.toprec:

                        lh, nuPz, mW, mTop = trec.calcLep(Leptons[0],Met,JetsBTagMedium[0])

                        tLep.topRecLH[0] = lh
                        tLep.topRecNuPz[0] = nuPz
                        tLep.topRecMW[0] = mW
                        tLep.topRecMTop[0] = mTop'''

                    tLep.metPt[0] = Met.pt
                    tLep.metPhi[0] = Met.phi
                    tLep.metPx[0] = Met.px
                    tLep.metPy[0] = Met.py
                    tLep.sumET[0] = Met.sumET

                    tLep.fill()

            elif nLepSelected == 0:

                if nJetSelected >= 3:
                    
                    tHad.fill()


    outFile.Write()
    outFile.Close()




