from collections import deque
import functools
import operator
import codecs

def day10(inp,part1=True):
    if part1:
        iters = 1
        lengths = map(int,inp.strip().split(','))
    else:
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
    if part1:
        # compute product of first two numbers
        return nums[0]*nums[1]

    # part 2: compute dense hash -> hex hash
    dense = [functools.reduce(operator.xor,batch) for batch in zip(*[iter(nums)]*16)]
    return codecs.encode(bytes(dense),'hex')
    
