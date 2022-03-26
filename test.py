# test


#%% Properties
import time
import numpy as np

def test_timer(func):
    power = 4
    def wrapper(*args):
        before = time.time()
        for _ in range(10**power):
            val = func(*args)
        print("Function ran {} took: {} seconds".format(10**power,np.round(time.time() - before,4)))
        return val
    return wrapper


def timer(func):
    def wrapper(*args):
        before = time.time()
        val = func(*args)
        print("Function took:", np.round(time.time() - before,4), " seconds")
        return val
    return wrapper

@test_timer
def test_run(p):
    sum_val = 0
    for i in range(10**p+1):
        sum_val += i
    return sum_val

#print(test_run(2))


# %% moves ray


# %% Board space?
from evaluation.board_sections import board_divide as bd
board = bd()

bb = np.zeros(64,dtype='byte')
bb[14],bb[17],bb[24],bb[31],bb[13],bb[27],bb[28],bb[25],bb[19],bb[34] = 1,1,1,1,1,1,1,1,1,1
print(bb.reshape(8,8)[::-1,],'\n')

def board_space(occ,white):
    "Simple board space calculator"
    space_bb = np.zeros(64,dtype='byte')
    
    fn = max if white else min
    prev_col = fn(np.bitwise_and(occ,board.col[0]).nonzero()[0])
    
    for i in range(8):
        max_col = fn(np.bitwise_and(occ,board.col[i]).nonzero()[0])
        row_col = max_col // 8
        if abs(row_col - prev_col) > 1:
            # Not finished
            pass
        
        
        prev_col = row_col
        
        space_bb[max_col] = 1
    return space_bb

print(board_space(bb,True).reshape(8,8)[::-1,])
# %% move list
def ind_to_square(index):
    letter = ['A','B','C','D','E','F','G','H']
    square = letter[index % 8] + str((index // 8) +1)
    return square



