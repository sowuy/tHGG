import utils
import math

def overlap(eta,phi,ecol,drMax):
    
    passed = True
    drMin = 777
    
    for e in ecol:
        dr = utils.deltaR(eta,phi,e.eta,e.phi)
        if (dr < drMin): drMin = dr
    
    if (drMin < drMax):
        passed = False
        
    return passed, drMin

def zveto(lep,ecol,mllZ,cut):
    
    passed = True
    diffMin = 777
    
    for e in ecol:
        mll = utils.mll(lep,e)
        diff = math.fabs(mllZ-mll)
        if (diff < diffMin): diffMin = diff
    
    if (diffMin < cut):
        passed = False
        
    return passed, diffMin
