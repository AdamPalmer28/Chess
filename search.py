class search():
    """
    [CRITICAL TO OPTERMISE - Longest computing process]
    The search class is the fundamentals of the AI, it handles searching and
    identifying the best move, communicating directly with evac class to obtain
    position evaluations to then perform min max algorithm
    
    Inputs:
        > w and b bitboards
        > w_to_move - boolean
        > all possible moves
    
    Outputs:
        > tuple - best move (PRIMARY)
        > recent evaluation (necessary but how?) //  (lists of move orders with associated value)
        
    Plan:
        > hold info about good recent move orders to check first

        
    Questions / problems:
        > This class will likely be large with arguably differnt functions, 
        could be split up!       
        > how to decide what is searched first?
        > get out of check?
    """
    def __init__(self):
        pass
