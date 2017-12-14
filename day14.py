from collections import deque
import functools
import operator
from scipy.ndimage.measurements import label

def knothash(inp):
    iters = 64
    if isinstance(inp,str):
        inp = inp.encode('ascii')
    lengths = inp + bytes([17, 31, 73, 47, 23])

    rotback = skip = 0
    nums = deque(range(256))
    for _ in range(iters):
        for l in lengths:
            # pop off, put back
            rev = [nums.popleft() for _ in range(l)]
            nums.extendleft(rev)
            nums.rotate(-l-skip)
            rotback += l + skip
            skip += 1

    # rotate back to canonical position
    nums.rotate(rotback)

    # part 2: compute dense hash -> hex hash
    dense = [functools.reduce(operator.xor,batch) for batch in zip(*[iter(nums)]*16)]
    return dense # return list of ints for simplicity

def day14(inp):
    hashes = [knothash(f'{inp}-{k}') for k in range(128)]
    tot = sum(f'{h:b}'.count('1') for hsh in hashes for h in hsh)
    bins = [[int(c) for h in hsh for c in f'{h:08b}'] for hsh in hashes]

    regions,num_regions = label(bins)
    return tot,num_regions

