import math

def deltaR2( e1, p1, e2, p2):

    de = e1 - e2
    dp = deltaPhi(p1, p2)
    return de*de + dp*dp
            
def deltaR( *args ):

    return math.sqrt( deltaR2(*args) )
                
def deltaPhi( p1, p2):

    res = p1 - p2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res

def mll ( p1, p2 ):

    p1Px = p1.pt*math.cos(p1.phi)
    p1Py = p1.pt*math.sin(p1.phi)
    p1Pz = p1.pt*math.sinh(p1.eta)
    
    p2Px = p2.pt*math.cos(p2.phi)
    p2Py = p2.pt*math.sin(p2.phi)
    p2Pz = p2.pt*math.sinh(p2.eta)

    res = math.pow(p1.E+p2.E,2)-math.pow(p1Px+p2Px,2)-math.pow(p1Py+p2Py,2)-math.pow(p1Pz+p2Pz,2)
    if res >= 0: res = math.sqrt(res)
    else: res = -1
    
    return res
    
