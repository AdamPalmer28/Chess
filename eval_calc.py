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
        > piece boards [Done]
        
    Intermediate:
        > pawn contested [Done]
        > pawn structure: [Done]
        > Board space 
        > move rays:
            > bishop
            > rook
            > queen
        > (P) basic king safety
        > improve knight eval:
            > postioning
            > "outputs"
            > eval scalars
        > rook eval: [Done]
        
    Advanced:
        > attackers
        > defenders
        > protectees(?)

"""
import numpy as np

def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped

from evaluation import all_eval, opening, middle, end_game, rays

@counted
def evaluation(gs):
    """
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
        score += (gs.w_knight - gs.b_knight).sum() * 3
        score += (gs.w_bishop - gs.b_bishop).sum() * 3
        score += (gs.w_rook - gs.b_rook).sum() * 5
        score += (gs.w_queen - gs.b_queen).sum() * 9
        
        score += (gs.w_king - gs.b_king).sum() * 100 # not sure if its needed
        
        return score
    total_eval = basic_p_count()
    
    move_rays = rays.gen_rays(gs.white_bit_boards,gs.black_bit_boards)
    
    
    total_eval += all_eval.eval_all_time(gs,move_rays) # eval for all stages of game
    
    
    # piece total
    w_p_total = gs.w_pawns.sum() + 3*gs.w_knight.sum() + 3*gs.w_bishop.sum() +\
                5*gs.w_rook.sum() + 9*gs.w_queen.sum()
    b_p_total = gs.b_pawns.sum() + 3*gs.b_knight.sum() + 3*gs.b_bishop.sum() +\
                5*gs.b_rook.sum() + 9*gs.b_queen.sum()
    
    def king_safety():
        "Works out the safety of the kings"
        for turn, king_pos in enumerate([gs.w_king.nonzero()[0][0],gs.b_king.nonzero()[0][0]]):
            pass
    
    
    
    if gs.move_count < 20:
        # opening
         total_eval += opening.opening_eval(gs)
    elif (w_p_total < 20) and (b_p_total < 20):
        # end
         total_eval += end_game.end_eval(gs)
    else:
        # mid
         total_eval += middle.mid_eval(gs)
    
    return np.round(total_eval,3)


