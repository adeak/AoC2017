import numpy as np
from scipy.optimize import minimize
from itertools import combinations
from collections import defaultdict

def day20(inp):
    """minimize analytical distances"""
    r = []
    v = []
    a = []
    for line in inp.rstrip().split('\n'):
        dats = line.split(', ')
        for lst,val in zip([r,v,a],dats):
            lst.append(list(map(int,val[3:-1].split(','))))
    r = np.array(r)
    v = np.array(v)
    a = np.array(a)

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
    """Find analytical collisionsi with masked arrays; slow but correct and guaranteed to give exact answer"""
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

        #print(A.shape,B.shape,D.shape,lininds.shape,nsols.shape,roundsols.shape,truehits.shape)

#        nsols = np.concatenate([(-B+np.sqrt(D))/2/A,(-B-np.sqrt(D))/2/A])
#        # double i1,i2 for consistent indexing later
#        i1 = np.tile(i1,2)
#        i2 = np.tile(i2,2)
#        roundsols = np.round(nsols)
#        hits = (roundsols >= n0).all(axis=-1) & np.isclose(nsols,roundsols).all(axis=-1) # all integral steps
#        # make sure that those numbers are the same...
#        truehits = hits & (roundsols[:,0] == roundsols[:,1]) & (roundsols[:,1] == roundsols[:,2])

        # find the smallest n for the given collisions
        #i1hit,i2hit,nsolhit = i1[truehits],i2[truehits],roundsols[truehits,:].compressed()[0]
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


def day20bv2(inp):
    """Find analytical collisions loopily; slow and incorrect"""
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

    # particle position: pos0 + n*v0 + n*(n+1)/2*a -> quadratic equation for n
    # need to solve n^2*(a1-a2) + n*(2*(v1-v2) + (a1-a2)) + 2*(pos1-pos2) == [0,0,0] for smallest integer n for any pair of particles -> continue
    n0 = 0
    numcolls = 0
    for _ in range(r.shape[0]//2+1): # at most N/2 collisions
        N = r.shape[0]
        colls = defaultdict(set)
        for i1,i2 in combinations(range(N),2):
            A = a[i1,:] - a[i2,:]
            B = 2*(v[i1,:] - v[i2,:]) + A
            C = 2*(r[i1,:] - r[i2,:])

            # see if there's a collision
            ncols = []
            numnums = 3
            for AA,BB,CC in zip(A,B,C):
                if AA == 0:
                    if BB == 0:
                        # same initial acceleration and speed; irrelevant dimension if positions are the same too
                        numnums -= 1 # ignore this in the test later
                        continue
                        
                    # or BB != 0
                    ncol = -CC/BB
                    if np.isclose(ncol,np.round(ncol)) and ncol >= n0:
                        ncols.append(np.round(ncol))
                else:
                    # solve the quadratic equation
                    D = BB**2 - 4*AA*CC
                    if D < 0:
                        continue
                    term1,term2 = -BB/2/AA, np.sqrt(D)/2/AA
                    for n in term1-term2,term1+term2:
                        # use the earlier collision if there are multiple
                        if np.isclose(n,np.round(n)) and n >= n0:
                            ncols.append(np.round(n))
                            continue
            # collision if we have `numnums` equal values in ncols
            if len(ncols) == numnums and len(set(ncols)) == 1:
                colls[ncols[0]] = colls[ncols[0]].union({i1,i2}) # add i1,i2 as colliding nodes to colls

        if not len(colls):
            # no more collisions found
            return r.shape[0]

        nextcoll = min(colls) # next iteration where there's a collision
        n0 = nextcoll # start searching here for the rest
        colliders = list(colls[nextcoll]) # the current indices of the particles that will die

        # increment killcount, remove dead particles
        numcolls += len(colliders)
        r = np.delete(r,colliders,axis=0)
        v = np.delete(v,colliders,axis=0)
        a = np.delete(a,colliders,axis=0)

        print(f'Culling {_}: number of particles left is {r.shape[0]}')

def day20bv3(inp):
    """simulate collisions step by step; fast but heuristic in terms of ending steps"""
    r = []
    v = []
    a = []
    for line in inp.rstrip().split('\n'):
        dats = line.split(', ')
        for lst,val in zip([r,v,a],dats):
            lst.append(list(map(int,val[3:-1].split(','))))
    r = np.array(r)
    v = np.array(v)
    a = np.array(a)

    for k in range(1000000):
        N = r.shape[0]
        allpos = r + k*v + k*(k+1)/2*a # shape (N,3)
        indcolls = (allpos == allpos[:,None,:]).all(axis=-1) # shape (N,N)
        indcolls[range(N),range(N)] = False # ignore self-collisions
        indcolls.nonzero() # whatever index collides
        colliders = np.unique(np.concatenate(indcolls.nonzero()))
        numcolls = len(colliders)
        if numcolls:
            print(f'Found {numcolls} colliders in step {k}')
            r = np.delete(r,colliders,axis=0)
            v = np.delete(v,colliders,axis=0)
            a = np.delete(a,colliders,axis=0)
            print(f'Left: {r.shape[0]} particles')
    return r.shape[0]
 
