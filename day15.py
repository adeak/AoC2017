def gen(init,mul,filt=1):
    val = init
    while True:
        val = val*mul % 2147483647
        if not val%filt:
            yield val

def day15(inp,part1=True):
    initA,initB = map(int,inp.split())
    mulA,mulB = 16807,48271
    filtA,filtB = (1,1) if part1 else (4,8)
    genA = gen(initA,mulA,filtA)
    genB = gen(initB,mulB,filtB)
    mask = 2**16 - 1
    hits = 0
    if part1:
        numiter = int(4e7)
    else:
        numiter = int(5e6)
    for _ in range(numiter):
        if next(genA) & mask == next(genB) & mask:
            hits += 1
    
    return hits

