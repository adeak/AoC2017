import numpy as np

def parseit(patt):
    """parse a string-valued input pattern and return a (2,2) or (3,3) binary array"""
    out = np.fromstring(patt.replace('.',' 0 ').replace('#',' 1 ').replace('/','\n'),sep=' ',dtype=int)
    return out.reshape(np.sqrt(out.size).round().astype(int),-1)

def genpatt(patt):
    """take a (2,2) or (3,3)-shaped binary pattern and generate all 8 orientations"""
    outlist = []
    for _ in range(2):
        for k in range(4):
            outlist.append(np.rot90(patt,k=k))
        patt = np.flipud(patt)
    return np.array(outlist) # shape (8,n,n)
    
def day21(inp,part1=True):
    """Raw numpy brute force"""
    s2s = [] # size 2s
    s3s = [] # size 3s
    for line in inp.rstrip().split('\n'):
        patfrom,patto = line.split(' => ')
        s = np.sqrt(len(patfrom.replace('/',''))).round().astype(int)
        stmp = s2s if s == 2 else s3s
        stmp.append((patfrom,patto))
    
    n2,n3 = len(s2s),len(s3s)
    # construct transformed pattern arrays: (n2,8,2,2) and (n3,8,3,3) complete with rotations
    # construct single output arrays: (n2,3,3) and (n3,4,4)
    for i,inlst in enumerate([s2s,s3s]):
        templst = []
        outlst = []
        for patfrom,patto in inlst:
            templst.append(genpatt(parseit(patfrom)))
            outlst.append(parseit(patto))
        temparr = np.array(templst)
        outarr = np.array(outlst)
        if i == 0:
            templates2 = temparr
            outs2 = outarr
        else:
            templates3 = temparr
            outs3 = outarr
            
    state = parseit('.#./..#/###')
    numsteps = 5 if part1 else 18
    for _ in range(numsteps):
        if state.shape[0]%2 == 0:
            n = 2 # size of chunks
            templates = templates2
            outs = outs2
        else:
            n = 3
            templates = templates3
            outs = outs3
        m = state.shape[0] // n # the number of chunks along a dimension
        state = state.reshape(m,n,m,n).transpose(0,2,1,3).reshape(-1,n,n) # (m*m,n,n)-shaped board

        # find a match for each chunk: broadcast (m*m,1,1,n,n) vs (l,8,n,n)
        inds = (state[:,None,None,...] == templates).reshape(m**2,-1,8,n**2).all(-1).any(-1).nonzero() # nonzeros of shape (m*m,l), and for each m1m2 there should be exactly one l
        
        # construct output state, shape (m*(n+1),m*(n+1))
        state = outs[inds[-1],...].reshape(m,m,n+1,n+1).transpose(0,2,1,3).reshape(m*(n+1),m*(n+1))

    return state.sum()

