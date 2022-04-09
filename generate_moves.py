import numpy as np
import itertools


class moves():
    """ 
    Identifies all moves avaliable to the side
    Will need to optimise 
    
    Inputs:
        > W and B bitboards (split inputs for ease? (Process pre/post __init__? is very easy))
        > Whos move (w/b)?
        > Last move - check en passent
        > Board state attributes (e.g w_K_castling = True)
      
    Outputs:
        > Dict - key = int (start pos), value = list/tuple (all legal moves)
        > Special information e.g. castle? en passent?
        
        
        
    Questions:
        > Should it include a legal move check?  (yes?)
        > Extra functions for special moves:
            > en passent
            > castling
    
    """
    def __init__(self, white_bb, black_bb, w_to_move,en_pas,castle_rights):
        # legal moves
        
        
        self.blockers = np.zeros(64,dtype='byte')
        self.opp_pieces = np.zeros(64,dtype='byte')
        self.w_to_move = w_to_move
        self.next_en_passant = [] # possible moves cause en_passant next move
        self.en_pass = en_pas
        
        if w_to_move: # sets primary and secondary bb
            self.primary_bb = white_bb
            self.opponent_bb = black_bb
        else:
            self.primary_bb = black_bb
            self.opponent_bb = white_bb
        
        # king position
        self.primary_king = self.primary_bb[5].nonzero()[0][0]
        self.opponent_king = self.opponent_bb[5].nonzero()[0][0]
        
    
        # side's pieces - i.e. blockers
        for bb in self.primary_bb:
            self.blockers = np.bitwise_or(self.blockers,bb)
        # opponent's pieces - i.e. possible captures
        for bb in self.opponent_bb:
            self.opp_pieces = np.bitwise_or(self.opp_pieces,bb)
        # all pieces - occupancy
        self.occupancy = np.bitwise_or(self.blockers,self.opp_pieces)
        
        self.castle_rights = castle_rights
        
        self.pawn_moves, self.pawn_captures, self.pos_en_passant_cap, self.promotion_moves = self.gen_pawn_moves(self.primary_bb[0])
        self.rook_moves, self.rook_captures = self.gen_rook_moves(self.primary_bb[3])
        self.bishop_moves, self.bishop_captures = self.gen_bishop_moves(self.primary_bb[2])
        self.knight_moves, self.knight_captures = self.gen_knight_moves(self.primary_bb[1])
        self.queen_moves, self.queen_captures = self.gen_queen_moves(self.primary_bb[4])
        
        
        self.direct_hv, self.hidden_hv, self.pinned_hv, self.direct_d, \
            self.hidden_d, self.pinned_d, self.direct_kn, self.check = self.king_analysis(self.primary_king,attack=False)
        
        self.basic_king_moves, self.king_moves, self.king_captures = self.gen_king_moves(self.castle_rights)
        
        # holds all moves
        self.all_moves = {**self.pawn_moves,**self.rook_moves,**self.bishop_moves,
                          **self.knight_moves,**self.queen_moves,**self.king_moves}
        # captures
        self.all_captures = {**self.pawn_captures,**self.rook_captures,**self.bishop_captures,
                          **self.knight_captures,**self.queen_captures,**self.king_captures}
        
        # pinned pieces
        for p, pinned_squares in {**self.pinned_d,**self.pinned_hv}.items():
            pinned_squares = set(pinned_squares)
            self.all_moves[p] = list(pinned_squares.intersection(self.all_moves[p]))
            self.all_captures[p] = list(pinned_squares.intersection(self.all_captures[p]))
            
        # CAN DEFINITELY BE IMPROVED
        if len(self.check) > 0: # in check 

            if len(self.check) > 1: # double check
            
                self.all_moves = self.basic_king_moves
                
            for key,list_value in (self.check).items():
                squares_set = set(list_value)
    
                for p, moves in (self.all_moves).items():
                    if p == self.primary_king:
                        continue
                    else:
                        self.all_moves[p] = list(squares_set.intersection(moves))
        
            if any(self.all_moves.values()):
                # CHECK
                pass
                
            else:
                # CHECKMATES
                pass
                    
        
    def sliding(self,start,direction): 
        """
        start: start index square
        direction: list: values - [8,1,7,9]
            8: Up - Down
            1: Left - Right
            7: Top_left - Bottom ight
            9: Bottom left - Top right
        """
        row = start // 8
        col = start % 8
        possible_moves = np.zeros(64,dtype='byte')
        def range_loop(fwd,back,s,move):
            for x in range(fwd): # forwards
                ind = start + (x+1)*s
                if self.blockers[ind] == 1:
                    break
                move[ind] = 1
                if self.opp_pieces[ind]==1:
                    break
                
            for x in range(back): # backwards
                ind = start - (x+1)*s
                if self.blockers[ind] == 1:
                    break
                move[ind] = 1
                if self.opp_pieces[ind]==1:
                    break
            return move
        
        
        for slide_change in direction:
            
            if slide_change == 8 : # vertical movement
            
                possible_moves = range_loop(7-row,row,slide_change,possible_moves) 
                
            elif slide_change == 1 : # horizoal movement
            
                possible_moves = range_loop(7-col,col,slide_change,possible_moves) 
                
            elif slide_change == 7 : # top left to bot right
            
                fwd_v = min(7-row,col) # fwd range value
                back_v = min(row,7-col) # back range value
                possible_moves = range_loop(fwd_v,back_v,slide_change,possible_moves) 
                
            elif slide_change == 9 : # top right to bot left  
            
                fwd_v = min(7-row,7-col) # fwd range value
                back_v = min(row,col) # back range value
                possible_moves = range_loop(fwd_v,back_v,slide_change,possible_moves) 
                
                
        possible_moves = np.bitwise_and(possible_moves,1-self.blockers)
        captures = np.bitwise_and(possible_moves,self.opp_pieces)
        return possible_moves, captures
        
    
    # Generation function for all pieces
    
    def gen_pawn_moves(self,pawn_bb):
        moves = {}
        captures = {}
        pos_en_passant_cap = {}
        pos_promotion = {}
        possible_moves = np.zeros(64,dtype='byte')
            
        
        
        def promotions():
            # promote on final rank
            final_rank = 3.5+3.5*col_con # rank of pawn promotion
            pass
        
        col_con = (1 if self.w_to_move else -1)
        pos_cap = np.array([9,7])
        for i in pawn_bb.nonzero()[0]: # for each piece
            p_move = []
            capture = []
            promotion = []
            # move forward
            fwd_1 = i + col_con*8
            if self.occupancy[fwd_1] == 0:
                p_move.append(fwd_1)
                possible_moves[fwd_1] = 1 # 1 square forward
            
                if i // 8 == 3.5 - 2.5*col_con: # check starting square 
                    fwd_2 = i + col_con*8*2
                    if self.occupancy[fwd_2] == 0:
                        p_move.append(fwd_2)
                        possible_moves[fwd_2] = 1 # 2 possible 
                        self.next_en_passant.append((i,fwd_2))
                        
                elif fwd_1 // 8 == 3.5 + 3.5*col_con: # check final rank
                    promotion.append(fwd_1)
                    
                        
            # captures 
            def get_captures():
                
                def en_passant(diag):
                    if (self.opp_pieces[diag] == 0):
                            p_move.append(diag)
                            capture.append(diag)
                            pos_en_passant_cap[i] = diag
                
                # normal captures
                if i % 8 in [0,7]: # edge of board: 
                    
                    if i % 8 == 0:
                        diag = i + col_con*(8 + col_con)
                    else:
                        diag = i + col_con*(8 - col_con)
                        
                    if self.opp_pieces[diag] == 1: # if capature is possible
                            p_move.append(diag)
                            capture.append(diag)
                            if diag // 8 == 3.5 + 3.5*col_con: # check final rank
                                promotion.append(diag)
                                
                    if (diag - 8*col_con == self.en_pass): # en passant
                            en_passant(diag)
                else: # middle of board
                    for diag in pos_cap:
                        diag = i + diag*col_con
                        if self.opp_pieces[diag] == 1: # capture is possible
                            p_move.append(diag)
                            capture.append(diag)
                            if diag // 8 == 3.5 + 3.5*col_con: # check final rank
                                promotion.append(diag)
                        if (diag - 8*col_con == self.en_pass):
                            en_passant(diag)

                    
                
                
            get_captures() # find captures
         
            
            moves[i] = p_move # adds moves to list of possible moves
            captures[i] = capture
            pos_promotion[i] = promotion 
            
            
        return moves, captures, pos_en_passant_cap, pos_promotion
    
    def gen_rook_moves(self,rook_bb):
        moves = {}
        captures = {}
        for p in rook_bb.nonzero()[0]:
            possible_moves, capture_moves = self.sliding(p,[1,8])
            
            moves[p] = possible_moves.nonzero()[0]
            captures[p] = capture_moves.nonzero()[0]
        return moves, captures
     
    def gen_bishop_moves(self,bishop_bb):
        moves = {}
        captures = {}
        for p in bishop_bb.nonzero()[0]:
            possible_moves, capture_moves = self.sliding(p,[7,9])
            
            moves[p] = possible_moves.nonzero()[0]
            captures[p] = capture_moves.nonzero()[0]
        return moves , captures
    
    def gen_knight_moves(self,knight_bb):
        moves = {}
        captures = {}
        for i in knight_bb.nonzero()[0]:
            possible_moves = np.zeros(64,dtype='byte')
            
            knight_jumps = [-17,-15,-10,-6,6,10,15,17] # index jumps of knights
            
            if i // 8 in [1,6]:# one square away (north & south)
                if i // 8 == 1: # south
                    knight_jumps = [j for j in knight_jumps if j not in [-17,-15]]
                else:           # north
                    knight_jumps = [j for j in knight_jumps if j not in [15,17]]
                    
            elif i // 8 in [0,7]:# edge of board (north & south) 
                if i // 8 == 0: # south
                    knight_jumps = [j for j in knight_jumps if j not in [-17,-15,-10,-6]]
                else:           # north   
                    knight_jumps = [j for j in knight_jumps if j not in [17,15,10,6]]

            if i % 8 in [1,6]: # one square away (east & west)
                if i % 8 == 1:  # west
                    knight_jumps = [j for j in knight_jumps if j not in [6,-10]]
                else:           # east
                    knight_jumps = [j for j in knight_jumps if j not in [10,-6]]
                    
            elif i % 8 in [0,7]: # edge of board (east & west)
                if i % 8 == 0:  # west
                    knight_jumps = [j for j in knight_jumps if j not in [-17,-10,6,15]]
                else:           # east
                    knight_jumps = [j for j in knight_jumps if j not in [-15,-6,10,17]]
                    
            
            for j in knight_jumps:
                possible_moves[i+j] = 1
                
            possible_moves = np.bitwise_and(possible_moves,1-self.blockers)
            possible_captures = np.bitwise_and(possible_moves,self.opp_pieces)
            moves[i] = possible_moves.nonzero()[0]
            captures[i] = possible_captures.nonzero()[0]
        return moves, captures
    
    def gen_queen_moves(self,queen_bb):
        moves = {}
        captures = {}
        for p in queen_bb.nonzero()[0]:
            possible_moves, capture_moves = self.sliding(p,[1,8,7,9])
            
            moves[p] = possible_moves.nonzero()[0]
            captures[p] = capture_moves.nonzero()[0]
        return moves , captures
    
    
    
    def gen_king_moves(self,castle_rights):
        # could make use of sliding to calculate legal moves?
        # blockers = same side pieces
        start = self.primary_king
        row = self.primary_king // 8
        col = self.primary_king % 8
        b_moves = {}
        moves = {}
        captures = {}
        
        p_moves = []
        p_captures = []
        
        if any(castle_rights) and (len(self.check) == 0):
            # castle moves generates
            if castle_rights[0]:
                # long castles
                k_end = start - 2
                #check = start - 3
                if all(self.occupancy[start-i] == 0 for i in range(1,4)):
                    # if self.king_analysis(start-1,attack=False,check_move=True) and \
                    #     self.king_analysis(start-2,attack=False,check_move=True):
                    if (self.king_move_check(start-1)) and (self.king_move_check(start-2)):
                        p_moves.append(k_end)

            if castle_rights[1]:
                # short castles
                k_end = start + 2
                #check = start + 2
                if all(self.occupancy[start+i] == 0 for i in range(1,3)):
                    # if self.king_analysis(start+1,attack=False,check_move=True) and \
                    #     self.king_analysis(start+2,attack=False,check_move=True):
                    if (self.king_move_check(start+1)) and (self.king_move_check(start+2)):
                        p_moves.append(k_end)
    
        
        # basic king moves
        basic_moves = [-1,-7,-8,-9,1,7,8,9]
        if row in [0,7]: # top or bottom of board
            if row == 0:
                basic_moves = [i for i in basic_moves if -i not in [7,8,9]]
            else:
                basic_moves = [i for i in basic_moves if i not in [7,8,9]]
        if col in [0,7]: # side of board 
            if col == 0:
                basic_moves = [i for i in basic_moves if -i not in [1,-7,9]]
            else:
                basic_moves = [i for i in basic_moves if i not in [1,-7,9]]
        
        
        
        for m in basic_moves:
            if self.blockers[start + m] == 0: # no friendly piece
                #if self.king_analysis(start+m,attack=False,check_move=True):
                if self.king_move_check(start+m):
                    # make sure kings don't touch
                    if (abs((start + m)//8 - self.opponent_king//8) <= 1) &  \
                        (abs((start + m)%8 - self.opponent_king%8) <= 1): 
                        continue 
                    if self.opp_pieces[start + m] == 1: # capture
                        p_captures.append(start + m)
                    p_moves.append(start + m) # move
              
        b_moves[start] = p_moves    
        moves[start] = p_moves 
        captures[start] = p_captures
        return b_moves ,moves , captures
    
    
    
    def king_analysis(self,start,attack=False):
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
        
        
        return direct_hv, hidden_hv, pinned_hv, direct_d, hidden_d, pinned_d, direct_kn, check 
    

    def king_move_check(self,start):
        row = start // 8
        col = start % 8
        
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
        
        # Possible knight attacks
        direct_kn = np.zeros(64,dtype='byte')
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
        
        if np.bitwise_and(attack_bb[1],direct_kn).sum() != 0:
            return False
            
        # horizontal / vertical & diagonal attacks
        def hvd_search(slider_dict):
            if 1 in slider_dict: # rook / queen
                attack_bb_index = [3,4]
            else: # bishop / queen
                attack_bb_index = [2,4]
            
            for s, (fwd,back) in slider_dict.items():
                
                # === Forwards loop === 
                for x in range(fwd): # forward
                    ind = start + (x+1)*s
                    
                    if defend_occ[ind] == 1: # defending pieces 
                        break
                    else: # attacking pieces
                        for i in attack_bb_index: 
                            if attack_bb[i][ind] == 1: # rook / bishop / queen in line
                                return False
                                
                    if attack_occ[ind] == 1: # blocking pieces 
                        break
                    
                # === Backwards loop ===
                for x in range(back): 
                    ind = start - (x+1)*s 
                    
                    if defend_occ[ind] == 1: # defending pieces 
                        break
                    
                    else: # attacking pieces
                        for i in attack_bb_index: 
                            if attack_bb[i][ind] == 1: # rook / bishop / queen in line
                                return False
                                        
                    if attack_occ[ind] == 1: # blocking pieces
                        break
            return True          
                    
        def pawn_attacks():
            # maybe a better place to put this?
            col_con = (1 if self.w_to_move else -1)
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
                    return False
            return True
        
        if not pawn_attacks():
            return False
        
        if not hvd_search({1:(7-col,col),8:(7-row,row)}):
            return False
        
        if not hvd_search({7:(min(7-row,col),min(row,7-col)),9:(min(7-row,7-col),min(row,col))}):
            return False
        
        return True
    
