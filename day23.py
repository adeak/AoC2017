def day23(inp,part1=True):
    instrs = [line.split() for line in inp.rstrip().split('\n')]
    regs = dict(zip('abcdefgh',[0]*8))
    if not part1:
        regs['a'] = 1
    last = None
    pos = 0
    muls = 0
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

        if mode == 'set':
            regs[op1] = val
        elif mode == 'sub':
            regs[op1] -= val
        elif mode == 'mul':
            regs[op1] *= val
            muls += 1
        elif mode == 'jnz':
            if specop1 != 0:
                pos += val
                continue
        pos += 1

    return muls if part1 else regs['h']

# part 2:

#  0 set b 84              # b = 84
#  1 set c b               # c = b = 84
#  2 jnz a 2               # if debug mode: 
#  3 jnz 1 5               #
#  4 mul b 100             #     b = 84*100
#  5 sub b -100000         #     b = 84*100 + 100000
#  6 set c b               #     c = b = 84*100 + 100000 = 108400
#  7 sub c -17000          #     c = 84*100 + 100000 + 17000 = 125400
                           #     d = e = f = g = h = 0

                           # while True:
#  8 set f 1               #     f = 1
#  9 set d 2               #     d = 2
                           #     do:
# 10 set e 2               #         e = 2
                           #         do:
# 11 set g d               #             g = d
# 12 mul g e               #             g *= e
# 13 sub g b               #             g -= b
# 14 jnz g 2               #             if g == 0:
# 15 set f 0               #                  f = 0
# 16 sub e -1              #             e += 1
# 17 set g e               #             g = e
# 18 sub g b               #             g -= b
# 19 jnz g -8              #         while g != 0
# 20 sub d -1              #         d += 1
# 21 set g d               #         g = d
# 22 sub g b               #         g -= b
# 23 jnz g -13             #     while g != 0
# 24 jnz f 2               #     if f == 0:
# 25 sub h -1              #         h += 1
# 26 set g b               #     g = b
# 27 sub g c               #     g -= c
# 28 jnz g 2               #     if g == 0:
# 29 jnz 1 3               #         return h
# 30 sub b -17             #     b += 17
# 31 jnz 1 -23             #

def day23b():
    """Execute manually optimized input code"""
    a = 1
    b = 108400
    c = 125400
    d = e = f = g = h = 0
                           
    while True:
        f = 1
        d = 2
    
        first = True
        while first or g != 0:
            if first: first = False

            if any(dd!=0 and 0 in range(dd*2-b,dd*(b+1)-b+1,dd) for dd in range(d,b)):
                f = 0
            d = b
            g = 0
        
        if f == 0:
            # 0 this is only where h changes value
            h += 1
        g = b - c
        if g == 0:
            return h
        b += 17

