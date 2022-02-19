"""
===============================================================================
==================================<[ Ideas ]>==================================
===============================================================================

> Call eval after move generation
    > use king safety in move gen to advantage
    
> is this 2 seperate scores for white and black 
 or is it a combined score indicating who is ahead? (think 2nd is better)    
        
    

Areas of evaluation:
    Basic:
        > piece score [Done]
        > Checkmate / Stalemate:
            > Stalemate
        > active/optimal piece placement
        
    Intermediate:
        > pawn structure
        > attackers
        > defenders
        > protectees(?)
        
    Advanced:
        > board space
        > xray

"""
import numpy as np

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
    def basic_p_count():
        "Counts board peices"
        score = 0
        score += gs.w_pawns.sum() * 1
        score += gs.w_knight.sum() * 3
        score += gs.w_bishop.sum() * 3
        score += gs.w_rook.sum() * 5
        score += gs.w_queen.sum() * 9
    
        #gs.w_king = np.zeros(64,dtype='byte')
        
        score -= gs.b_pawns.sum() * 1
        score -= gs.b_knight.sum() * 3
        score -= gs.b_bishop.sum() * 3
        score -= gs.b_rook.sum() * 5
        score -= gs.b_queen.sum() * 9
        
        return score
        #gs.b_king = np.zeros(64,dtype='byte')
       
    total_eval = basic_p_count()
       
    return total_eval