from collections import deque

def day16(inp,part1=True):
    d = deque((chr(o) for o in range(ord('a'),ord('p')+1)))
    numiter = 1 if part1 else int(1e9)

    # watch and hope for cycles...
    seen = set()
    states = []
    for it1 in range(numiter):
        for step in inp.rstrip().split(','):
            form,val = step[0],step[1:]
            if form == 's':
                d.rotate(int(val))
                continue
            vals = val.split('/')
            if form == 'x':
                pos1,pos2 = map(int,vals)
            else:
                pos1 = d.index(vals[0])
                pos2 = d.index(vals[1])
            d[pos1],d[pos2] = d[pos2],d[pos1]

        state = ''.join(d)
        if part1:
            return state
        if state in seen:
            break

        # otherwise it's a new state
        seen.add(state) # for quick membership
        states.append(state) # for getting a quick final answer
    else:
     return state
    # here: we've found a cycle \o/

    it0 = states.index(state)
    # numiter = it0 + n*(it1-it0) + rest plus an off-by-one error
    rest = (numiter - it0) % (it1 - it0)
    finalind = (it0 + rest) % len(states) - 1

    return states[finalind]

