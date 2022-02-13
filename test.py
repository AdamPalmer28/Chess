# test


#%% Properties
import time
import numpy as np

def timer(func):
    def wrapper(*args):
        before = time.time()
        val = func(*args)
        print("Function tooks:", np.round(time.time() - before,4), " seconds")
        return val
    return wrapper

@timer
def test_run(p):
    sum_val = 0
    for i in range(10**p+1):
        sum_val += i
    return sum_val

print(test_run(6))
#%%
test_list = []
for i in range(10):
    test_list.append(i)
    
    if i == 6:
        result = test_list

#print(result)

# %% speed test


array = np.zeros(64,dtype='byte') 

array[45]== 1
array[63]== 1
before = time.time()
for i in range (100000):
    for i in array.nonzero():
        2*i
array = (time.time()-before)


before2 = time.time()

list_test = [45,63]
for i in range (100000):
    for i in list_test:
        2*i
list_time = (time.time()-before2)

print(list_time - array)


# %% move list
def ind_to_square(index):
    letter = ['A','B','C','D','E','F','G','H']
    square = letter[index % 8] + str((index // 8) +1)
    return square

def move_script(move):
    pass

