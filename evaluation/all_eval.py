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
        
        for p in gs.w_rook.nonzero()[0]:
            # pawn ahead?
            for pawn in gs.w_pawns.nonzero()[0]:
                if (pawn - p) % 8 == 0:
                    score -= 0.2

                
        for p in gs.b_rook.nonzero()[0]:
            # pawn ahead?
            for pawn in gs.b_pawns.nonzero()[0]:
                if (pawn - p) % 8 == 0:
                    score -= 0.2

        return score
    
    total_eval += rook_eval()
    
    
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
            #score based on position up the board
        
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
            
        # isolated pawns
        
        # backward / weak pawns
        
        # past pawns (calc will be similar to above) 
        
        return score
    total_eval += pawn_eval()
    
    def protect_rays():
        score = 0
        return score
        
    
    total_eval += protect_rays()
    
    
    return total_eval