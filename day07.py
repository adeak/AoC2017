import anytree as at
from operator import itemgetter
from collections import Counter

def day07(inp,part1=True):
    vertices = []
    nodes = {}
    for line in inp.rstrip().split('\n'):
        if '->' in line:
            vertices.append(line)
            line,_ = line.split(' -> ')

        name,dat = line.split()
        dat = int(dat[1:-1])
        nodes[name] = at.Node(name,data=dat)
    for line in vertices:
        head,tail = line.split(' -> ')
        parent,_ = head.split()
        children = tail.split(', ')
        for child in children:
            nodes[child].parent = nodes[parent]
    root = next(iter(nodes.values())).root
    if part1:
        return root.name

    # slow and iterative assessment of weights:
    while True:
        for elem in root.descendants:
            if elem.depth != root.height:
                continue
            parent = elem.parent
            children = parent.children
            if len({child.data for child in children}) == 1:
                # then this parent is balanced, kill children and accumulate weights
                parent.olddata = parent.data # sorry for the monkeypatch
                for child in children:
                    parent.data += child.data
                    child.parent = None

                # start again from the next deepest leaf level
                break

            # if we're here: unbalanced parent, need to find the guilty child
            namedweights = {child.data:child.name for child in children}                      # weight -> name inverse map
            weightcounts = Counter(child.data for child in children)                          # frequency of weights, least frequent is bad
            (badweight,_),(goodweight,_) = sorted(weightcounts.items(),key=itemgetter(1))[:2] # a bad and a good weight
            naughty = namedweights[badweight]                                                 # the naughty child that needs readjustment
            return nodes[naughty].olddata - (badweight-goodweight)

