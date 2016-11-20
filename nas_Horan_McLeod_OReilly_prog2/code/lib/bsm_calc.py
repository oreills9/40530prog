class BsmCalc:
    '''
    :param Smax: price of option
    :param T: maturity date
    :param theta: volatility of stock
    :param r: risk-free rate of interest
    :param k: time-steps (intervals)
    :return:
    '''
    
    def __init__(self, Smax, T, theta, r, intervals):
        self.Smax = Smax
        self.T = T
        self.theta = theta
        self.r = r
        self.intervals = intervals
		
    def bsm_calc(self):
        csr = {"val": [], "col": [], "row_start": [], "B": [], "N": 0.0}
        dim = int((self.intervals * self.T) - 1)
        csr["B"].insert(0, self.Smax)    
        csr["N"] = dim
        csr["row_start"].insert(0, (dim * 3) - 1) #fill last value for rowstart
        k = self.T / dim
		
        previous = 0
        present = 0
        future = 0
        bValue = self.Smax
        for n in range (dim, 0, -1):
            entry_count = 0
            #populate 3rd equation for all rows, bar the last row in the matrix        
            future = self.tridiagfuture(n, k)            
            if n != dim:
                csr["col"].insert(0, n + 1)
                csr["val"].insert(0, future)
                entry_count += 1 
		
            #populate 2nd equation for all rows
            csr["col"].insert(0, n)
            present = self.tridiagpresent(n, k)
            csr["val"].insert(0, present)
            entry_count += 1
			
            #populate 1st equation for all rows, bar the first row in the matrix
            previous = self.tridiagprevious(n, k)            
            if n != 1:
                csr["col"].insert(0, n - 1)
                csr["val"].insert(0, previous)
                bValue = bValue / (previous + present + future) 
                csr["B"].insert(0, bValue)
                entry_count += 1
			
            csr["row_start"].insert(0, csr["row_start"][0] - entry_count) 
				
        return csr

    def tridiagprevious(self, n, k):
        '''
	   :param n: nth row of matrix
        :param t: k/T  
        :param theta: volatility
        :param r: risk-free rate of interest
        :return: result of 1st equation of BSM
        '''
        return   ( (-n * k ) / 2 ) * ( (n * (self.theta ** 2)) - self.r )
    
    def tridiagpresent(self, n, k):
         '''
         :param n: nth row of matrix
         :param t: k/T  
         :param theta: volatility
         :param r: risk-free rate of interest
         :return: result of 2nd equation of BSM
         '''
         return 1 + (k * self.r) + (k * (self.theta ** 2) * (n ** 2) )
    
    def tridiagfuture(self, n, k):
         '''
         :param n: nth row of matrix
         :param t: k/T  
         :param theta: volatility
         :param r: risk-free rate of interest
         :return: result of 3rd equation of BSM
         '''
         return  ( (-n * k ) / 2 ) * ( (n * (self.theta ** 2)) + self.r )