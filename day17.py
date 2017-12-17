from collections import deque

def day17(inp,part1=True):
    # part2 is awfully brute force, see the separate smarter solution
    d = deque()
    maxind = 2017 if part1 else int(5e7)
    for k in range(maxind+1):
        d.rotate(-inp)
        d.append(k)
    if part1:
        return d[0]
    else:
        return d[d.index(0)+1]

def day17_smarterpart2(inp):
    maxind = int(5e7)
    pos = 0
    for k in range(1,maxind+1):
        pos += inp + 1
        pos %= k
        if pos == 0:
            ans = k
    return ans
