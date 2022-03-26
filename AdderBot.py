"""
Chess AI
"""
import copy
from eval_calc import evaluation
import time 
import numpy as np

# optermisation
import cProfile
import pstats
from pstats import SortKey

def timer(func):
    def wrapper(*args):
        before = time.time()
        val = func(*args)
        print("Function took:", np.round(time.time() - before,4), " seconds")
        return val
    return wrapper

def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped




def quiesce(gs,alpha,beta,capture_depth=0):
        "Searchs all possible caputres for possible tatics after intial depth"
        stand_score = (1 if gs.w_to_move else -1) * evaluation(gs)
        
        if stand_score >= beta:
            return beta
        if alpha < stand_score:
            alpha = stand_score
            
        if capture_depth == 4:
            "limit quiesce depth"
            return alpha
        
        for p, m_l in gs.captures.items():
            for m in m_l:
                gs.make_move(p,m) # make move
                score = -quiesce(gs,-beta,-alpha,capture_depth+1)
                gs.undo_move()
               
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score 
                    
        return alpha
    
#@timer
def alphabeta_search(gs,total_depth=2): 
    
    bestmoves_dict = {}
    
    def alphabeta(alpha=-511, beta=511, depth=0):
        "Alpha-Beta algorithm"
        if depth == total_depth:
            return quiesce(gs,alpha,beta)
        
        if len(gs.moves)==0: # checkmate / stalemate
            score = (1 if gs.w_to_move else -1) * evaluation(gs)
            if score >= beta:
                return beta
            if score > 127: # checkmate
                score -= depth*10
            if score > alpha:
                alpha = score
            return alpha
        
        
        for p, m_l in gs.moves.items():
            
            for m in m_l:
                gs.make_move(p,m) # make move
                
                score = -alphabeta(-beta,-alpha, depth+1) # go a further depth
                
                gs.undo_move()
                if score >= beta:
                    return beta
                
                if score > 127: # checkmate (possibility)
                        score -= depth*10
                if score > alpha:
                    alpha = score
                    
                    if depth == 0:
                        bestmoves_dict[alpha] = (p,m)
                        
        return alpha
    
    alphabeta()
    
    #print(bestmoves_dict)
    return bestmoves_dict[max(bestmoves_dict.keys())]



from multiprocessing import Process
import os
@timer
def adder_chess(gs,depth):
    "Implements a min-max algorithm with Alpha-beta prunning"
    
    # num_process = os.cpu_count()
    # cores = []
    
    # for i in range(num_process):
    #     process = Process(target=alphabeta_search, args =(gs,depth))
    #     cores.append(process)
    
    #     for process in cores:
    #         process.start()
    
    #     for process in cores:
    #         process.join()
            
    best_move = alphabeta_search(gs,depth)
    
    #alphabeta_search(gs,depth)
    return best_move

# %%
# from multiprocessing import Process
# import os

# num_process = os.cpu_count()
# cores = []
# for i in range(num_process):
#     process = Process(target=alphabeta_search)
#     cores.append(process)

#     for process in cores:
#         process.start()

#     for process in cores:
#         process.join()



# %% Old bots - pathfinders
import random

def rando_bot(moves):
    random_p, p_moves = random.choice(list(moves.items()))
    r_move = random.choice(p_moves)
    
    combo = (random_p, r_move)
    return combo




def simple_bot(gs):
    """
    Looks 1 move ahead and evaluates (i.e. depth 1)
    Goal: pathfind methodology for min max algo
    """
    moves = gs.moves
    #gstest = gs.copy
    
    best_move = (0,0)
    
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