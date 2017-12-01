def day1(inp):
    return sum(int(c1) for c1,c2 in zip(inp,inp[1:]+inp[0]) if c1==c2)

def day1b(inp):
    return sum(int(c1) for c1,c2 in zip(inp,inp[len(inp)//2:]+inp[:len(inp)//2]) if c1==c2)

