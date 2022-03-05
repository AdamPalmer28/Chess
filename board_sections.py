import numpy as np

class board_divide():
    """
    Divide board into sections for easy evaluation reference

    Center - 2 middle rows/cols
    Middle - 4 middle rows/cols
    """
    
    def __init__(self):
        
        self.empty = np.zeros(64,dtype='byte')
        
        # 2 centre cols/rows
        self.centre_col = np.zeros(64,dtype='byte') 
        self.centre_row = np.zeros(64,dtype='byte')
        
        # 4 centre cols/rows
        self.out_mid_col = np.zeros(64,dtype='byte')
        self.out_mid_row = np.zeros(64,dtype='byte')
        
        # longest diagonals 
        self.long_1_diag = np.zeros(64,dtype='byte')
        self.long_2_diag = np.zeros(64,dtype='byte')
        self.long_3_diag = np.zeros(64,dtype='byte')
        
        for i in range(8):
            # cols
            self.centre_col[3+i*8] = 1
            self.centre_col[4+i*8] = 1
            
            self.out_mid_col[2+i*8] = 1
            self.out_mid_col[5+i*8] = 1
            
            # rows
            self.centre_row[32+i] = 1
            self.centre_row[24+i] = 1
            
            self.out_mid_row[40+i] = 1
            self.out_mid_row[16+i] = 1
            
            # long diag
            self.long_1_diag[0+9*i] = 1
            self.long_1_diag[7+7*i] = 1
            
        for i in range(7):
            # 2nd long diags
            self.long_2_diag[1+9*i] = 1
            self.long_2_diag[8+9*i] = 1
            
            self.long_2_diag[6+7*i] = 1
            self.long_2_diag[15+7*i] = 1
            
        for i in range(6):
            # 3rd long diags
            self.long_3_diag[2+9*i] = 1
            self.long_3_diag[16+9*i] = 1
            
            self.long_3_diag[5+7*i] = 1
            self.long_3_diag[23+7*i] = 1
            
            
        # longest diagonals 
        self.w_side = np.zeros(64,dtype='byte')
        #self.b_side = np.zeros(64,dtype='byte') 
        
        for i in range(32):
            self.w_side[i] = 1
            
        self.b_side = 1 - self.w_side
            
            
        self.mid_row = np.bitwise_or(self.centre_row,self.out_mid_row)   
        self.mid_col = np.bitwise_or(self.centre_col,self.out_mid_col)   
            
        self.mid = np.bitwise_and(self.mid_row,self.mid_col)
        self.centre = np.bitwise_and(self.centre_row,self.centre_col)
        self.mid_rc = np.bitwise_or(self.mid_row,self.mid_col)
        
        self.w_mid = np.bitwise_and(self.w_side, self.mid)
        self.b_mid = np.bitwise_and(self.b_side, self.mid)
            
            
if __name__ == '__main__': 
    bd = board_divide()       
         