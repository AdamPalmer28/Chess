"""
This is the driver file of the chess program, handling input and displaying
the current game state
"""

"""
Notes / Plans
=============
    > Add detail to top ribben
"""
# %% Imports / Intialising 
import numpy as np
import pygame as p
import sys
from pygame.locals import *
import time

import Chess_engine
import AdderBot # chess bot


# board attributes
width = height = 768
top_rib = 96
dimensions = 8
sq_size = height / dimensions 
max_fps = 15


# chess pieces
images = {}
def load_images():
    colour = ['w','b']
    peices = ['p','K','Q','B','N','R']
    for col in colour:
        for peice in peices:
            images[col + peice] = p.transform.scale(p.image.load('images/{}{}.png'.format(col,peice)),(sq_size,sq_size))

# %% main
def main(white =0,black = 0):
    """
    Runs the chess program connecting the pygame UI to the chess engine
    
    white : binary
    black : binary
    
    0 = AI
    1 = Human
    """
    p.init()

    screen = p.display.set_mode((width,height+top_rib))
    clock = p.time.Clock()
    screen.fill(p.Color("#1f1c1c"))
    load_images() # only do once
    
    # Initialise
    gs = Chess_engine.game_state()
    draw_board_state(screen,gs)# Initialise the board
    selected_piece = 0
    
    AI_turn = False
    if (white == 0) or (black == 0):
        if (white == 0) and (black == 0):
            AI_turn = True
        elif (white == 0):
            AI_turn = 'w'
        elif (black == 0):
            AI_turn = 'b'

    
    running = True
    while running:
        next_turn = ("w" if gs.w_to_move else "b") 
        
        if (AI_turn == True) or (AI_turn == next_turn):
            # not sure if there is a better place to put this?
            # call AI bot
            #time.sleep(0.5)
            if gs.status == 0:
                AI_move = AdderBot.rando_bot(gs.moves)
                gs.make_move(AI_move[0],AI_move[1])
                draw_board_state(screen,gs,None)
            else:
                #print("Game over!")
                pass

        for e in p.event.get():
            
            if e.type == p.QUIT:
                p.quit()
                sys.exit()

                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN:# moves
                location = p.mouse.get_pos() # (x, y) location of mouse
                
                col = (location[0])//sq_size
                row = (location[1]-top_rib)//sq_size
                if row < 0:
                    # Clicked Ribben area!!!
                    continue
                
                
                # Interactive with board
                
                if (AI_turn == True) or (AI_turn == next_turn):
                    # AI turn
                    pass
                else:
                     
                    if (selected_piece == 0):
                        # first click - selecting piece
                        if (gs.display[7-int(row),int(col)]!=0) and (gs.display[7-int(row),int(col)][0]==next_turn):
                            
                            def first_click():
                                selected_piece = gs.display[7-int(row),int(col)]
                                start_index = int((7-row)*8 + col)
                                try:
                                    p_moves = gs.moves[start_index]
                                    #print(p_moves) # feedback
                                except KeyError:
                                    p_moves = []
                                draw_board_state(screen,gs,start_index,p_moves)
                                return selected_piece,start_index,p_moves
                            
                            selected_piece,start_index, p_moves = first_click()
                    else:
                        # second click - move command
                        
                        if (gs.display[7-int(row),int(col)]!= 0) and (gs.display[7-int(row),int(col)][0] == next_turn):
                            # if same colour selected recall first_click
                            selected_piece,start_index, p_moves = first_click()
                            continue
                        
                        end_index = int((7-row)*8 + col)
                        
                        if end_index in p_moves: # avaliable move
                            gs.make_move(start_index,end_index) # make move
                            selected_piece = 0 # reset selected piece
                            draw_board_state(screen,gs,None)
                            #print(gs.moves)
            
        clock.tick(max_fps)
        p.display.flip()
        
        
# %% Draw Board state        
        
def draw_board_state(screen,gs,start_index=None,moves=None):
    
    draw_board(screen) # draws square on the board
    draw_pieces(screen,gs.display) # draws pieces
    draw_ribben(screen,gs)
    if start_index != None:

        row = 7 - start_index // 8 
        col = start_index - (8*(7-row))   
        
        # highlights sq selected and avaliable moves
        highlight_square(screen,row,col,moves)   
    
def draw_board(screen):
    colors = [p.Color("White"),p.Color("#5e1106")]
    for r in range(dimensions):
        for c in range(dimensions):
            color = colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*sq_size,r*sq_size+top_rib,sq_size,sq_size))
        
