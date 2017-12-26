from collections import defaultdict

def getend(line):
    dat = line.split()[-1][:-1]
    return int(dat) if dat.isdigit() else dat

def parser(inp):
    """Return initial state, number of steps and a dict with states as keys and [act_0,act_1] as values where act=[new_value,step,new_state]"""
    itinp = iter(inp.rstrip().split('\n'))
    init = getend(next(itinp))
    steps = int(next(itinp).split()[-2])
    blueprint = {}
    for line in itinp:
        if line.startswith('In state'):
            state = getend(line)
            # take values for value 0, then value 1
            acts = []
            for _ in range(2):
                next(itinp)
                act = [getend(next(itinp)) for _ in range(3)]
                act[1] = 1 if act[1] == 'right' else -1
                acts.append(act)
            blueprint[state] = acts
    return init,steps,blueprint

def day25(inp):
    state,numsteps,info = parser(inp)
    tape = defaultdict(int)
    pos = 0
    for _ in range(numsteps):
        val = tape[pos]
        tape[pos],delta,state = info[state][val]
        pos += delta
    return sum(tape.values())
