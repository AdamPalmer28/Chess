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
        
        
        self.piece_dict = {'wp':self.w_pawns,'wN':self.w_knight, 'wB':self.w_bishop, 
                           'wR':self.w_rook, 'wQ':self.w_queen, 'wK':self.w_king,
                           'bp':self.b_pawns, 'bN':self.b_knight, 'bB':self.b_bishop, 
                           'bR':self.b_rook, 'bQ':self.b_queen, 'bK':self.b_king}
        
        self.default_start() # initates default start
        
        self.w_to_move = True
        self.last_move = (0,0) # placeholder
        
        # advanced moves
        self.en_pass = None # possible en_pass moves
        
        self.white_castle = (True,True)
        self.black_castle = (True,True)
            
            # 0 - normal, 1 - check, 2 - checkmate, 3 - stalemate
        self.white_status = 0 
        self.black_status = 0
        self.status = 0
        
        self.gen_moves() # generate the first set of moves
        
  
    def default_start(self):
        # sets bits of pieces to correct postions
        
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
        
        self.get_game_postion()
        
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
            castle_rights = self.white_castle
        else:
            castle_rights = self.black_castle
            
        # generates moves
        move_class = gm.moves(self.white_bit_boards,self.black_bit_boards,\
                              self.w_to_move,self.en_pass,castle_rights)
        self.moves = move_class.all_moves
        
        # temp solution to remove empty move lists
        self.moves = {k: v for k, v in self.moves.items() if len(v)!=0} 
        print(self.moves)
        self.pos_en_pass = move_class.next_en_passant # possible en passant next turn
        self.en_pass_cap = move_class.pos_en_passant_cap # possible en passent this turn
        self.promotion = move_class.promotion_moves # promotion moves
        self.promotion = {k: v for k, v in self.promotion.items() if len(v)!=0}
        
        # update game state status

        if len(self.moves.values()) != 0: # moves avaliable
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
        if (start,end) in self.pos_en_pass: # updates possible postion of en passant
            self.en_pass = end
        else:
            self.en_pass = None
        
        self.update_bitboards(start,end)
        self.last_move = (start,end)
        self.w_to_move = not self.w_to_move # flips move 
        
        self.get_game_postion()
        
        # generate next set of moves
        
        #t = time.time()
        self.gen_moves() 
        #print(np.round(time.time()-t,6))
    
    def update_bitboards(self,start,end):
        # could be optermised by setting primary and opponent bitboard? maybe not worth
        for bitboard in self.piece_bit_boards: # capture
            if bitboard[end] == 1:
                bitboard[end] = 0
                break
            
        for bitboard in self.piece_bit_boards: # move
            if bitboard[start] == 1: 
                # moves
                bitboard[start] = 0
                bitboard[end] = 1
                break

        if start in self.en_pass_cap : # en passant
            if self.en_pass_cap[start] == end:
                for bitboard in self.piece_bit_boards:
                    if self.w_to_move:
                        bitboard[end-8] = 0
                    else:
                        bitboard[end+8] = 0
                         
        if start in self.promotion: # promotion
            if self.w_to_move:
                self.white_bit_boards[0][end] = 0 # Pawn BB
                self.white_bit_boards[4][end] = 1 # Queen BB
            else:
                self.black_bit_boards[0][end] = 0 # Pawn BB
                self.black_bit_boards[4][end] = 1 # Queen BB
                
            
                

# %% testing class features
if __name__ == '__main__': 
    gs = game_state() 
    for i in gs.piece_dict.values():# without values() it prints keys
        print(i)
