# -*- coding: utf-8 -*-
"""
This scripts generates the move rays from the current gs, this will be a simple 
stripped down version of move generate but with additional benifits.  
"""
import numpy as np


def move_rays(index, slide : list):
    """
    Generate the move arrays of each piece
            
    slide: int - values are one of [8,1,7,9]
            8: Up - Down
            1: Left - Right
            7: Top_left - Bottom ight
            9: Bottom left - Top right
    """
    move_rays = np.zeros(64,dtype='byte')
    
    row = index // 8
    col = index % 8
    for step in slide: 
        if step == 8 : # vertical movement
            fwd = 7 - row
            back = row
            
        elif step == 1 : # horizoal movement
            fwd = 7 - col
            back = col
            
        elif step == 7 : # top left to bot right
            fwd = min(7-row,col)
            back = min(row,7-col) 
            
        elif step == 9 : # top right to bot left  
            fwd = min(7-row,7-col) 
            back = min(row,col) 
         
        for x in range(fwd): # forwards
            move_rays[index + (x+1)*step] = 1
            
        for x in range(back): # backwards
            move_rays[index - (x+1)*step] = 1   
    
    return move_rays

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

def knight_moves(index):
    moves = np.zeros(64,dtype='byte')
    
    knight_jumps = [-17,-15,-10,-6,6,10,15,17] # index jumps of knights
    
    if index // 8 in [1,6]:# one square away (north & south)
        if index // 8 == 1: # south
            knight_jumps = [j for j in knight_jumps if j not in [-17,-15]]
        else:           # north
            knight_jumps = [j for j in knight_jumps if j not in [15,17]]
            
    elif index // 8 in [0,7]:# edge of board (north & south) 
        if index // 8 == 0: # south
            knight_jumps = [j for j in knight_jumps if j not in [-17,-15,-10,-6]]
        else:           # north   
            knight_jumps = [j for j in knight_jumps if j not in [17,15,10,6]]

    if index % 8 in [1,6]: # one square away (east & west)
        if index % 8 == 1:  # west
            knight_jumps = [j for j in knight_jumps if j not in [6,-10]]
        else:           # east
            knight_jumps = [j for j in knight_jumps if j not in [10,-6]]
            
    elif index % 8 in [0,7]: # edge of board (east & west)
        if index % 8 == 0:  # west
            knight_jumps = [j for j in knight_jumps if j not in [-17,-10,6,15]]
        else:           # east
            knight_jumps = [j for j in knight_jumps if j not in [-15,-6,10,17]]
            
            
    for j in knight_jumps:
        moves[index+j] = 1
    
    return moves 

class gen_rays():
    
    def __init__(self,w_bb, b_bb):
        # pawns, knight, bishop, rook, queen, king
        self.w_bishop = self.slide_move(w_bb[2],[7,9])
        self.b_bishop = self.slide_move(b_bb[2],[7,9])
        
        self.w_queen = self.slide_move(w_bb[4],[1,8,7,9])
        self.b_queen = self.slide_move(b_bb[4],[1,8,7,9])
        
        self.w_rook = self.slide_move(w_bb[3],[1,8])
        self.b_rook = self.slide_move(b_bb[3],[1,8])
       
        self.w_knight = self.knight_move(w_bb[1])
        self.b_knight = self.knight_move(b_bb[1])
        
        
    def slide_move(self,bb,slide):
        p_rays = np.zeros(64,dtype='byte')
        for p in bb.nonzero()[0]: 
            p_rays = np.bitwise_or(p_rays,move_rays(p, slide))
        return p_rays
    
    def knight_move(self, bb):
        p_rays = np.zeros(64,dtype='byte')
        for p in bb.nonzero()[0]: 
            p_rays = np.bitwise_or(p_rays,knight_moves(p))
        return p_rays