from operator import itemgetter

def day24(inp,part1=True):
    pipes = [list(map(int,row.split('/'))) for row in inp.rstrip().split('\n')]

    def builder(conn,pipes):
        """Get the length and strength of the largest-scoring subbridge recursively"""
        goods = [p for p in pipes if conn in p]
        maxdat = []
        for good in goods:
            tmpgood = good[:]
            tmpgood.remove(conn)
            other = tmpgood[0]
            rest = [p for p in pipes if set(p) != {conn,other}]
            maxlen,substrength = builder(other,rest)
            maxdat.append((maxlen+1,conn + other + substrength))
        if not maxdat:
            return (0,0) # (length,strength)
        maxlen = max(maxdat,key=itemgetter(0))[0]
        if part1:
            maxstr = max(dat[1] for dat in maxdat)
        else:
            maxstr = max(dat[1] for dat in maxdat if dat[0] == maxlen)
        return (maxlen,maxstr)

    return builder(0,pipes)[1]

