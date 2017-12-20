import numpy as np
from scipy.optimize import minimize

def parse_inputs(inp):
    r = []
    v = []
    a = []
    for line in inp.rstrip().split('\n'):
        dats = line.split(', ')
        for lst,val in zip([r,v,a],dats):
            lst.append(list(map(int,val[3:-1].split(','))))
    r = np.array(r) # shape (N,3)
    v = np.array(v) # shape (N,3)
    a = np.array(a) # shape (N,3)

    return r,v,a

def day20(inp):
    """minimize analytical distances"""
    r,v,a = parse_inputs(inp)

    # in step n the position is r + n*v + n*(n+1)/2*a,
    # so we need to minimize this for every particle
    def getmindist(n,r,v,a):
        """compute the overall minimum distance in step n"""
        return np.abs(r + n*v + n*(n+1)/2*a).sum(axis=1).min()
    # try from various starting points to be sure
    mindist = np.inf
    for n0 in np.logspace(0,10):
        res = minimize(getmindist,n0,(r,v,a))
        dist = getmindist(res.x,r,v,a)
        if dist < mindist:
            nmin = res.x
    return np.abs(r + nmin*v + nmin*(nmin+1)/2*a).sum(axis=1).argmin()


def day20b(inp):
    """Find analytical collisions with masked arrays; slow but correct and guaranteed to give exact answer"""
    r,v,a = parse_inputs(inp)

    # particle position: pos0 + n*v0 + n*(n+1)/2*a -> quadratic equation for n
    # need to solve n^2*(a1-a2) + n*(2*(v1-v2) + (a1-a2)) + 2*(pos1-pos2) == [0,0,0] for smallest integer n for any pair of particles -> continue
    
    n0 = 0 # step of next collision
    for _ in np.arange(r.shape[0]//2+1): # at most nparticle/2 collisions
        N = r.shape[0]
        A = a[:,None,:] - a[None,:,:] # shape (N,N,3)
        B = 2*(v[:,None,:] - v[None,:,:]) + A # shape (N,N,3)
        C = 2*(r[:,None,:] - r[None,:,:])  # shape (N,N,3)

        D = B**2 - 4*A*C # discriminant
        # remove self-collisions and complex roots
        D[range(N),range(N),:] = -1
        inds = (D>=0).all(axis=-1)

        # remove complex or self-colliding solutions
        i1,i2 = inds.nonzero() # indices of real solutions
        A = np.ma.array(A[inds]) # shape (N',3)
        B = np.ma.array(B[inds]) # shape (N',3)
        C = np.ma.array(C[inds]) # shape (N',3)
        D = np.ma.array(D[inds]) # shape (N',3)

        # try to handle A==0 cases correctly...
        badinds = ((A == 0) & (B == 0) & (C != 0)).any(axis=-1) # these will never collide
        i1 = i1[~badinds]
        i2 = i2[~badinds]
        A = A[~badinds]
        B = B[~badinds]
        C = C[~badinds]
        D = D[~badinds]
        maskinds = (A == 0) & (B == 0) # & (C == 0);  these dimensions are trivial, ignore them later
        for arr in A,B,C,D:
            arr.mask |= maskinds

        def get_quadsol(A,B,D,n0):
            """return the smallest integer solution of A*n**2 + B*n + C == 0 larger than n0 if exists"""
            smallers = (-B-np.sqrt(D))/2/A
            goodsmalls = (smallers >= n0) & np.isclose(smallers,np.round(smallers))
            return np.where(goodsmalls,smallers,(-B+np.sqrt(D))/2/A)


        # if A == 0: linear equation
        lininds = (A == 0) & (B != 0)
        nsols = np.where(lininds,-C/B,get_quadsol(A,B,D,n0)) # shaped like A; non-solutions return large floats in general
        roundsols = np.ma.array(np.round(nsols),mask=A.mask,dtype=int)
        hits = (roundsols >= n0).all(axis=-1) & np.isclose(nsols,roundsols).all(axis=-1) # all integral steps; this is where the mask comes into play
        # make sure that those numbers are the same...
        # loop over the rows for checking uniqueness with the mask :( TODO?
        samensols = np.array([np.unique(row.compressed()).size == 1 for row in roundsols])
        truehits = hits & samensols
        if not truehits.any():
            # no more collisions
            return r.shape[0]

        # find the smallest n for the given collisions
        i1hit,i2hit,nsolhit = i1[truehits],i2[truehits],np.array([row.compressed()[0] for row in roundsols[truehits,:]]) # bah ugly listcomp again
        imin = nsolhit.argmin()
        nmin = nsolhit[imin]
        n0 = nmin
        dropinds = nsolhit == nmin  # colliding indices in i1hit,i2hit
        colliders = list(set(i1hit[dropinds]) | set(i2hit[dropinds])) # particle indices to remove for the rest of the simulation

        r = np.delete(r,list(colliders),axis=0)
        v = np.delete(v,list(colliders),axis=0)
        a = np.delete(a,list(colliders),axis=0)

        print(f'Culling {_}: size {r.shape}, n0={n0}')

    return r.shape[0]


def day20b_v2(inp,maxiter=10000):
    """simulate collisions step by step; fast but heuristic in terms of ending steps"""
    r,v,a = parse_inputs(inp)

    for k in range(maxiter): # maxiter is the heuristic...
        N = r.shape[0]
        allpos = r + k*v + k*(k+1)/2*a # shape (N,3)
        indcolls = (allpos == allpos[:,None,:]).all(axis=-1) # shape (N,N)
        indcolls[range(N),range(N)] = False # ignore self-collisions
        indcolls.nonzero() # whatever index collides
        colliders = np.unique(np.concatenate(indcolls.nonzero()))
        numcolls = len(colliders)
        if numcolls:
            r = np.delete(r,colliders,axis=0)
            v = np.delete(v,colliders,axis=0)
            a = np.delete(a,colliders,axis=0)
            print(f'particles left after {k} steps: {r.shape[0]}')

    return r.shape[0]
 
