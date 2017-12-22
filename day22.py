from collections import defaultdict

def day22(inp,part1=True):
    lines = inp.rstrip().split('\n')
    nrows = len(lines)
    ncols = len(lines[0])
    # 0 is clean, 2 is sick
    board = defaultdict(int,{(-i,j):0 if c=='.' else 2 for i,line in enumerate(lines) for j,c in enumerate(line)})
    pos = -(nrows-1)//2,(ncols-1)//2
    dir = 1j
    infs = 0
    numsteps = 10000 if part1 else 10000000
    for step in range(numsteps):
        # 0: clean, 1: weakened, 2: infected, 3: flagged, 0->1->2->3->0
        if board[pos] == 0:
            dir *= 1j
        elif board[pos] == 2:
            dir *= -1j
        elif board[pos] == 3:
            dir *= -1

        if part1:
            # 0 -> 2 -> 0
            board[pos] = (board[pos]+2) % 4
        else:
            # full cycle
            board[pos] = (board[pos]+1) % 4

        if board[pos] == 2:
            # this has just been infected
            infs += 1

        pos = pos[0]+int(dir.imag),pos[1]+int(dir.real)

    return infs
