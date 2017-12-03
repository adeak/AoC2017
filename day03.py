from itertools import cycle

def day03(inp):                    
    def stepgen():
        steps = 0
        for stepcount,dir in enumerate(cycle([(1,0),(0,1),(-1,0),(0,-1)])):
            if stepcount % 2 == 0:
                steps += 1
            for _ in range(steps):
                yield dir

    posx,posy = (0,0)
    stepper = stepgen()
    for i,newdir in enumerate(stepper,1):
        if i == inp:      
            return abs(posx)+abs(posy)
        posx += newdir[0]
        posy += newdir[1]                                                   

def day03b(inp):                   
    def stepgen():
        steps = 0
        for stepcount,dir in enumerate(cycle([(1,0),(0,1),(-1,0),(0,-1)])):
            if stepcount % 2 == 0:
                steps += 1
            for _ in range(steps):
                yield dir

    posx,posy = (0,0)
    stepper = stepgen()
    data = {(0,0): 1}
    for newdir in stepper:            
        posx += newdir[0]
        posy += newdir[1]                                                                                    
        val = sum(data.get((posx+dx,posy+dy),0) for dx,dy in [(1,0),(0,1),(-1,0),(0,-1),
                                                              (1,1),(-1,1),(1,-1),(-1,-1)])
        data[posx,posy] = val
        if val > inp:       
            return val

