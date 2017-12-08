from collections import defaultdict
import operator as oper

def day08(inp):
    regs = defaultdict(lambda: 0)
    comps = {
        '==': oper.eq,
        '!=': oper.ne,
         '<': oper.lt,
        '<=': oper.le,
         '>': oper.gt,
        '>=': oper.ge,
    }
    ops = {
        'inc': oper.add,
        'dec': oper.sub,
    }
    maxval = 0
    for line in inp.rstrip().split('\n'):
        reg,op,val,_,cond1,comp,cond2 = line.split()
        val,cond2 = map(int,[val,cond2])
        if comps[comp](regs[cond1],cond2):
            regs[reg] = ops[op](regs[reg],val)
            maxval = max(maxval,regs[reg])
        
    return max(regs.values()),maxval

