import math
import ROOT

class toprec():
    
    def __init__(self, fileName):

        self.fPDF = ROOT.TFile.Open(fileName)
        self.hPDF = {}
        self.rnd = ROOT.TRandom3(777)
        self.ns = 3
        self.toys = 10
        self.setPDF()

    def getWmassBW(self, mWmean, GammaW, nSigma):

        mW = 0.
             
        max = self.BW(mWmean,mWmean,GammaW)
                
        while True:

            r1 = self.rnd.Rndm()
            r2 = self.rnd.Rndm()
                     
            mW = mWmean - nSigma*GammaW + 2*nSigma*GammaW*r1
            if mW <= 0: continue
            if self.BW(mW,mWmean,GammaW) > max*r2: break
                                
        return mW      
                            
    def BW(self, mW, mWmean, GammaW):
        
        return mWmean*mWmean*GammaW*GammaW/(math.pow(mW*mW-mWmean*mWmean,2)+mWmean*mWmean*GammaW*GammaW)

    def getNuMom(self, Wmass, WTmass, lPx, lPy, lPz, lE, nuPx, nuPy):
    
        solved = False
        solvedt = False
        nuPz1 = -777
        nuPz2 = -777
        nuPz3 = -777
        nuPz4 = -777
        
        a = math.sqrt(lPx*lPx+lPy*lPy)
        b = lPz
        d = math.sqrt(nuPx*nuPx+nuPy*nuPy)
        f = lE
        
        c = Wmass*Wmass/2+lPx*nuPx+lPy*nuPy
        ct = WTmass*WTmass/2+lPx*nuPx+lPy*nuPy

        racine = c*c*b*b-a*a*(d*d*f*f-c*c)
        racinet = ct*ct*b*b-a*a*(d*d*f*f-ct*ct)
        
        if racine >= 0:

            solved = 1
            nuPz1 = (c*b+math.sqrt(racine))/a/a
            nuPz2 = (c*b-math.sqrt(racine))/a/a

        if racinet >= 0:

            solvedt = 1
            nuPz3 = (ct*b+math.sqrt(racinet))/a/a
            nuPz4 = (ct*b-math.sqrt(racinet))/a/a
            
        return solved, solvedt, nuPz1, nuPz2, nuPz3, nuPz4

    def setPDF(self):
    
#        for h in ['dBJetPx','dBJetPy','dBJetPz','dBJetE',\
#        'dMetPx','dMetPy',\
#        'dElecPx','dElecPy','dElecPz','dElecE',\
#        'dMuonPx','dMuonPy','dMuonPz','dMuonE',\
#        'TopWM','TopM']:
        for h in ['dMetPx','dMetPy',\
        'dElecPx','dElecPy','dElecPz','dElecE',\
        'dMuonPx','dMuonPy','dMuonPz','dMuonE',\
        'TopWM']:
            self.hPDF[h] = []
            lab = '_Fit'
            if h in ['dMetPx','dMetPy']: lab = '_Gaus'
            self.hPDF[h].append(self.fPDF.Get(h+lab))
            self.hPDF[h].append(self.hPDF[h][0].GetMaximum())
            self.hPDF[h].append(self.hPDF[h][0].GetMaximumX())
            self.hPDF[h].append(math.fabs(self.hPDF[h][0].GetX(0.5)))

    def getProb(self, hPDF, var):

        return hPDF.Eval(var)
            
    def getProbGaus(self, h, max, mean, sigma):
   
        x = 0.
        
        while True:
        
            r1 = self.rnd.Rndm()
            r2 = self.rnd.Rndm()
              
            x = mean - self.ns*sigma + 2*self.ns*sigma*r1
            if x <= 0: continue
            if h.Eval(x) > max*r2: break

        return x

    def calc(self, l, nu, bjet):
    
        lhMin = 10E+10
        nuPz = -777
        mW = -777
        mTop = -777

        for t in range(self.toys):

            pNuPx = self.getProbGaus(self.hPDF['dMetPx'][0],self.hPDF['dMetPx'][1],self.hPDF['dMetPx'][2],self.hPDF['dMetPx'][3])+nu.px;
            pNuPy = self.getProbGaus(self.hPDF['dMetPy'][0],self.hPDF['dMetPy'][1],self.hPDF['dMetPy'][2],self.hPDF['dMetPy'][3])+nu.py;
            
            pWMass = self.getWmassBW(80.4,2.1,5)
            
#            while True:
                
