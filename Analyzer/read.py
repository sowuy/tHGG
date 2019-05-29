import os
import sys
import math
import operator
import objects as obj
import tree as tr
from array import array
import xml.etree.ElementTree as ET
import common as c
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Analysis script to select tH FCNC events"
    
    parser = OptionParser(usage)
    parser.add_option("-s","--sample",default="sample",help="input sample [default: %default]")
    parser.add_option("-x","--xml",default="samples.xml",help="input xml configuration [default: %default]")
    parser.add_option("-o","--output",default="output.root",help="output file name [default: %default]")
    parser.add_option("-n","--nmax",default=-1,help="max number of events [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

if __name__ == '__main__':
    
    options = main()
                
    ROOT.gROOT.SetBatch()

    outFile = ROOT.TFile.Open(options.output,"RECREATE")
    
    tLep = tr.tree('leptonic')
    tHad = tr.tree('hadronic')
    
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

    ie = 0
    
    for ev in tr:

        ie = ie + 1
        if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
            break
        
        Jets = []
        JetsBTag = []
        Leptons = []
        Photons = []

        Event = obj.event(ev,isdata)
        tLep.count(Event.weightb)
        
        passTrig = Event.trig
        if passTrig == False:
            continue

        nJet = ev.__getattr__("jets_size")
        for i in range(int(nJet)):
            j = obj.jet(ev,i)
            if j.passed:
                Jets.append(j)
                if j.isBTag:
                    JetsBTag.append(j)
        nJetSelected = len(Jets)
        nJetBTagSelected = len(JetsBTag)

        for i in range(2):
            p = obj.photon(ev,i)
            if p.passed:
                Photons.append(p)
                
        nElec = ev.__getattr__("ElecInfo.Size")
        for i in range(int(nElec)):
            l = obj.lepton(ev,i,1,Jets,Photons)
            if l.passed:
                Leptons.append(l)
                
        nMuon = ev.__getattr__("MuonInfo.Size")
        for i in range(int(nMuon)):
            l = obj.lepton(ev,i,0,Jets,Photons)
            if l.passed:
                Leptons.append(l)
                
        Leptons.sort(key=operator.attrgetter('pt'))
        Jets.sort(key=operator.attrgetter('pt'))
                
        nLepSelected = len(Leptons)
        
        nPho = len(Photons)
        if nPho < 2: continue
        
        if nJetBTagSelected == 0: continue

        for t in [tLep,tHad]:
            
            t.evNVtx[0] = Event.nVtx
            t.evWeight[0] = Event.weight
            t.evWeightb[0] = Event.weightb

            t.diPhoMass[0] = Event.diPhoMass
            t.diPhoMVA[0] = Event.diPhoMVA
            
            t.phoLeadIsGenMatched[0] = Photons[0].isGenMatched
            t.phoLeadIDMVA[0] = Photons[0].IDMVA
            
            t.phoSubLeadIsGenMatched[0] = Photons[1].isGenMatched
            t.phoSubLeadIDMVA[0] = Photons[1].IDMVA
        
            if nJetSelected > 0:
            
                t.jet1Pt = Jets[0].pt
                t.jet1Eta = Jets[0].eta
                t.jet1Phi = Jets[0].phi
                t.jet1E = Jets[0].E
                t.jet1Btag = Jets[0].btag

            if nJetSelected > 1:
                    
                t.jet2Pt = Jets[1].pt
                t.jet2Eta = Jets[1].eta
                t.jet2Phi = Jets[1].phi
                t.jet2E = Jets[1].E
                t.jet2Btag = Jets[1].btag
        
        if nJetSelected > 2:
            
            tHad.jet3Pt = Jets[2].pt
            tHad.jet3Eta = Jets[2].eta
            tHad.jet3Phi = Jets[2].phi
            tHad.jet3E = Jets[2].E
            tHad.jet3Btag = Jets[2].btag

        if nJetSelected > 3:
            
            tHad.jet4Pt = Jets[3].pt
            tHad.jet4Eta = Jets[3].eta
            tHad.jet4Phi = Jets[3].phi
            tHad.jet4E = Jets[3].E
            tHad.jet4Btag = Jets[3].btag
            
        if nLepSelected >= 1:

            tLep.lepPt[0] = Leptons[0].pt
            tLep.lepEta[0] = Leptons[0].eta
            tLep.lepPhi[0] = Leptons[0].phi
            tLep.lepE[0] = Leptons[0].E
            tLep.lepCharge[0] = Leptons[0].charge
            tLep.lepIsElec[0] = Leptons[0].isElec
            
            if nJetSelected >= 2:
                
                tLep.fill()
            
        else:
            
            if nJetSelected >= 4:
            
                tHad.fill()
        
    outFile.Write()
    outFile.Close()
