import numpy as np

def day02(inp):
    '''Compute checksum from file'''
    # rectangular cases are faster
    try:
        return np.loadtxt(inp).ptp(axis=1).sum()
    except ValueError:
        # this is probably just a test case
        return sum(np.fromstring(row,sep=' ').ptp() for row in open(inp).read().rstrip().split('\n'))

def day02b(inp):
    '''Compute part 2 checksum from filename'''
    dat = np.loadtxt(inp)

    # divide each pair of elements in each row, set diagonals to 0
    divs = dat[:,None,:]/dat[:,:,None]
    ran = range(divs.shape[1])
    divs[:,ran,ran] = 0
    inds = divs==divs.astype(int)

    return divs[inds].sum()
