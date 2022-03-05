"""
===============================================================================
==================================<[ Ideas ]>==================================
===============================================================================

> Call eval after move generation
    > use king safety in move gen to advantage
    
> is this 2 seperate scores for white and black 
 or is it a combined score indicating who is ahead? (think 2nd is better)    
        
    

Areas of evaluation:
    Basic: [Done]
        > piece score [Done]
        > Checkmate / Stalemate: [Done]
            > Stalemate
        > piece boards [Done]
        
    Intermediate:
        > pawn structure
        > attackers
        > defenders
        > protectees(?)
        > rook eval:
            > vertical squares
            > pawns ahead of rook?
        
    Advanced:
        > board space
        > xray

"""
import numpy as np
from board_sections import board_divide as bd

board = bd()

def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped

@counted
def evaluation(gs):
    """
    [--< Critical to optermisation >--]
    The evaluation function handles evaluating a postion
    
    
    The method to evaluate it tbd:
        evaluate the whole position every time?
            smart evac? only evaluate when there is an update
        evac each side seperately? independently?
        
    Inputs:
        > Piece bitboards
        > Who's next to move? (simply guess next move? - not much weighting)
        
        
    Outputs:
        > evac score of board
 
    """
    if gs.status == 2: # checkmate
        return (-1 if gs.w_to_move else +1) * 256
    if gs.status == 3: # stalemate
        return 0
    
    def basic_p_count():
        "Counts board peices"
        score = 0
        score += (gs.w_pawns - gs.b_pawns).sum() * 1
        score += (gs.w_knight - gs.b_knight).sum() * 3.1
        score += (gs.w_bishop - gs.b_bishop).sum() * 3.3
        score += (gs.w_rook - gs.b_rook).sum() * 5
        score += (gs.w_queen - gs.b_queen).sum() * 9
        
        score += (gs.w_king - gs.b_king).sum() * 100 # not sure if its needed
        
        return score
        
       
    total_eval = basic_p_count()
       
    def bishop_pos():
        "Basic bishop postions"
        score = 0
        score += np.bitwise_and(gs.w_bishop, board.long_1_diag).sum() * 0.6
        score -= np.bitwise_and(gs.b_bishop, board.long_1_diag).sum() * 0.6
        
        score += np.bitwise_and(gs.w_bishop, board.long_2_diag).sum() * 0.45
        score -= np.bitwise_and(gs.b_bishop, board.long_2_diag).sum() * 0.45
                
        score += np.bitwise_and(gs.w_bishop, board.long_3_diag).sum() * 0.35
        score -= np.bitwise_and(gs.b_bishop, board.long_3_diag).sum() * 0.35
        return score
    
    total_eval += bishop_pos()
    
    def knight_pos():
        "Basic knight postions"
        score = 0
        score += np.bitwise_and(gs.w_knight, board.mid).sum() * 0.3
        score -= np.bitwise_and(gs.b_knight, board.mid).sum() * 0.3
        
        score += np.bitwise_and(gs.w_knight, board.w_mid).sum() * 0.15
        score -= np.bitwise_and(gs.b_knight, board.b_mid).sum() * 0.15
         
        return score
    
    total_eval += knight_pos()
    
    def rook_eval():
        score = 0
        
        return score
    
    
    def pawn_eval():
        score = 0
        
        return score
    
    
    
    
    return total_eval