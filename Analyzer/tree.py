import os
import sys
import math
from array import array
import utils
import ROOT

class tree():

    def __init__(self, name):

        self.lepPt, self.lepEta, self.lepPhi, self.lepE, self.evWeight, \
        self.diPhoMass = (array( 'f', [ -777 ] ) for _ in range(6))
        
        self.lepCharge, self.evNVtx = (array( 'i', [ -777 ] ) for _ in range(2))

        self.phoLeadIsGenMatched, self.phoSubLeadIsGenMatched = (array( 'b', [ 0 ] ) for _ in range(2))

        self.t = ROOT.TTree( name, 'Analysis tree' )
        
        self.t.Branch( 'evNVtx', self.evNVtx, 'evNVtx/I' )
        self.t.Branch( 'evWeight', self.evWeight, 'evWeight/F' )
        
        self.t.Branch( 'diPhoMass', self.diPhoMass, 'diPhoMass/F' )
        
#        self.t.Branch( 'phoLeadIsGenMatched', self.phoLeadIsGenMatched, 'phoLeadIsGenMatched/O' )
#        self.t.Branch( 'phoSubLeadIsGenMatched', self.phoSubLeadIsGenMatched, 'phoSubLeadIsGenMatched/O' )
        
        if (name == 'leptonic'):

            self.t.Branch( 'lepPt', self.lepPt, 'lepPt/F' )
            self.t.Branch( 'lepEta', self.lepEta, 'lepEta/F' )
            self.t.Branch( 'lepPhi', self.lepPhi, 'lepPhi/F' )
            self.t.Branch( 'lepE', self.lepE, 'lepE/F' )
            self.t.Branch( 'lepCharge', self.lepCharge, 'lepCharge/I' )

    def fill(self):
        
        self.t.Fill()
