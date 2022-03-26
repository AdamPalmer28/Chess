"""
This class is responsible for storing all the information of the chess game

It will also be responsible for determining valid moves at the current state
It will also keep a move log
"""
import numpy as np

import generate_moves as gm

"""
Notes/ Plans:
===============================================================================    
    
> 'cProfile' and 'pstats' to act as performance evac tools of code


"""
import time
def timer(func):
    def wrapper(*args):
        before = time.time()
        func(*args)
        print("Function tooks:", np.round(time.time() - before,8), " seconds")  
    return wrapper

def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped

class game_state():        

    def __init__(self):
        
        # white
        self.w_pawns = np.zeros(64,dtype='byte')
        self.w_knight = np.zeros(64,dtype='byte')
        self.w_bishop = np.zeros(64,dtype='byte')
        self.w_rook = np.zeros(64,dtype='byte')
        self.w_queen = np.zeros(64,dtype='byte')
        self.w_king = np.zeros(64,dtype='byte')
        
        # black
        self.b_pawns = np.zeros(64,dtype='byte')
        self.b_knight = np.zeros(64,dtype='byte')
        self.b_bishop = np.zeros(64,dtype='byte')
        self.b_rook = np.zeros(64,dtype='byte')
        self.b_queen = np.zeros(64,dtype='byte')
        self.b_king = np.zeros(64,dtype='byte')

        
        self.white_bit_boards = [self.w_pawns, self.w_knight, self.w_bishop, self.w_rook, self.w_queen, self.w_king]
        self.black_bit_boards = [self.b_pawns, self.b_knight, self.b_bishop, self.b_rook, self.b_queen, self.b_king]
        self.piece_bit_boards = self.white_bit_boards + self.black_bit_boards
        
        self.w_occ = np.zeros(64,dtype='byte')
        self.b_occ = np.zeros(64,dtype='byte')
        
        self.piece_dict = {'wp':self.w_pawns,'wN':self.w_knight, 'wB':self.w_bishop, 
                           'wR':self.w_rook, 'wQ':self.w_queen, 'wK':self.w_king,
                           'bp':self.b_pawns, 'bN':self.b_knight, 'bB':self.b_bishop, 
                           'bR':self.b_rook, 'bQ':self.b_queen, 'bK':self.b_king}
        
        self.default_start() # initates default start
        
        self.w_to_move = True
        self.last_move = (0,0) # placeholder
        
        # advanced moves
        self.en_pass = None # possible en_pass moves
        
        self.w_castle = [True,True]
        self.b_castle = [True,True]
        
            # 0 - normal, 1 - check, 2 - checkmate, 3 - stalemate
        self.white_status = 0 
        self.black_status = 0
        self.status = 0
        
        self.gen_moves() # generate the first set of moves
        
        self.move_count = 0
        
        self.move_log = []
        
        self.capture_log = {} # move_count : associated bb taken from 
        self.special_move_log = {} # move_count : 0 - castle, 1 - promotion, 2 - enpassent 
        self.castle_right_log = {} # move_count : castle_rights for move
        self.en_pass_log = {}
        
  
    def default_start(self):
        # sets bits of pieces to correct starting postions
        
        # white     
        self.w_pawns[8:16] = 1
        self.w_rook[0] = 1
        self.w_rook[7] = 1
        self.w_knight[1] = 1
        self.w_knight[6] = 1
        self.w_bishop[2] = 1
        self.w_bishop[5] = 1
        self.w_queen[3] = 1
        self.w_king[4] = 1
        
        # black
        self.b_pawns[-16:-8] = 1
        self.b_rook[-1] = 1
        self.b_rook[-8] = 1
        self.b_knight[-2] = 1
        self.b_knight[-7] = 1
        self.b_bishop[-3] = 1
        self.b_bishop[-6] = 1
        self.b_queen[-5] = 1
        self.b_king[-4] = 1
        
        
    #@timer   
    def get_game_postion(self):
        game_state = np.zeros(64,dtype='byte') 
        display_state = np.zeros(64,dtype='object') 
        
        for i in self.piece_dict:
            game_state = np.bitwise_or(game_state,self.piece_dict[i])
            
            for j in np.where(self.piece_dict[i]==1):
                display_state[j] = i

        self.game_state = np.reshape(game_state,(8,8))
        self.display = np.reshape(display_state,(8,8))
       
    def gen_moves(self):
        "generates all legal moves"
        if self.w_to_move:
            self.castle_right = self.w_castle
        else:
            self.castle_right = self.b_castle
            
        if sum((self.w_king)) + sum((self.b_king))!=2:
            self.moves = {}
            self.captures = {}
            return    
        # generates moves
        move_class = gm.moves(self.white_bit_boards,self.black_bit_boards,\
                              self.w_to_move,self.en_pass,self.castle_right)
        
        
        self.moves = move_class.all_moves
        # temp solution to remove empty move lists
        
        self.moves = {k: v for k, v in self.moves.items() if len(v)!=0} 
        self.captures = move_class.all_captures
        self.captures = {k: v for k, v in self.captures.items() if len(v)!=0} 
        
        self.pos_en_pass = move_class.next_en_passant # possible en passant next turn
        self.en_pass_cap = move_class.pos_en_passant_cap # possible en passent this turn
        self.promotion = move_class.promotion_moves # promotion moves
        
        # temp solution
        self.promotion = {k: v for k, v in self.promotion.items() if len(v)!=0}
        
        # update game state status
        
        if len(self.moves) != 0: # moves avaliable
            if len(move_class.check) > 0:
                status = 1 # check
            else:
                status = 0 # Normal  
        else:
            if len(move_class.check) > 0:
                status = 2 # checkmate   
            else:
                status = 3 # stalemate
        self.status = status
                
        
        if self.w_to_move:
            self.white_status = status
        else:
            self.black_status = status
        
 
    def make_move(self,start,end):
        "Makes move on the board"
        
        # move log stuff
        self.move_count += 1    
        self.move_log.append((start,end))  # update move log
        self.castle_right_log[self.move_count -1] = [self.w_castle,self.b_castle]
        self.en_pass_log[self.move_count] = self.en_pass
        self.last_move = (start,end)
        
        if (start,end) in self.pos_en_pass:
            self.en_pass = end
        else:
            self.en_pass = None
        
        if any(self.castle_right):
            if self.w_to_move:
                if start == 4:
                    self.w_castle = [False,False]
                elif start == 0 or end == 0:
                    self.w_castle = [False,self.b_castle[1]]
                elif start == 7 or end == 7:
                    self.w_castle = [self.w_castle[0],False]
            else:
                if start == 60:
                    self.b_castle = [False,False]
                elif start == 56 or end == 56:
                    self.b_castle = [False,self.b_castle[1]]
                elif start == 63 or end == 63:
                    self.b_castle = [self.b_castle[0],False]
          
        
        self.update_bitboards(start,end)
        
        self.w_to_move = not self.w_to_move # flips move 
        
        # generate next set of moves
        self.gen_moves() 
        
    #@counted
    def undo_move(self):
        if len(self.move_log)!=0:
            self.w_to_move = not self.w_to_move
            
            self.w_castle,self.b_castle = self.castle_right_log[self.move_count-1] # castle rights before this turn
            self.en_pass = self.en_pass_log[self.move_count] 
            
            start,end = self.move_log.pop()
            for bitboard in self.piece_bit_boards: # move
                if bitboard[end] == 1: 
                    bitboard[end] = 0
                    bitboard[start] = 1
                    break
            
            if self.move_count in self.capture_log.keys(): # undo capture
                self.piece_bit_boards[self.capture_log[self.move_count]][end] = 1
                del self.capture_log[self.move_count]
                
            if self.move_count in self.special_move_log.keys():
                value = self.special_move_log[self.move_count]
                if value == 1: # promotion
                    if self.w_to_move:
                        self.white_bit_boards[0][start] = 1 # Pawn BB
                        self.white_bit_boards[4][start] = 0 # Queen BB
                    else:
                        self.black_bit_boards[0][start] = 1 # Pawn BB
                        self.black_bit_boards[4][start] = 0 # Queen BB
                    
                elif value == 2: # enpassent
                    if self.w_to_move:
                        self.b_pawns[end-8] = 1
                    else:
                        self.w_pawns[end+8] = 1
                    
                else: # castling
                    if self.w_to_move:
                        if end > start:
                            self.white_bit_boards[3][7] = 1
                            self.white_bit_boards[3][5] = 0
                        else:
                            self.white_bit_boards[3][0] = 1
                            self.white_bit_boards[3][3] = 0
                    else:
                        if end > start:
                            self.black_bit_boards[3][63] = 1
                            self.black_bit_boards[3][61] = 0
                        else:
                            self.black_bit_boards[3][56] = 1
                            self.black_bit_boards[3][59] = 0
            
                del self.special_move_log[self.move_count]
                
            self.move_count -= 1
            
            # generate next set of moves
            self.gen_moves()
    
    def update_bitboards(self,start,end):
        # castling
        if any(self.castle_right) and abs(end - start) == 2:
            if self.w_to_move:
                if start == 4:# white castle move
                
                    self.white_bit_boards[5][start] = 0
                    self.white_bit_boards[5][end] = 1
                    
                    if end - start < 0: # rook
                        # long castle
                        self.white_bit_boards[3][0] = 0
                        self.white_bit_boards[3][end+1] = 1
                    else:
                        self.white_bit_boards[3][7] = 0
                        self.white_bit_boards[3][end-1] = 1
                        
                    self.special_move_log[self.move_count] = 0 # move log
                    return None
            else:
                if start == 60:# black castle move
                
                    self.black_bit_boards[5][start] = 0
                    self.black_bit_boards[5][end] = 1
                    
                    if end - start < 0: # rook
                        # long castle
                        self.black_bit_boards[3][56] = 0
                        self.black_bit_boards[3][end+1] = 1
                    else:
                        self.black_bit_boards[3][63] = 0
                        self.black_bit_boards[3][end-1] = 1
                        
                    self.special_move_log[self.move_count] = 0 # move log
                    return None
        
        # could be optermised by setting primary and opponent bitboard? maybe not worth        
        for ind, bitboard in enumerate(self.piece_bit_boards): # capture
            if bitboard[end] == 1:
                bitboard[end] = 0
                self.capture_log[self.move_count] = ind # move log
                break
            
        for bitboard in self.piece_bit_boards: # move
            if bitboard[start] == 1: 
                bitboard[start] = 0
                bitboard[end] = 1
                break
            
        # en passant
        if start in self.en_pass_cap: 
            if self.en_pass_cap[start] == end:
                if self.w_to_move:
                    self.b_pawns[end-8] = 0
                else:
                    self.w_pawns[end+8] = 0
                        
                self.special_move_log[self.move_count] = 2 # move log
        
        # promotion                 
        if start in self.promotion: 
            if self.w_to_move:
                self.white_bit_boards[0][end] = 0 # Pawn BB
                self.white_bit_boards[4][end] = 1 # Queen BB
            else:
                self.black_bit_boards[0][end] = 0 # Pawn BB
                self.black_bit_boards[4][end] = 1 # Queen BB
            
            self.special_move_log[self.move_count] = 1 # move log
                

                
            
                

# %% testing class features
if __name__ == '__main__': 
    gs = game_state() 
    
    
    