def draw_pieces(screen,board):    
    for r in range(dimensions):
        for c in range(dimensions):
            piece = board[r,c]
            if piece != 0:
                screen.blit(images[piece],p.Rect((c)*sq_size,(7-r)*sq_size+top_rib,sq_size,sq_size,))
            
def highlight_square(screen,row,col,moves=None):
    
    s=p.Surface((sq_size,sq_size))
    s.set_alpha(75) # transperacy value
    s.fill(p.Color('blue'))
    screen.blit(s,(col*sq_size,row*sq_size + top_rib))
    
    for m in moves:
        r = 7 - m // 8 
        c = m - (8*(7-r))
        t=p.Surface((sq_size,sq_size))
        t.set_alpha(150) # transperacy value
        t.fill(p.Color('yellow'))
        screen.blit(t,(c*sq_size,r*sq_size+top_rib))


# %% UI features  

# ribben infomation
p.font.init() # you have to call this at the start, 
ribbon_font = p.font.SysFont('Arial', 36)
ribbon_bold = p.font.SysFont('Arial', 36)
ribbon_bold.set_bold(True)
end_screen_font = p.font.SysFont('Arial', 72)   

def draw_ribben(screen,gs):
    p.draw.rect(screen,'#9A9A9A',p.Rect(0,0,width,top_rib))
    p.draw.rect(screen,"#5e1106",p.Rect(10,top_rib/16,192,top_rib-top_rib/8))
    
    p.draw.rect(screen,"black",p.Rect(width/2 - 80,top_rib/16,192,top_rib-top_rib/8)) # check
    move_text = ribbon_bold.render('Move:', True, (0, 0, 0))
    screen.blit(move_text,(20,top_rib/4))
    
    if gs.w_to_move:
        textsurface = ribbon_font.render('White', True, (255,255,255))
        p.draw.rect(screen,"White",p.Rect(210,top_rib/16,top_rib-top_rib/8,top_rib-top_rib/8))
        if gs.white_status != 0:
            # check / checkmate / stalemate
            status_update(screen,gs.white_status, 'Black')
    else:
        textsurface = ribbon_font.render('Black', True, (0, 0, 0))
        p.draw.rect(screen,"Black",p.Rect(210,top_rib/16,top_rib-top_rib/8,top_rib-top_rib/8))
        if gs.black_status != 0:
            status_update(screen,gs.black_status, 'White')
            
    screen.blit(textsurface,(120,top_rib/4))  


ribbon_check = p.font.SysFont('Arial', 60)

def status_update(screen,status, attacker):
    # check / checkmate / stalemate
    if status == 1:
        check(screen)
    elif status == 2:
        checkmate(screen,attacker)
    else:
        stalemate(screen)
    
def check(screen): # Check GFX
    textsurface = ribbon_check.render('Check', True, (128,17,6))#r=94
    screen.blit(textsurface,(width/2 - 56,top_rib/7)) 

end_screen_font = p.font.SysFont('Arial', 54)  
def checkmate(screen,winner): # Checkmate GFX
    p.draw.rect(screen,'Black',p.Rect(192/2,(height-top_rib)/2,width-192, 256)) # outter retangle
    p.draw.rect(screen,"White",p.Rect(192/2 + 8,(height-top_rib)/2 +8 ,width-192-16, 256 -16)) # inner retangle
    end_text = end_screen_font.render(winner + ' wins by checkmate!', True, (0, 0, 0))
    screen.blit(end_text,(192/2 + 32,(height-top_rib)/2 + 100))

def stalemate(screen): # Stalemate GFX  
    p.draw.rect(screen,'Black',p.Rect(192/2,(height-top_rib)/2,width-192, 256)) # outter retangle
    p.draw.rect(screen,"White",p.Rect(192/2 + 8,(height-top_rib)/2 +8 ,width-192-16, 256 -16)) # inner retangle
    end_text = end_screen_font.render('Draw by Stalemate', True, (0, 0, 0))
    screen.blit(end_text,(192/2 + 100,(height-top_rib)/2 + 100))
    

# %% Start program    ( if __name__ == '__main__' )  
        
if __name__ == '__main__':
    ref_matrix = np.arange(64).reshape(8,8)[::-1,]# for my visulisation
    
    w_player = 0 
    b_player = 0
    # 1 = human, 0 = AI
    main(white = w_player, black = b_player)

    


