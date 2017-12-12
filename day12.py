from collections import defaultdict

def day12(inp,part1=True):
     conns = defaultdict(set)
     for line in inp.rstrip().split('\n'):
         first,rest = line.split(' <-> ')
         for second in rest.split(', '):
             conns[first].add(second)
             conns[second].add(first)
     allpoints = set(conns.keys())
     groups = 0
     while len(allpoints):
         start = '0' if part1 else allpoints.pop()
         visited = set()
         check = {start}
         while len(check):
             checknow = check.pop()
             visited.add(checknow)
             for pair in conns[checknow]:
                 if pair in visited or pair in check:
                     continue
                 check.add(pair)
         if part1:
             return len(visited)
         allpoints -= visited
         groups += 1
 
     return groups
 
import numpy as np
def day12_matrix(inp,part1=True):
    """Use a transition matrix to explore the graph (hint: it's slow)"""
    inp = inp.rstrip().split('\n')
    n = len(inp)
    C = np.zeros((n,n),dtype=int)
    
    # build connectivity graph
    for line in inp:
         first,rest = line.split(' <-> ')
         i1 = int(first)
         i2s = list(map(int,rest.split(', ')))
         C[i1,i2s] = C[i2s,i1] = 1

    # we can walk the group in at most n-1 steps
    inits = list(range(n))[::-1] # ensure pop(0) for part 1
    groups = 0
    while len(inits):
        pos = np.zeros(len(inits),dtype=int)
        start = inits.pop()
        pos[start] = 1
        allpos = pos.copy()
        for k in range(n):
            pos = C @ pos
            allpos += pos

        if part1:
            group, = allpos.nonzero()
            return len(group)

        # for part 2 we can discard the visited nodes altogether
        keep = np.logical_not(allpos)
        C = C[np.ix_(keep,keep)]
        inits = list(range(C.shape[0]))

        groups += 1
        
    return groups
