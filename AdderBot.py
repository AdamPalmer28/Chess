"""
Chess AI
"""
import random

def rando_bot(moves):
    random_p, p_moves = random.choice(list(moves.items()))
    r_move = random.choice(p_moves)
    
    combo = (random_p, r_move)
    return combo

from eval_calc import evaluation

import copy
def simple_bot(gs):
    """
    Looks 1 move ahead and evaluates (i.e. depth 1)
    Goal: pathfind methodology for min max algo
    """
    moves = gs.moves
    #gstest = gs.copy
    
    best_move = (0,0)
    
    #con = (1 if gs.w_to_move else -1)
    #best_eval = con * -511 # idk what to put here
    if gs.w_to_move:
        best_eval = -511
        for p, m_l in moves.items():
            for m in m_l:
                gstest = copy.deepcopy(gs)
                    
                gstest.make_move(p,m)
                move_eval = evaluation(gstest)
                
                if move_eval > best_eval:
                    best_move = (p,m)
                    best_eval = move_eval
                    
    else: # black move
        best_eval = +511
        for p, m_l in moves.items():
            for m in m_l:
                gstest = copy.deepcopy(gs)
                    
                gstest.make_move(p,m)
                move_eval = evaluation(gstest)
                
                if move_eval < best_eval:
                    best_move = (p,m)
                    best_eval = move_eval
            
    return best_move