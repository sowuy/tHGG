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
    parser.add_option("-o","--output",default="output",help="file output name [default: %default]")
    parser.add_option("-n","--nmax",default=-1,help="max number of events [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

if __name__ == '__main__':
    
    options = main()
                
    ROOT.gROOT.SetBatch()

    outFile = ROOT.TFile(options.output,"RECREATE")
    
    tLep = tr.tree('leptonic')
    tHad = tr.tree('hadronic')
    
    files=[]
    xmlTree = ET.parse(c.workdir+c.xmlName)
    for s in xmlTree.findall('sample'):
        if s.get('id') == options.sample:
            isdata = s.get('isdata')
            for child in s:
                files.append(child.text)

    tr = ROOT.TChain(c.treeName)

    for f in files: tr.Add(f)

    nEntries = tr.GetEntries()

    ie = 0
    
    for ev in tr:

        if (ie > int(options.nmax) and int(options.nmax) >= 0): break
        
        Jets = []
        Leptons = []
        Photons = []

        Event = obj.event(ev)

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
            l = obj.lepton(ev,i,1,Jets,Photons)
            if l.passed:
                Leptons.append(l)
                
        nMuon = ev.__getattr__("MuonInfo.Size")
        for i in range(int(nMuon)):
            l = obj.lepton(ev,i,0,Jets,Photons)
            if l.passed:
                Leptons.append(l)
                
        Leptons.sort(key=operator.attrgetter('pt'))
                
        nLep = len(Leptons)

        for t in [tLep,tHad]:
            
            t.evNVtx[0] = Event.nVtx
            t.evWeight[0] = Event.weight

            t.diPhoMass[0] = Event.diPhoMass
        
        if( nLep == 1 ):                            
           
            tLep.lepPt[0] = Leptons[0].pt
            tLep.lepEta[0] = Leptons[0].eta
            tLep.lepPhi[0] = Leptons[0].phi
            tLep.lepE[0] = Leptons[0].E
            tLep.lepCharge[0] = Leptons[0].charge

            tLep.fill()
            
        elif( nLep == 0 ):
            
            tHad.fill()

        ie = ie + 1
        
    outFile.Write()
    outFile.Close()
