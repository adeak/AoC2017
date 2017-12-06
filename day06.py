import numpy as np
from itertools import count

def day06(inp):                                             
    # return part1,part2
    blocks = np.fromstring(inp, sep=' ', dtype=np.int64)
    seens = {tuple(blocks): 0}
    for step in count(1):
        ind = blocks.argmax()
        val = blocks[ind]
        blocks[ind] = 0
        np.add.at(blocks, np.arange(ind+1,ind+1+val) % blocks.size, 1)
        if tuple(blocks) in seens:
            return step,step-seens[tuple(blocks)]
        seens[tuple(blocks)] = step

