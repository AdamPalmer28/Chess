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


# %% king analysis
    def king_analysis(self,start,attack=False,check_move=False):
        # checks king safety and possible attacks
        
        row = start // 8
        col = start % 8
        check = {} # pieces giving check and moves too block
        
        if attack: # for calc attacking checks
            defend_bb = self.opponent_bb
            attack_bb = self.primary_bb
        else: # for calc defending checks
            defend_bb = self.primary_bb
            attack_bb = self.opponent_bb
          
        defend_occ = np.zeros(64,dtype='byte') # defence occupancy
        for ind, bb in enumerate(defend_bb):
            if ind == 5: # king bb
                continue
            defend_occ = np.bitwise_or(defend_occ,bb)
        attack_occ = np.zeros(64,dtype='byte') # attack occupancy
        for bb in attack_bb:
            attack_occ = np.bitwise_or(attack_occ,bb)
            
        all_occ = np.bitwise_or(attack_occ,defend_occ) # all occupancy
        
        
        
        direct_kn = np.zeros(64,dtype='byte')
        
        # knight squares
        def knight_attacks():
            knight_jumps = [-17,-15,-10,-6,6,10,15,17]
            if row in [1,6]:# one square away (north & south)
                if row == 1: # south
                    knight_jumps = [j for j in knight_jumps if j not in [-17,-15]]
                else:           # north
                    knight_jumps = [j for j in knight_jumps if j not in [15,17]]
                    
            elif row in [0,7]:# edge of board (north & south) 
                if row == 0: # south
                    knight_jumps = [j for j in knight_jumps if j not in [-17,-15,-10,-6]]
                else:           # north   
                    knight_jumps = [j for j in knight_jumps if j not in [17,15,10,6]]
    
            if col in [1,6]: # one square away (east & west)
                if col == 1:  # west
                    knight_jumps = [j for j in knight_jumps if j not in [6,-10]]
                else:           # east
                    knight_jumps = [j for j in knight_jumps if j not in [10,-6]]
                    
            elif col in [0,7]: # edge of board (east & west)
                if col == 0:  # west
                    knight_jumps = [j for j in knight_jumps if j not in [-17,-10,6,15]]
                else:           # east
                    knight_jumps = [j for j in knight_jumps if j not in [-15,-6,10,17]]
            
            for j in knight_jumps:
                direct_kn[start+j] = 1
        knight_attacks()  
        
        knight_attacks = np.bitwise_and(attack_bb[1],direct_kn).nonzero()[0]
        if len(knight_attacks)!=0:
            check[knight_attacks[0]]=[knight_attacks[0]]
            
        # horizontal / vertical & diagonal attacks
        def king_hv_diag_loop(slider_dict):
            direct_squares = np.zeros(64,dtype='byte')
            hidden_squares = np.zeros(64,dtype='byte')
            pinned_pieces  = {}
            if 1 in slider_dict: # rook / queen
                attack_bb_index = [3,4]
            else: # bishop / queen
                attack_bb_index = [2,4]
            
            for s, (fwd,back) in slider_dict.items():
                
                # === Forwards loop === 
                fwd_friendly, fwd_blocker, squares = [],[],[]
                for x in range(fwd): # forward
                    ind = start + (x+1)*s 
                    squares.append(ind)
                    # direct and hidden attacks
                    if (len(fwd_friendly) == 0 or len(fwd_blocker) == 0):
                        direct_squares[ind] = 1
                    else:
                        hidden_squares[ind] = 1
                        
                    
                    if defend_occ[ind] == 1: # defending pieces 
                        fwd_friendly.append(ind)
                    else: # attacking pieces
                        for i in attack_bb_index: 
                            if attack_bb[i][ind] == 1: # rook / bishop / queen in line
                                if len(fwd_blocker) == 0:
                                    if len(fwd_friendly) == 1: # i.e. pinned
                                        pinned_pieces[fwd_friendly[0]] = [i for i in squares]
                                        
                                    elif len(fwd_friendly) == 0: # direct attack
                                        check[ind] = list(squares)
                                
                    if attack_occ[ind] == 1: # blocking pieces 
                        fwd_blocker.append(ind) 
                    
                # === Backwards loop ===
                back_friendly, back_blocker, squares = [],[],[]
                for x in range(back): 
                    ind = start - (x+1)*s 
                    squares.append(ind)
                    # direct and hidden attacks
                    if (len(back_friendly) == 0 or len(back_blocker) == 0):
                        direct_squares[ind] = 1
                    else:
                        hidden_squares[ind] = 1
                        
                    if defend_occ[ind] == 1: # defending pieces 
                        back_friendly.append(ind)
                    
                    else: # attacking pieces
                        for i in attack_bb_index: 
                            if attack_bb[i][ind] == 1: # rook / bishop / queen in line
                                if len(back_blocker) == 0:
                                    if len(back_friendly) == 1: # i.e. pinned
                                        pinned_pieces[back_friendly[0]] = [i for i in squares]
                                        
                                    elif len(back_friendly) == 0: # direct attack
                                        check[ind] = list(squares)
                                        
                    if attack_occ[ind] == 1: # blocking pieces 
                        back_blocker.append(ind) 
                        
            return direct_squares, hidden_squares, pinned_pieces
                    
        def pawn_attacks():
            # maybe a better place to put this?
            col_con = (1 if self.w_to_move else -1)*(-1 if attack else 1)
            for i in [7,9]:
                ind = start + i*col_con
                
                # edge of board
                if (start % 8 == 7) & (ind % 8 != 6):
                    continue
                if (start % 8 == 0) & (ind % 8 != 1):
                    continue
                if start // 8 == 3.5 + 3.5*col_con:
                    continue
                
                if attack_bb[0][ind] == 1:
                    check[ind] = [ind]
        
        pawn_attacks()
        
        direct_hv, hidden_hv, pinned_hv = king_hv_diag_loop({1:(7-col,col),8:(7-row,row)})
            
        direct_d, hidden_d, pinned_d = king_hv_diag_loop({7:(min(7-row,col),min(row,7-col)),9:(min(7-row,7-col),min(row,col))})
        
        
        if check_move:
            if len(check) > 0: # move would be in check
                return False 
            else:
                return True
        else:
            return direct_hv, hidden_hv, pinned_hv, direct_d, hidden_d, pinned_d, direct_kn, check 
    
# %% king moves   


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



