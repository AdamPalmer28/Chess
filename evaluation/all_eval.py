import numpy as np

from evaluation.board_sections import board_divide as bd
board = bd()

def pawn_caps(pawns,white=True):
    "Calcs capture moves "
    
    captures = np.zeros(64,dtype='byte')
    if white:
        for i in pawns.nonzero()[0]:
            if i % 8 != 7: 
                captures[i+9] = 1
            if i % 8 != 0:
                captures[i+7] = 1
    else:
        for i in pawns.nonzero()[0]:
            if i % 8 != 7: 
                captures[i-7] = 1
            if i % 8 != 0:
                captures[i-9] = 1
    return captures

def eval_all_time(gs,rays):
    total_eval = 0
    
    ##### Postions #####
    def bishop_pos():
        "Basic bishop postions"
        score = 0
        # long diag
        score += np.bitwise_and(gs.w_bishop, board.long_1_diag).sum() * 0.6
        score -= np.bitwise_and(gs.b_bishop, board.long_1_diag).sum() * 0.6
        # 2nd long diag
        score += np.bitwise_and(gs.w_bishop, board.long_2_diag).sum() * 0.45
        score -= np.bitwise_and(gs.b_bishop, board.long_2_diag).sum() * 0.45
        # 3rd long diag        
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
    
    # King safety
    def king_safety():
        pass
    
    #total_eval += king_safety()
    
    def rook_eval():
        score = 0
        pawn_occ = np.bitwise_or(gs.w_pawns,gs.b_pawns)
        
        w_rook = gs.w_rook.nonzero()[0]
        b_rook = gs.b_rook.nonzero()[0]
        # white
        for w_r in w_rook:
            # blocking pawns
            for w_p in gs.w_pawns.nonzero()[0]:
                if (w_r - w_p) % 8 == 0:
                    if w_p > w_r:
                        score += -0.2
            # opp pawns            
            for b_p in gs.b_pawns.nonzero()[0]:
                if (w_r - b_p) % 8 == 0:
                    score += -0.05
            # open file   
            if np.bitwise_and(board.col[w_r % 8],pawn_occ).sum() == 0:
                score += 0.25
            elif np.bitwise_and(board.col[w_r % 8],gs.b_pawns).sum() == 0:
                score += 0.15
          
            if w_r // 8 >= 5:
                score += 0.1
                
        # black
        for b_r in b_rook:
            # blocking pawns
            for b_p in gs.b_pawns.nonzero()[0]:
                if (b_r - b_p) % 8 == 0:
                    if b_p > b_r:
                        score -= -0.2
            # opp pawns           
            for w_p in gs.w_pawns.nonzero()[0]:
                if (b_r - w_p) % 8 == 0:
                    score -= -0.05
                    
            # open file
            if np.bitwise_and(board.col[b_r % 8],pawn_occ).sum() == 0:
                score -= 0.25
            elif np.bitwise_and(board.col[b_r % 8],gs.w_pawns).sum() == 0:
                score -= 0.15
       
            if b_r // 8 <= 2:
                score -= 0.1
                
        # doubled rooks
        if len(w_rook) > 1:
            if w_rook[0] - w_rook[1] % 8 == 0:
                score += 0.15
        if len(b_rook) > 1:
            if b_rook[0] - b_rook[1] % 8 == 0:
                score -= 0.15
         
        return score
    
    total_eval += rook_eval()
    
    weak_pawns = np.zeros(64,dtype='byte')
    def pawn_eval():
        score = 0
        
        # white
        w_contested = pawn_caps(gs.w_pawns,white=True)
        # black
        b_contested = pawn_caps(gs.b_pawns,white=False)
        
        # postions
        score += np.bitwise_and(w_contested, board.mid).sum() * 0.15
        score += np.bitwise_and(w_contested, board.centre).sum() * 0.1
        score += np.bitwise_and(w_contested, board.b_side).sum() * 0.1
        
        score -= np.bitwise_and(b_contested, board.mid).sum() * 0.15
        score -= np.bitwise_and(b_contested, board.centre).sum() * 0.1
        score -= np.bitwise_and(b_contested, board.w_side).sum() * 0.1
        
        # pawn chains
        score += np.bitwise_and(w_contested, gs.w_pawns).sum() * 0.2
        score -= np.bitwise_and(b_contested, gs.b_pawns).sum() * 0.2
        
        # double pawns
        for col in board.col:
            w_pawns = np.bitwise_and(col, gs.w_pawns).sum()
            b_pawns = np.bitwise_and(col, gs.b_pawns).sum()

            if w_pawns > 1:
                score += -0.12*(w_pawns - 1)
            if b_pawns > 1:
                score -= -0.12*(b_pawns - 1)
         
        w_pawns_l = gs.w_pawns.nonzero()[0]
        b_pawns_l = gs.b_pawns.nonzero()[0]
        w_pawns_cols = [p % 8 for p in w_pawns_l]
        w_pawns_rows = [p // 8 for p in w_pawns_l]
        b_pawns_cols = [p % 8 for p in b_pawns_l]
        b_pawns_rows = [p // 8 for p in b_pawns_l]
        
        # Isolated & weak pawns
        for colour, col_list in enumerate([w_pawns_cols,b_pawns_cols]):
            con = (1 if colour == 0 else -1)
            
            pawn_set = (w_pawns_l if colour == 0 else b_pawns_l)
            row_l = (w_pawns_rows if colour == 0 else b_pawns_rows)
            opp_row_l = (b_pawns_rows if colour == 0 else w_pawns_rows)
            opp_col_l = (b_pawns_cols if colour == 0 else b_pawns_cols)
            
            start_row = 3.5 - con*2.5
            end_row = 3.5 + con*3.5
            
            for ind, p in enumerate(col_list):
                # adjacent col pawns
                adj_index = [i for i, x in enumerate(col_list) if (p - 1 == x or p + 1 == x)]
                adj_opp_index = [i for i, x in enumerate(opp_col_l) if (p - 1 == x or p + 1 == x)]
                # isolated pawns
                if p == 0 or p == 7:
                    if len(adj_index) == 0:
                        score -= con*0.12
                        weak_pawns[pawn_set[ind]] = 1
                elif len(adj_index) == 0:
                    score -= con*0.2
                    weak_pawns[pawn_set[ind]] = 1
                    
                # backward pawns
                p_row = row_l[ind]
                if all(con*(row_l[r_ind] - p_row) > 0 for r_ind in adj_index):
                    if not (p == 0 or p == 7):
                        score -= con*0.07
                    weak_pawns[pawn_set[ind]] = 1
                    
                # past pawns  
                if p not in opp_col_l: # no opposite pawn
                    rel_row = p_row if con == 1 else abs(p_row -7)
                    
                    if len(adj_opp_index) == 0:
                        score += con*0.4
                        
                    elif all( con*(p_row - opp_row_l[index]) >= 0 for index in adj_opp_index):
                        score += con*0.4
                
                # rank detection 
                rel_row = p_row if con == 1 else abs(p_row -7)
                if rel_row > 4:
                    score += con*(rel_row - 4)
                elif rel_row >= 3: 
                    score += con*(rel_row - 2)*0.05
        return score
    total_eval += pawn_eval()
    
    def pawn_rays():
        """ Attacks / defends weak pawns """
        score = 0
        
        score += np.bitwise_and(rays.w_bishop,weak_pawns).sum()*0.07
        score -= np.bitwise_and(rays.b_bishop,weak_pawns).sum()*0.07
        
        score += np.bitwise_and(rays.w_knight,weak_pawns).sum()*0.14
        score -= np.bitwise_and(rays.b_knight,weak_pawns).sum()*0.14
        
        score += np.bitwise_and(rays.w_rook,weak_pawns).sum()*0.05
        score -= np.bitwise_and(rays.b_rook,weak_pawns).sum()*0.05
        
        score += np.bitwise_and(rays.w_queen,weak_pawns).sum()*0.04
        score -= np.bitwise_and(rays.b_queen,weak_pawns).sum()*0.04
 
        return score
    total_eval += pawn_rays()
    
    def protect_rays():
        """ Battery / protection detection """
        score = 0
        
        score += np.bitwise_and(rays.w_bishop,gs.w_queen).sum()*0.1
        score -= np.bitwise_and(rays.b_bishop,gs.b_queen).sum()*0.1
        
        score += np.bitwise_and(rays.w_knight,gs.w_knight).sum()*0.05
        score -= np.bitwise_and(rays.b_knight,gs.b_knight).sum()*0.05
        
        score += np.bitwise_and(rays.w_rook,gs.w_queen).sum()*0.1
        score -= np.bitwise_and(rays.b_rook,gs.w_queen).sum()*0.1
 
        return score
    total_eval += protect_rays()
    
    
    return np.round(total_eval,3)