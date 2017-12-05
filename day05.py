def day05(inp,part1=True):
    vals = list(map(int,inp.rstrip().split()))
    ind = steps = 0
    while True:
        delta = vals[ind]
        vals[ind] += 1 if part1 or vals[ind] <= 2 else -1
        ind += delta
        steps += 1
        if not 0 <= ind < len(vals):
            return steps

