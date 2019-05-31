import os
import sys
import math
import utils
import ROOT
import functions as fun

class event():
    
    def __init__(self, ev, isdata):

        self.nVtx = ev.__getattr__("EvtInfo.NVtx")
        self.weight = ev.__getattr__("EvtInfo.genweight")
        if isdata == "1": self.weight = 1
        if self.weight > 0:
            self.weightb = 1
        else:
            self.weightb = -1
        self.trig = ev.__getattr__("EvtInfo.passTrigger")
        
        self.diPhoMass = ev.__getattr__("DiPhoInfo.mass")
        self.diPhoMVA = ev.__getattr__("DiPhoInfo.diphotonMVA")

class jet():

    idx = -1
    
    def __init__(self, ev, idx):

        self.idx = idx
        self.passed = False
    
        self.pt = ev.__getattr__("JetInfo.Pt")[idx]
        self.eta = ev.__getattr__("JetInfo.Eta")[idx]
        self.phi = ev.__getattr__("JetInfo.Phi")[idx]
        self.E = ev.__getattr__("JetInfo.Energy")[idx]
        
        self.puIdMVA = ev.__getattr__("JetInfo.puJetIdMVA")[idx]
        
        self.btag = ev.__getattr__("JetInfo.pfDeepCSVJetTags_probb")[idx]+ev.__getattr__("JetInfo.pfDeepCSVJetTags_probbb")[idx]
        self.isBTagLoose = bool(self.btag > 0.1522)
        self.isBTagMedium = bool(self.btag > 0.4941)
        self.isBTagTight = bool(self.btag > 0.8001)

        passPt = bool(self.pt > 25)
        passEta = bool(math.fabs(self.eta) < 2.4)
#        passPU = (ev.__getattr__("JetInfo.puJetIdMVA")[idx] & (1 << 0))
        
        self.passed = (passPt and passEta)

class photon():

    idx = -1
    
    def __init__(self, ev, idx):

        self.idx = idx
        self.passed = False
        
        self.diPhoMass = ev.__getattr__("DiPhoInfo.mass")
        if self.diPhoMass < 0:
            return
    
        if idx == 0:
            
            self.pt = ev.__getattr__("DiPhoInfo.leadPt")
            self.eta = ev.__getattr__("DiPhoInfo.leadEta")
            self.phi = ev.__getattr__("DiPhoInfo.leadPhi")
            self.E = ev.__getattr__("DiPhoInfo.leadE")
            
            self.IDMVA = ev.__getattr__("DiPhoInfo.leadIDMVA")
            self.isGenMatched = ev.__getattr__("DiPhoInfo.leadGenMatch")
            
            passPt = bool(self.pt > self.diPhoMass/2)
        
#            passID = bool(ev.__getattr__("DiPhoInfo.leadIDMVA") > -0.4)
        
        else:
            
            self.pt = ev.__getattr__("DiPhoInfo.subleadPt")
            self.eta = ev.__getattr__("DiPhoInfo.subleadEta")
            self.phi = ev.__getattr__("DiPhoInfo.subleadPhi")
            self.E = ev.__getattr__("DiPhoInfo.subleadE")
            
            self.IDMVA = ev.__getattr__("DiPhoInfo.subleadIDMVA")
            self.isGenMatched = ev.__getattr__("DiPhoInfo.subleadGenMatch")
            
            passPt = bool(self.pt > self.diPhoMass/4)
        
#            passID = bool(ev.__getattr__("DiPhoInfo.subleadIDMVA") > -0.4)
        
        self.passed = (passPt)
        
class lepton():

    idx = -1
    
    def __init__(self, ev, idx, isElec, Jets, Photons):
        
        self.idx = idx
        self.isElec = isElec
        self.passed = False
        
        if (isElec):
      
            self.pt = ev.__getattr__("ElecInfo.Pt")[idx]
            self.eta = ev.__getattr__("ElecInfo.Eta")[idx]
            self.phi = ev.__getattr__("ElecInfo.Phi")[idx]
            self.E = ev.__getattr__("ElecInfo.Energy")[idx]
            self.charge = ev.__getattr__("ElecInfo.Charge")[idx]
            
            passPt = bool(self.pt > 20)
            passEta = bool((math.fabs(self.eta) < 1.4442 or math.fabs(self.eta) > 1.566) and math.fabs(self.eta) < 2.4)
#            passOverlapPhotons = bool(ev.__getattr__("ElecInfo.fggPhoVeto")[idx])
            passOverlapPhotons, self.drlpMin = fun.overlap(self.eta,self.phi,Photons,0.3)
#            passID = bool(ev.__getattr__("ElecInfo.EGMCutBasedIDLoose")[idx])
            passID = bool(ev.__getattr__("ElecInfo.EGMCutBasedIDMedium")[idx])
#            passDxy = (math.fabs(ev.__getattr__("ElecInfo.GsfTrackDxy")[idx]) < 0.02)
#            passDz = (math.fabs(ev.__getattr__("ElecInfo.GsfTrackDz")[idx]) < 0.2)

            if (passPt and passEta and passID and passOverlapPhotons): self.passed = True
            
        else:
            
            self.pt = ev.__getattr__("MuonInfo.Pt")[idx]
            self.eta = ev.__getattr__("MuonInfo.Eta")[idx]
            self.phi = ev.__getattr__("MuonInfo.Phi")[idx]
            self.E = ev.__getattr__("MuonInfo.Energy")[idx]
            self.iso = ev.__getattr__("MuonInfo.PFIsoDeltaBetaCorrR04")[idx]
            self.charge = ev.__getattr__("MuonInfo.Charge")[idx]
            
            passPt = bool(self.pt > 20)
            passEta = bool(math.fabs(self.eta) < 2.4)
            passTight = bool(ev.__getattr__("MuonInfo.CutBasedIdTight")[idx])
            passIso = bool(self.iso < 0.25)
            passOverlapPhotons, self.drlpMin = fun.overlap(self.eta,self.phi,Photons,0.3)
            
            self.passed = (passPt and passEta and passTight and passIso and passOverlapPhotons)
