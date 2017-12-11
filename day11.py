import numpy as np
from collections import Counter

def unitvec(phi):
    """Return 2d unitvector t angle phi in degrees"""
    return np.array([np.cos(phi/180*np.pi),np.sin(phi/180*np.pi)])

def finddist(pos):
    """Find the minimum number of steps needed to reach a point in a hexagonal grid"""
    # find nearest high-symmetry angle to step along for minimum distance
    angle = np.arctan2(pos[1],pos[0])/np.pi*180 # from -180 to 180
    search_angles = np.arange(-210,211,60) # to avoid jumps in angle later
    closest = np.abs(angle - search_angles).argmin()
    maindir = search_angles[closest]

    # construct adapted basis in order to find minimum coordinates
    a1 = unitvec(maindir)
    a2 = unitvec(maindir+60) if angle-maindir>0 else unitvec(maindir-60)
    
    # decompose pos on the basis of a1,a2
    coords = np.linalg.inv(np.array([a1,a2]).T) @ pos
    return np.round(coords.sum())

def day11(inp,part1=True):
    main_angles = np.linspace(90,90+360,6,False)
    dirs = dict(zip(['n','nw','sw','s','se','ne'],main_angles))
    pos = np.zeros(2)
    if part1:
        # no need to take each step once
        steps = Counter(inp.strip().split(','))
        for dir in steps:
            pos += steps[dir]*unitvec(dirs[dir])
        return finddist(pos)
    
    maxdist = 0
    for dir in inp.strip().split(','):
        pos += unitvec(dirs[dir])
        dist = finddist(pos)
        if dist > maxdist:
            maxdist = dist
    
    return maxdist
