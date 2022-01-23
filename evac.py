


class evaluation():
    """
    [--< Critical tooptermisation >--]
    The evaluation class handles evaluating a postion
    
    The method to evaluate it tbd:
        evaluate the whole position every time?
            smart evac? only evaluate when there is an update
        evac each side seperately? independently?
        
    Inputs:
        > Piece bitboards
        > Who's next to move? (simply guess next move? - not much weighting)
        
        
    Outputs:
        > evac score of board
            is this 2 seperate scores for white and black 
            or is it a combined score indicating who is ahead
        
        
    

    Areas of evaluation:
        Basic:
            > piece score
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
    def __init__(self):
        pass