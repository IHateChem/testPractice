import numpy as np
import time as tm
import sys
import math

sys.setrecursionlimit(100000000)


def read_file(file_name): #reading file and return input array
    '''
    Parameters
      ----------
      file_name: str, the path of the file

      Returns
      ----------
      sotre: list used in inputdata of selection algorithm
      num : int that used in num th order we want to find
    '''
    f = open(file_name, 'r')
    num = 0
    store = []
    arr_len = int(f.readline().rstrip())
    for i in f.readline().rstrip().split():
        store.append(int(i))
    num = int(f.readline().rstrip())
    return arr_len,store, num



def random_Select(arr, p , r, i):
    '''
    Parameters
      ----------
      arr: list which have to be selected
      p  : index for starting selection
      r  : index for finishing selection
      i  : ith order we want to find

      Returns
      ----------
      arr[q]: ith value'''
    if p == r:
        return arr[p]
    q = random_partition(arr, p, r)
    k = q - p + 1
    if i < k:
        return random_Select(arr,p,q-1,i)
    elif i == k:
        return arr[q]
    else: 
        return random_Select(arr,q+1,r,i-k)
    
def random_partition(arr,p,r,):
    i = np.random.randint(p,r+1)
    arr[i], arr[r] = arr[r], arr[i]
    return partition(arr, p, r)

def partition(arr, p, r):
    x = arr[r]
    i = p - 1
    for j in range(p,r):
        if x >= arr[j]:
            i += 1
            arr[i] , arr[j] = arr[j], arr[i]
    arr[i+1] , arr[r] = arr[r] , arr[i+1]
    return i+1



def deter_select(arr,n, k):
    '''
    deternimistic selection algorithms
    Parameters
      ----------
    list arr: input data 
    int n: size of input data 
    int k: kth order we want to find
      Returns
      ----------
    int k th element in arr
     '''
    if n  <= 5:
        t_arr = insertionsort(arr)
        return t_arr[k-1]
    ceil_n = math.ceil(n/5)
    m = []

    # splitting array
    for i in range(ceil_n-1):
        m.append(insertionsort(arr[i*5:i*5+5])[2]) #same as m.append(deter_select(arr[i*5:i*5+5],5,3))
    n_5 = 5 if n%5 ==0 else n%5
    m.append(insertionsort(arr[n-n_5 -1:n])[math.floor((n_5-1)/2)]) #same as m.append(deter_select(arr[n-n_5 -1:n],n_5,math.floor((ceil_n-1)/2)))

    #find median of median
    pivot = deter_select(m,ceil_n,math.floor((ceil_n-1)/2))

    #pivotting
    pivot_index = arr.index(pivot)
    arr[pivot_index] ,arr[n-1] = arr[n-1], arr[pivot_index]

    #partitioning
    q = partition(arr,0,n-1)
    i = q  + 1
    if i == k:
        return arr[q]
    elif i> k:
        return deter_select(arr[:q],q,k)
    else:
        return deter_select(arr[q+1:],n-q-1,k-i)


def insertionsort(arr):
    '''
    insertionsort used in deter_select
    Parameters
      ----------
    list arr: input data
      Returns
      ----------
    list arr: sorted arr
    '''
    n = len(arr)
    if n == 1:
        return arr
    else:
        for i in range (1, n):
            key = arr[i]
            jj = i
            for j in range(i,0,-1):      
                if arr[j-1] <=  key:        
                    break
                arr[j] = arr[j-1]
                jj = j-1 
            arr[jj] = key
    return arr


def checker(input_data, k, answer): #input: (input, k), answer
    answer_data = seok_selection(input_data,k)
    return answer == answer_data

    

def seok_selection(arr,n, k):
    '''
    checking algorithm
    Parameters
      ----------
    list arr: input data
    int n   : size of input
    int k   : k th order
      Returns
      ----------
    int k th element in arr
    '''
    arr1_n = 0
    Sum = 0
    Iter = 0
    if n == 1:
        return arr[k-1]
    m = max(arr)
    if 2*n < m:
        arr_negative = [0]*n
        arr_negative_big = []
        isnegative = False
        arr_1 = [0]*(2*n)
        arr_2 = [[]]*n #(math.ceil((m-2*n)/5/n**int(math.log(m,n)-1))+1)
        for element in arr:
            if element < 0:
                isnegative = True
                if element > -1 * n:
                    arr_negative[-element-1] += 1
                else:
                    arr_negative_big.append(element)
            elif element < 2*n:
                arr_1[element] += 1
                arr1_n += 1
            else:
                arr_2[math.floor((element-2*n)/m*n)].append(element)
        if isnegative: ###음수가 있을경우
            if k <= len(arr_negative_big):
                p = 0
                r = len(arr_negative_big)-1
                kk = k -Sum
                while True:
                    q = partition(arr_negative_big,p,r)
                    i = q - p +1
                    if i == kk:
                        return arr_negative_big[q]
                    elif i > kk:
                        r = q - 1
                    else:
                        p = q + 1
                        kk = kk - i
            else:
                Sum += len(arr_negative_big)
                for i in range(n-1,-1,-1):
                    Sum += arr_negative[i]
                    if Sum >= k:
                        return -i -1
        if arr1_n > k: 
            for num in arr_1:
                Sum += num
                Iter += 1
                if Sum >= k:
                    return Iter -1
        else:
            Sum += arr1_n
        for element in arr_2:
            len_n = len(element)
            Sum += len_n
            if Sum >= k:
                p = 0 
                r = len_n-1
                kk = k -Sum + len_n
                while True:
                    q = partition(element,p,r)
                    i = q - p +1
                    if i == kk:
                        return element[q]
                    elif i > kk:
                        r = q - 1
                    else:
                        p = q + 1
                        kk = kk - i

    else:  ###음수가 있을경우
        arr_1 = [0]*(m+1)
        arr_negative = [0]*n
        arr_negative_big = []
        isnegative = False
        for element in arr:
            if element >= 0:
                arr_1[element] += 1
            else:
                isnegative = True
                if element > -1 * n:
                    arr_negative[-element-1] += 1
                else:
                    arr_negative_big.append(element)
        if isnegative:
            if k <= len(arr_negative_big):
                p = 0
                r = len(arr_negative_big)-1
                kk = k -Sum
                while True:
                    q = partition(arr_negative_big,p,r)
                    i = q - p +1
                    if i == kk:
                        return arr_negative_big[q]
                    elif i > kk:
                        r = q - 1
                    else:
                        p = q + 1
                        kk = kk - i
            else:
                Sum += len(arr_negative_big)
                for i in range(n-1,-1,-1):
                    Sum += arr_negative[i]
                    if Sum >= k:
                        return -i -1
        for num in arr_1:
            Sum += num
            Iter += 1
            if Sum >= k:
                return Iter-1


