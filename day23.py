from collections import defaultdict,deque

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

# only need h; starts from 0 and only instruction is `sub h -1` looped by final `jnz 1 -23`
# final is only skipped by `jnz 1 3` when the program ends
# ending is only skipped by `jnz g 2` -> loop as long as g!=0

#  0 set b 84              # b = 84
#  1 set c b               # c = b = 84
#  2 jnz a 2               # if debug mode: 
#  3 jnz 1 5               #
#  4 mul b 100             #     b = 84*100
#  5 sub b -100000         #     b = 84*100 + 100000
#  6 set c b               #     c = b = 84*100 + 100000
#  7 sub c -17000          #     c = 84*100 + 100000 + 17000

                           # setup:
                           # a = 1
                           # b = 108400
                           # c = 125400
                           # d = e = f = g = h = 0

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

###

# raw: 
def raw():
    a = 1
    b = 108400
    c = 125400
    d = e = f = g = h = 0
    
    while True:
        f = 1
        d = 2
        first1 = True
        while first1 or g != 0: # do-while
            if first1: first1 = False
            e = 2
            first2 = True
            while first2 or g != 0: # do-while
                if first2: first2 = False
                g = d
                g *= e
                g -= b
                if g == 0:
                     f = 0
                e += 1
                g = e
                g -= b
    
            d += 1
            g = d
            g -= b
    
        if f == 0:
            h += 1
        g = b
        g -= c
        if g == 0:
            return h
        b += 17


###

# optimized 0:
def opt0():
    a = 1
    b = 108400
    c = 125400
    d = e = f = g = h = 0
                           
    while True:
        f = 1
        d = 2
    
        first1 = True
        while first1 or g != 0:
            if first1: first1 = False
            e = 2
    
            first2 = True
            while first2 or g != 0:
                if first2: first2 = False
                # 3 if we entered here, previous g wasn't 0 or first iteration
                g = d*e - b
                # 2 if g was zero: d*e == b
                if g == 0:
                     # 1 this is only where f gets set from 1
                     f = 0
                # 5/1 if g = d*e - b was zero:
                e += 1
                g = e - b
                # 5/2 g = (d+1)*e_prev - b is only zero if e_prev == 0 and b == 0
                #     but then 
                # 4 e - b wasn't zero


                # (g!= 0)
                # g = d*e0 - b
                # if d*e0-b == 0: f=0
                # e = e0+1
                # g = e0 + 1 - b
                # if g==0==e0+1-b: break
                #
                # g = d*(e0+1) - b
                # if d*(e0+1)-b == 0: f=0
                # e = e0 + 2
                # g= ...
                # if e0 + 2 - b == 0: break
                # 
                # when it breaks: e = b; in last f-testing step e = b + 1
                # if d*e0-b == 0 or d*(e0+1)-b==0 or ... or d*(b+1) - b: f=0
        
            d += 1
            g = d - b
        
        if f == 0:
            # 0 this is only where h changes value
            h += 1
        g = b - c
        if g == 0:
            return h
        b += 17

# optimized 1:
def opt1():
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
            e = 2
    
    
            e0 = e
            e = b
            g = 0
            if d!=0 and 0 in range(d*e0-b,d*(b+1)-b+1,d):
                f = 0
    
            d += 1
            g = d - b
        
        if f == 0:
            # 0 this is only where h changes value
            h += 1
        g = b - c
        if g == 0:
            return h
        b += 17


# optimized 2:
def opt2():
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
    
            g = 0
            if d!=0 and 0 in range(d*2-b,d*(b+1)-b+1,d):
                f = 0

            d += 1
            g = d - b
        
        if f == 0:
            # 0 this is only where h changes value
            h += 1
        g = b - c
        if g == 0:
            return h
        b += 17


# optimized 3:
def opt3():
    a = 1
    b = 108400
    c = 125400
    d = e = f = g = h = 0
                           
    while True:
        f = 1
        d = 2
    
        # initially f=1, d=2, g=0, skip loop
        # f==0 -> h-= 1
        # g=b-c=-91600+108600
        # b-= 1
        # loop True, enter outer g loop
    
        first = True
        while first or g != 0:
            if first: first = False
    
            # g starts from -91600+108600
            # f maybe gets set to 0
            # d -= 1
            # g = d - b until g == 0
            # -> at exit d = b; g = 0
    
            if d!=0 and 0 in range(d*2-b,d*(b+1)-b+1,d):
                f = 0
    
            d += 1
            g = d - b
        
        if f == 0:
            # 0 this is only where h changes value
            h += 1
        g = b - c
        if g == 0:
            return h
        b += 17

        #e=b+17;print(a,b,c,d,e,f,g,h) # TODO

# optimized 4:
def opt4():
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

