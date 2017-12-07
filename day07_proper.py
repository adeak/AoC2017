from collections import Counter
from operator import itemgetter

class Node:
    def __init__(self,name,weight):
        self.name = name
        self.weight = weight
        self.parent = None
        self.children = []

    def get_root(self):
        """Find the root from a given node"""
        if self.parent is None:
            return self
        return self.parent.get_root()

    def get_cumweight(self):
        """Compute total weight of subtree below a given node"""
        if not self.children:
            return self.weight
        return self.weight + sum(child.get_cumweight() for child in self.children)

    def is_unstable(self):
        """Determine whether a given node is unstable"""
        return len({child.get_cumweight() for child in self.children}) != 1

    def find_instability(self):
        """Find the instability of a bad child node with the assumption that there's exactly 1 unstable"""
        if not self.children:
            # should never happen if we're calling this for the root node
            return None
        for child in self.children:
            if child.is_unstable():
                # then we're not the primary unstable one; we need to go deeper
                return child.find_instability()

        # find the least frequent weight and the other one
        namedweights = {child.name: child.get_cumweight() for child in self.children}
        weightfreq = Counter(namedweights.values())
        (badweight,_),(goodweight,_) = sorted(weightfreq.items(),key=itemgetter(1))[:2]
        for child in self.children:
            if namedweights[child.name] == badweight:
                return child, (badweight - goodweight)

def parse_inputs(inp):
    nodeinfo = []
    vertexinfo = {}
    for line in inp.rstrip().split('\n'):
        node,_,vert = line.partition(' -> ')

        # parse node-related info
        name,weight = node.split()
        weight = int(weight[1:-1])
        nodeinfo.append((name,weight))

        # parse vertex-related info if present
        if vert:
            children = vert.split(', ')
            vertexinfo[name] = children
    return nodeinfo,vertexinfo

def day07(inp,part1=True):
    nodeinfo,vertexinfo = parse_inputs(inp)

    # construct a tree from the input
    nodes = {}
    for name,weight in nodeinfo:
        nodes[name] = Node(name,weight)
    for parent,childnames in vertexinfo.items():
        nodes[parent].children = [nodes[childname] for childname in childnames]
        for childname in childnames:
            nodes[childname].parent = nodes[parent]

    # get the root
    root = nodes[parent].get_root()
    if part1:
        return root.name

    # get the instability
    badchild,instability = root.find_instability()
    return badchild.weight - instability
