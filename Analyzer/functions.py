import utils

def overlap(eta,phi,ecol,drMax):
    
    passed = True
    drMin = 777
    
    for e in ecol:
        dr = utils.deltaR(eta,phi,e.eta,e.phi)
        if (dr < drMin): drMin = dr
    
    if (drMin < drMax):
        passed = False
        
    return passed, drMin
