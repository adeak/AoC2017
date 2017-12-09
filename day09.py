import re

def nester(patt,level):
    """Recursively parse nested group structure and return score"""
    # assume opening and closing parens
    nextlevel = patt[1:-1]
    if not nextlevel:
        # we're out of levels here
        return level
    # need to find our children and sum their weights
    numdiff = last = 0
    partsum = level
    for i,c in enumerate(nextlevel):
        if c == '{':
            numdiff += 1
        elif c == '}':
            numdiff -= 1
        if numdiff == 0:
            # we've got a complete group
            partsum += nester(nextlevel[last:i+1],level+1)
            last = i + 1
    return partsum

def day09(inp):
    commenter = re.compile('!.')
    cleaner = re.compile('<[^>]*>')

    inp = commenter.sub('',inp) # decomment
    garbagechars = sum(hit.span()[1]-hit.span()[0]-2 for hit in re.finditer(cleaner,inp)) # count garbage
    inp = cleaner.sub('',inp).replace(',','') # defluff
    
    # return score and number of garbage characters
    return nester(inp,1),garbagechars
    
