import numpy as np

def day19(inp):
    board = np.array(list(map(list,inp.rstrip('\n').split('\n'))),dtype='U1')
    #print(board,board.shape)
    i0 = (board[0,:] == '|').nonzero()[0][0]
    pos = np.array([0,i0])
    dir = np.array([1,0])
    ans = []
    steps = 0
    while True:
        # step first
        pos += dir
        steps += 1
        
        # check for exit
        if (not 0<=pos[0]<board.shape[0]) or (not 0<=pos[1]<board.shape[1]) or (board[tuple(pos)] == ' '):
            return ''.join(ans), steps
        
        # check for letter
        val = board[tuple(pos)]
        #print(val)
        if val.isalnum():
            ans.append(val)
        # check for direction change
        elif val == '+':
            if dir[1] == 0:
                # [1,0] or [-1,0] vertical before switch
                newdir_temp = np.array([0,1])
                goodval = '-'
            else:
                # [0,1] or [0,-1] horizontal before switch
                newdir_temp = np.array([1,0])
                goodval = '|'
            for fac in -1,1:
                newdir = fac*newdir_temp
                nextval = board[tuple(pos+newdir)]
                if nextval == goodval or nextval.isalnum():
                    dir = newdir
                    break
                    
        # else we should just keep on stepping

