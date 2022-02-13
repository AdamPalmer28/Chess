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
        pass
    pass