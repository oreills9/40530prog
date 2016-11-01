import numpy as np

def SOR(filename):
    file = open(filename)
    n = int(file.readline()) #catch NaN exception
    M = np.zeros(shape = (n,n))
    val = np.array(file.readline())
    col = np.array(file.readline())
    rowstart = np.array(file.readline())
    print(n)
    print(val)
    print(col)
    print(rowstart)
    M = populatematrix(n, val, col, rowstart)
    print(M)
    
def iteratematrix(M, val, col, rowstart):
    for i to rowstart-1:
        
    
    
    return M
    

    
SOR("nasSOR.in")
        
    
    