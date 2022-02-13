""""""
import random

def rando_bot(moves):
    random_p, p_moves = random.choice(list(moves.items()))
    r_move = random.choice(p_moves)
    
    combo = (random_p, r_move)
    return combo

