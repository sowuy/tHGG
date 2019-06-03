import os
import sys
import math
from array import array
import utils
import ROOT

class tree():

    def __init__(self, name):

        self.lepPt, self.lepEta, self.lepPhi, self.lepE, self.evWeight, self.evWeightb, \
        self.diPhoMass, self.phoLeadIDMVA, self.phoSubLeadIDMVA, self.diPhoMVA, \
        self.jet1Pt, self.jet1Eta, self.jet1Phi, self.jet1E, self.jet1Btag, \
        self.jet2Pt, self.jet2Eta, self.jet2Phi, self.jet2E, self.jet2Btag, \
        self.jet3Pt, self.jet3Eta, self.jet3Phi, self.jet3E, self.jet3Btag, \
        self.jet4Pt, self.jet4Eta, self.jet4Phi, self.jet4E, self.jet4Btag, \
        self.lepDrlpMin, self.lepPhMllMin, \
        self.topRecLH, self.topRecNuPz, self.topRecMW, self.topRecMTop, \
        self.metPt, self.metPhi, self.metPx, self.metPy, self.sumET \
        = (array( 'f', [ -777 ] ) for _ in range(41))
        
        self.lepCharge, self.evNVtx, self.evNJet, self.evNLep, self.evNBLJet, self.evNBMJet, self.evNBTJet \
        = (array( 'i', [ -777 ] ) for _ in range(7))

        self.phoLeadIsGenMatched, self.phoSubLeadIsGenMatched, self.lepIsElec \
        = (array( 'b', [ 0 ] ) for _ in range(3))

        if name == 'leptonic':
            self.h = ROOT.TH1F ( 'counter', 'counter', 1, 0., 1. )
        
        self.t = ROOT.TTree( name, 'Analysis tree' )
        
        self.t.Branch( 'evNVtx', self.evNVtx, 'evNVtx/I' )
        self.t.Branch( 'evWeight', self.evWeight, 'evWeight/F' )
        self.t.Branch( 'evWeightb', self.evWeightb, 'evWeightb/F' )
        
        self.t.Branch( 'evNJet', self.evNJet, 'evNJet/I' )
        self.t.Branch( 'evNBLJet', self.evNBLJet, 'evNBLJet/I' )
        self.t.Branch( 'evNBMJet', self.evNBMJet, 'evNBMJet/I' )
        self.t.Branch( 'evNBTJet', self.evNBTJet, 'evNBTJet/I' )
        self.t.Branch( 'evNLep', self.evNLep, 'evNLep/I' )
        
        self.t.Branch( 'diPhoMass', self.diPhoMass, 'diPhoMass/F' )
        self.t.Branch( 'diPhoMVA', self.diPhoMVA, 'diPhoMVA/F' )
        
        self.t.Branch( 'phoLeadIsGenMatched', self.phoLeadIsGenMatched, 'phoLeadIsGenMatched/O' )
        self.t.Branch( 'phoLeadIDMVA', self.phoLeadIDMVA, 'phoLeadIDMVA/F' )
        
        self.t.Branch( 'phoSubLeadIsGenMatched', self.phoSubLeadIsGenMatched, 'phoSubLeadIsGenMatched/O' )
        self.t.Branch( 'phoSubLeadIDMVA', self.phoSubLeadIDMVA, 'phoSubLeadIDMVA/F' )
        
        self.t.Branch( 'jet1Pt', self.jet1Pt, 'jet1Pt/F' )
        self.t.Branch( 'jet1Eta', self.jet1Eta, 'jet1Eta/F' )
        self.t.Branch( 'jet1Phi', self.jet1Phi, 'jet1Phi/F' )
        self.t.Branch( 'jet1E', self.jet1E, 'jet1E/F' )
        self.t.Branch( 'jet1Btag', self.jet1Btag, 'jet1Btag/F' )

        self.t.Branch( 'jet2Pt', self.jet2Pt, 'jet2Pt/F' )
        self.t.Branch( 'jet2Eta', self.jet2Eta, 'jet2Eta/F' )
        self.t.Branch( 'jet2Phi', self.jet2Phi, 'jet2Phi/F' )
        self.t.Branch( 'jet2E', self.jet2E, 'jet2E/F' )
        self.t.Branch( 'jet2Btag', self.jet2Btag, 'jet2Btag/F' )
        
        if (name == 'hadronic'):
            
            self.t.Branch( 'jet3Pt', self.jet3Pt, 'jet3Pt/F' )
            self.t.Branch( 'jet3Eta', self.jet3Eta, 'jet3Eta/F' )
            self.t.Branch( 'jet3Phi', self.jet3Phi, 'jet3Phi/F' )
            self.t.Branch( 'jet3E', self.jet3E, 'jet3E/F' )
            self.t.Branch( 'jet3Btag', self.jet3Btag, 'jet3Btag/F' )

            self.t.Branch( 'jet4Pt', self.jet4Pt, 'jet4Pt/F' )
            self.t.Branch( 'jet4Eta', self.jet4Eta, 'jet4Eta/F' )
            self.t.Branch( 'jet4Phi', self.jet4Phi, 'jet4Phi/F' )
            self.t.Branch( 'jet4E', self.jet4E, 'jet4E/F' )
            self.t.Branch( 'jet4Btag', self.jet4Btag, 'jet4Btag/F' )
            
        if (name == 'leptonic'):

            self.t.Branch( 'lepPt', self.lepPt, 'lepPt/F' )
            self.t.Branch( 'lepEta', self.lepEta, 'lepEta/F' )
            self.t.Branch( 'lepPhi', self.lepPhi, 'lepPhi/F' )
            self.t.Branch( 'lepE', self.lepE, 'lepE/F' )
            self.t.Branch( 'lepCharge', self.lepCharge, 'lepCharge/I' )
            self.t.Branch( 'lepIsElec', self.lepIsElec, 'lepIsElec/O' )
            self.t.Branch( 'lepDrlpMin', self.lepDrlpMin, 'lepDrlpMin/F' )
            self.t.Branch( 'lepPhMllMin', self.lepPhMllMin, 'lepPhMllMin/F' )
            
            self.t.Branch( 'metPt', self.metPt, 'metPt/F' )
            self.t.Branch( 'metPhi', self.metPhi, 'metPhi/F' )
            self.t.Branch( 'metPx', self.metPx, 'metPx/F' )
            self.t.Branch( 'metPy', self.metPy, 'metPy/F' )
            self.t.Branch( 'sumET', self.sumET, 'sumET/F' )
            
            self.t.Branch( 'topRecLH', self.topRecLH, 'topRecLH/F' )
            self.t.Branch( 'topRecNuPz', self.topRecNuPz, 'topRecNuPz/F' )
            self.t.Branch( 'topRecMW', self.topRecMW, 'topRecMW/F' )
            self.t.Branch( 'topRecMTop', self.topRecMTop, 'topRecMTop/F' )

    def fill(self):
        
        self.t.Fill()

    def count(self, w):
        
        self.h.SetBinContent(1,self.h.GetBinContent(1)+w)
        
