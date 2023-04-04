import algorithm 
import time as tm
import numpy as np
import math


def MkOutput():
    '''
    function makes ouput files.
    '''
    n, input_data, k = algorithm.read_file("input.txt")
    #Random select
    random_out = random(input_data, 0, n-1, k)
    #Deter Select
    deter_out = deter(input_data, n, k)
    #Checker start
    tm_check_start = tm.time()
    flag_rand, flag_deter = checker(input_data, n, k, random_out, deter_out)
    tm_check_end = tm.time()

    tm_check = tm_check_end - tm_check_start
    with open("result.txt","w") as fc:
        fc.write("Checking Start....\n")
        fc.write("Random_Check: {} \n".format(flag_rand))
        fc.write("Deter_Check: {} \n".format(flag_deter))
        fc.write("Checking Finish... It takes {}  ms ".format(str(int(round(tm_check*1000)))))
    fc.close()

    
def random(data,p,r, k):
    '''
    making random.txt and return answer
    ''' 
    input_data = data[:]
    t_start = tm.time()
    q = algorithm.random_Select(input_data,p,r,k)
    t_end = tm.time()
    with open("random.txt", "w") as f:
        f.write(str(q)+"\n")
        f.write(str(int(round((t_end-t_start)*1000)))+"ms")
        f.close()
    return q

def deter(data,n, k):
    '''
    making deter.txt and return answer
    '''
    input_data = data[:]
    t_start = tm.time()
    q = algorithm.deter_select(input_data,n,k)
    t_end = tm.time()
    with open("deter.txt", "w") as f:
        f.write(str(q)+"\n")
        f.write(str(int(round((t_end-t_start)*1000)))+"ms")
        f.close()
    return q
 
def checker(data,n, k,random_out, deter_out ):
    '''
    result
    ------ 
    bool flag_rand: correctness of rand algorithm , bool flag_deter: correctness of deter algorithm
    '''
    answer = algorithm.seok_selection(data,n, k)
    flag_rand= answer == random_out
    flag_deter = answer == deter_out
    return flag_rand, flag_deter
MkOutput()
