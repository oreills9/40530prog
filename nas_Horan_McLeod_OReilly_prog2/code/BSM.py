#BSM.py

def BSM(Smax, T ,theta, r, k = 1):
    csr = populate_matrix(Smax, T, theta, r, k)
    print(csr)
    
    
def populate_matrix(Smax, T, theta, r, k):
    csr = {"val": [], "col": [], "row_start": [], "B": [], "N": 0.0}
    dim = int(k * T)    
    csr["N"] = dim
    csr["row_start"].insert(0, (dim * 3) - 1) #fill last value for rowstart
    for n in range (dim, 0, -1):
        entry_count = 0
        #populate 3rd equation for all rows, bar the last row in the matrix        
        if n != dim:
            
            csr["col"].insert(0, n + 1)
            csr["val"].insert(0, tridiagfuture(n, dim, theta, r) )
            entry_count += 1 
    
        #populate 2nd equation for all rows            
        csr["col"].insert(0, n)
        csr["val"].insert(0, tridiagcurrent(n, dim, theta, r) )
        entry_count += 1
        
        #populate 1st equation for all rows, bar the first row in the matrix
        if n != 1:
            csr["col"].insert(0, n - 1)
            csr["val"].insert(0, tridiagfuture(n, dim, theta, r) )
            entry_count += 1
        
        csr["row_start"].insert(0, csr["row_start"][0] - entry_count)        
        csr["B"].insert(0, Smax)
            
    return csr
    
def tridiagprevious(n, t, theta, r): #-nk/2(n*o2) - r
    return -n * ((t/(n - 1)) / 2) * ( (n * (theta ** 2)) - r) 
    
def tridiagcurrent(n, t, theta, r): # 1 + kr + ko2n2
    return 1 + ((t / n) * r) + ((t / n) * (theta ** 2) * (n ** 2) )
    
def tridiagfuture(n, t, theta, r): #-nk/2(n*o2) + r
    return -n * ((t/(n + 1)) / 2) * ( (n * (theta ** 2)) + r)
  
if __name__ == '__main__':
    BSM(160, 5 ,0.2, 0.01, 1)

    