#                pBJetPx = self.getProbGaus(self.hPDF['dBJetPx'][0],self.hPDF['dBJetPx'][1],self.hPDF['dBJetPx'][2],self.hPDF['dBJetPx'][3])+bjet.px;
#                pBJetPy = self.getProbGaus(self.hPDF['dBJetPy'][0],self.hPDF['dBJetPy'][1],self.hPDF['dBJetPy'][2],self.hPDF['dBJetPy'][3])+bjet.py;
#                pBJetPz = self.getProbGaus(self.hPDF['dBJetPz'][0],self.hPDF['dBJetPz'][1],self.hPDF['dBJetPz'][2],self.hPDF['dBJetPz'][3])+bjet.pz;
#                pBJetE = self.getProbGaus(self.hPDF['dBJetE'][0],self.hPDF['dBJetE'][1],self.hPDF['dBJetE'][2],self.hPDF['dBJetE'][3])+bjet.E;
 #               if pBJetE*pBJetE-pBJetPx*pBJetPx-pBJetPy*pBJetPy-pBJetPz*pBJetPz > 0: break
                
            lab = 'Muon'
            if l.isElec: lab = 'Elec'
                
            while True:
                
                pLepPx = self.getProbGaus(self.hPDF['d'+lab+'Px'][0],self.hPDF['d'+lab+'Px'][1],self.hPDF['d'+lab+'Px'][2],self.hPDF['d'+lab+'Px'][3])+l.px;
                pLepPy = self.getProbGaus(self.hPDF['d'+lab+'Py'][0],self.hPDF['d'+lab+'Py'][1],self.hPDF['d'+lab+'Py'][2],self.hPDF['d'+lab+'Py'][3])+l.py;
                pLepPz = self.getProbGaus(self.hPDF['d'+lab+'Pz'][0],self.hPDF['d'+lab+'Pz'][1],self.hPDF['d'+lab+'Pz'][2],self.hPDF['d'+lab+'Pz'][3])+l.pz;
                pLepE = self.getProbGaus(self.hPDF['d'+lab+'E'][0],self.hPDF['d'+lab+'E'][1],self.hPDF['d'+lab+'E'][2],self.hPDF['d'+lab+'E'][3])+l.E;
                if pLepE*pLepE-pLepPx*pLepPx-pLepPy*pLepPy-pLepPz*pLepPz > 0: break

            pNuET = math.sqrt(pNuPx*pNuPx+pNuPy*pNuPy)
            pLepET = math.sqrt(pLepPx*pLepPx+pLepPy*pLepPy)
            mWT = math.sqrt(math.pow(pNuET+pLepET,2)-math.pow(pNuPx+pLepPx,2)-math.pow(pNuPy+pLepPy,2))
                
            solved, solvedt, pNuPz1, pNuPz2, pNuPz3, pNuPz4 = self.getNuMom(pWMass,mWT,pLepPx,pLepPy,pLepPz,pLepE,pNuPx,pNuPy)
            
            sol = []
            if solved: 
                sol.append(pNuPz1)
                sol.append(pNuPz2)
#            if solvedt:
#                sol.append(pNuPz3)
#                sol.append(pNuPz4)                

            for pNuPz in sol:
                        
                pNuE = math.sqrt(pNuPx*pNuPx+pNuPy*pNuPy+pNuPz*pNuPz)
                
                totPx = pLepPx+pNuPx+bjet.px
                totPy = pLepPy+pNuPy+bjet.py
                totPz = pLepPz+pNuPz+bjet.pz
                totE = pLepE+pNuE+bjet.E
                    
                pmW = math.pow(pNuE+pLepE,2)-math.pow(pNuPx+pLepPx,2)-math.pow(pNuPy+pLepPy,2)-math.pow(pNuPz+pLepPz,2)
                pmTop = totE*totE-totPx*totPx-totPy*totPy-totPz*totPz
                  
                if pmW > 0:
#                if mW > 0 and mTop > 0:
                    
                    pmW = math.sqrt(pmW)
                    pmTop = math.sqrt(pmTop)
                    
                    mWProb = self.getProb(self.hPDF['TopWM'][0],pmW)
#                    mTopProb = self.getProb(self.hPDF['TopM'][0],mTop)
                    
#                    if mWProb > 10E-10 and mTopProb > 10E-10:
                    if mWProb > 10E-10:
                        
                        lh = -2*math.log(mWProb)

                        if lh < lhMin:
                            
                            lhMin = lh
                            nuPz = pNuPz
                            mW = pmW
                            mTop = pmTop

        return lhMin, nuPz, mW, mTop
                
    
    
    
        
        
