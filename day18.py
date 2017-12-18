from collections import defaultdict,deque

def day18a(inp):
    instrs = [line.split() for line in inp.rstrip().split('\n')]
    regs = defaultdict(int)
    last = None
    pos = 0
    while pos < len(instrs):
        mode,op1,*op2 = instrs[pos]
        if len(op2):
            try:
                val = int(op2[0])
            except ValueError:
                val = regs[op2[0]]

        if mode == 'snd':
            last = regs[op1]
        elif mode == 'set':
            regs[op1] = val
        elif mode == 'add':
            regs[op1] += val
        elif mode == 'mul':
            regs[op1] *= val
        elif mode == 'mod':
            regs[op1] %= val
        elif mode == 'rcv':
            if regs[op1] == 0:
                pos += 1
                continue
            return last
        elif mode == 'jgz':
            if regs[op1] > 0:
                pos += val
                continue
        pos += 1
    return 'wtf'


def day18b(inp):
    """Pass a deque to the processes for queueing, append sent values here"""

    instrs = [line.split() for line in inp.rstrip().split('\n')]
    q0 = deque([])
    q1 = deque([])
    gen0 = gen(instrs,0,q0)
    gen1 = gen(instrs,1,q1)
    tot = 0
    while True:
        try:
            val0 = next(gen0)
            if val0 is not None:
                # 0 sends to 1
                q1.append(val0)
        except StopIteration:
            val0 = None
        # if val0 is None: 0 is waiting or ended

        # now the same for gen1 with counting
        try:
            val1 = next(gen1)
            if val1 is not None:
                # 1 sends to 0
                q0.append(val1)
                tot += 1 # count these for the answer
        except StopIteration:
            val1 = None
        # if val1 is None: 1 is waiting or ended

        # if neither are running: deadlock or both are finished
        if val0 is None and val1 is None:
            return tot

def gen(instrs,ID,q):
    """Generator implementing a process; yields an int on send or None while waiting"""

    regs = defaultdict(int)
    regs['p'] = ID
    pos = 0
    while pos < len(instrs):
        mode,op1,*op2 = instrs[pos]

        # convert op1 and op2 to ints if necessary
        try:
            # special-case int op1 input for snd and jgz
            specop1 = int(op1)
        except ValueError:
            specop1 = regs[op1]

        if len(op2):
            try:
                val = int(op2[0])
            except ValueError:
                val = regs[op2[0]]

        if mode == 'snd':
            yield specop1
        elif mode == 'set':
            regs[op1] = val
        elif mode == 'add':
            regs[op1] += val
        elif mode == 'mul':
            regs[op1] *= val
        elif mode == 'mod':
            regs[op1] %= val
        elif mode == 'jgz':
            if specop1 > 0:
                pos += val
                continue
        elif mode == 'rcv':
            while True:
                if len(q):
                    # receiving
                    regs[op1] = q.popleft()
                    break
                else:
                    # waiting
                    yield None
        pos += 1
