from itertools import count
from ast import literal_eval

def day13(inp,part1=True):
    dat = literal_eval('{' + inp.rstrip().replace('\n',',') + '}')
    for d in count():
        costs = (k*v for k,v in dat.items() if ((k+d)%(2*(v-1)) if (k+d)%(2*(v-1)) < v else 2*(v-1) - (k+d)%(2*(v-1))) == 0)
        if part1:
            return sum(costs)
        try:
            next(costs)
        except StopIteration:
            return d

