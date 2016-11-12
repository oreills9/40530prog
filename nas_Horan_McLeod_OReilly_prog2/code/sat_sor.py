import math
import numpy as np
import sys
import doctest

## Allowable reasons for exiting process
STOP_REASON_X_SEQ_CON = 'x Sequence Convergence'
STOP_REASON_RES_CON = 'Residual Convergence'
STOP_REASON_MAX_ITS = 'Max Iterations Reached'
STOP_REASON_DIVERGENCE = 'x Sequence Divergence'    
STOP_REASON_ZERO_DIAGONAL = 'Zero On Diagonal'
STOP_REASON_OTHER = 'Cannot Proceed'
STOP_REASON_ZERO_MATRIX = 'Zero Matrix Size'
STOP_REASON_INVALID_MATRIX = 'Invalid Matrix Input'
STOP_REASON_NOT_DIAG_DOM = 'Not Diagonally Dominant'

Em = np.finfo(float).eps
E = 1.0e-3

def get_tol(x):
    print('TEST' + str(E) )
    tolerance = E + ( (4 * Em) * abs(x) )
    return tolerance
    
def row_iterator(input_file):
    '''
    Input:
    File with following format:
    Line 1: Matrix size
    Line 2-N: N double values
    Line N+2: N values for B vector
    Output:
    Dictionary with format:
    {"val": [], "col": [], "row_start": [], "B" = [], "N" = 0.0}
    '''

    csr = {"val": [], "col": [], "row_start": [], "B": [], "N": 0.0}

    ## We want to perform as many of the checks and functions during
    ## the single iterations as possible. As we iterate through the input
    ## file we need populate the csr dict with the matrix size and the
    ## matrix values in csr format and the B vector on the last line
    line_count = 0
    with open(input_file, "r") as infile:
        for line in infile:
            ## Get line in list format, remove carriage returns and commas
            formatted_line = ([float(x) for x in line.rstrip().rsplit(',')])

            ## The first line is the matrix size so not part of the matrix
            if line_count == 0:
                csr["N"] = formatted_line[0]
                if (csr["N"] == 0.0):
                    output_results(STOP_REASON_ZERO_MATRIX, 100, 1, 1)
            ## The last line is the vector B
            elif line_count == csr["N"] + 1:
                csr["B"] = formatted_line
                if (len(csr['B']) != csr["N"]):
                    output_results(STOP_REASON_INVALID_MATRIX, 100, 1, 1)
            ## All other lines are part of the matrix
            else:
                ## Validate row length and matrix row requirements
                row_check(formatted_line,line_count-1,csr["N"])
                ## Create CSR dict as we iterate through the lines
                csr = convert_csr(csr, formatted_line)

            line_count +=1
        csr["row_start"].append(len(csr["val"])+1)
            ## Check line count N+2
    return(csr)

def row_check(row,row_number,N):
    running_sum = 0
    d = 0

    if(len(row)!= N):
        output_results(STOP_REASON_INVALID_MATRIX, 100, 1, 1)

    for i in range(int(N)):
        elem = row[i]
        if i == row_number:
            d = abs(elem)
            if elem == 0.0:
                output_results(STOP_REASON_ZERO_DIAGONAL, 100, 1, 1)
        else:
            running_sum += abs(elem)
    
    if d < running_sum: 
        output_results(STOP_REASON_NOT_DIAG_DOM, 100, 1, 1)

def convert_csr(csr, row_contents):
    ## As strictly diagonally dominant, can assume each row has at least one elem.
    print(len(csr["col"])+1)
    csr["row_start"].append(len(csr["col"])+1)

    for index, item in enumerate(row_contents):
        ## if the entry is zero then just move on
        if item == 0.0:
            continue

        else:
            ## The val will contain all non zero entries
            csr["val"].append(item)
            ## Index will restart for each row
            ## Want to add 1 so we dont start at 0
            csr["col"].append(index+1)

    return csr

def sor_calc(csr,maxits,omega):
        
    reason = ''
    x_zero = guess_x(csr["N"])
    x_zero_norm = 0
    ## What does convergence?
    for i in range (0, maxits):
        x_one = new_x(x_zero,csr,omega)
        x_one_norm = vector_norm(x_one)
        res_norm = residual_norm(csr,x_one)
        xSeqTol = get_tol(x_one_norm)
        resSeqTol = get_tol(res_norm)
        
        if x_one_norm - x_zero_norm < xSeqTol:
            reason = STOP_REASON_DIVERGENCE
        elif res_norm < resSeqTol:
            reason = STOP_REASON_RES_CON
            
        else: 
            converging = convergence_check(x_one, x_zero, xSeqTol)
            if converging:
                reason = STOP_REASON_DIVERGENCE
            x_zero = x_one
            x_zero_norm = x_one_norm
        
        if i + 1 >= maxits:
            reason = STOP_REASON_MAX_ITS
        
        if len(reason) > 0:
            output_results(reason, maxits, xSeqTol, resSeqTol, numIts = i, result = x_zero)
    
    ## returns stop reason num its and x
    
def guess_x(i):
    list_zeroes = [0] * int(i)
    return list_zeroes

def new_x(current,csr,omega):
    for i in range(0,int(csr["N"])):
        sor_return = sor_sum(current,csr,i)
        ssum = sor_return["sorSum"]
        d = sor_return["diag"]
        print(sor_return)
        current[i] += (omega/d)*((csr["B"][i]) - ssum)
        print('Current[i] ' + str(current[i]) )
    return current

def sor_sum(current,csr,i):
    ssum = 0
    for j in range(csr["row_start"][i]-1,csr["row_start"][i+1]-1):
        ssum += csr["val"][j]*current[csr["col"][j]-1]
        if csr["col"][j] == i+1:
            d = csr["val"][j]
    return {"sorSum": ssum, "diag": d}

def residual_norm(csr,current):
    product = prod_mat_vec(csr,current)
    res = guess_x(csr["N"])
    
    for i in range(0,int(csr["N"])):
        res[i] = csr["B"][i]-product[i]
    res_norm = vector_norm(res)
    return res_norm

def prod_mat_vec(csr,current):
    prod = guess_x(csr["N"])
    for i in range(0,int(csr["N"])):
        for j in range(csr["row_start"][i]-1,csr["row_start"][i+1]-1):
            prod[i] += csr["val"][j]*current[csr["col"][j]-1]
    return prod

def vector_norm(vector):
    ## Cathal
    ## Calculating length or 2 norm of vector
    val = 0
    for elem in vector:
        val += elem**2
    ## Check for zero vector
    if val == 0:
        return(0)
    else:
        return(math.sqrt(val))

def convergence_check(prev_x, cur_x, tol):
    ## Cathal
    ## returns true if going good (converging towards a point)
    ## false if diverging
    ## vector norm
    ## has to hold previous values
    ## check for diverging
    ## check for converging but not converged
    print(cur_x)
    print(prev_x)
    x_diff = vector_norm(cur_x) - vector_norm(prev_x)
    if x_diff <= tol:
        return False
    else:
        return True

def get_input_file(args):
    """ 
    Checks to see if an input file is provided in the arguments of the class
    and if not, returns the default 'nas_Sor.in' file containing a sample 
    matrix.
    Arguments: None
    Returns: String
    
    
    >>> get_input_file([])
    'nas_Sor.in'
    >>> get_input_file(['sat_sor.py'])
    'nas_Sor.in'
    >>> get_input_file(['sat_sor.py', 'nas_SOR_small_diag_dom.in'])
    'nas_SOR_small_diag_dom.in'
    """

    filename = 'nas_Sor.in' if len(args) < 2 else args[1]
    return filename
    
def get_output_file(args):
    """ 
    Checks to see if an output file is provided in the arguments of the class
    and if not, returns the default 'nas_Sor.out' file which will be populated
    with the output of the Sparse SOR calculation.
    Arguments: None
    Returns: String
    
    >>> get_output_file([])
    'nas_Sor.out'
    >>> get_output_file(['sat_sor.py'])
    'nas_Sor.out'
    >>> get_output_file(['sat_sor.py', 'nas_SOR_small_diag_dom.in'])
    'nas_Sor.out'
    >>> get_output_file(['sat_sor.py', 'nas_SOR_small_diag_dom.in', 'test_output.out'])
    'test_output.out'
    """

    filename = 'nas_Sor.out' if len(args) < 3 else args[2]
    return filename
    
def output_results(stopReason, maxIts, xSeqTol, residualSeqTol, \
                   numIts = None, result = None, epsilon = None):
    """ 
    Outputs the results (or reasons for failure) for the Sparse SOR function 
    to both the output_file() location and the prompt, before exiting the 
    SOR function
    Arguments:  stopReason - The reason for exiting the algorithm.
                maxIts - The number of iterations cycled through.
                xSeqTol - The tolerance between sucsessive x estimations
                residualSeqTol - The error tolerance                
                numIts - The number of iterations cycled through. ('None' if error)
                result - The matrix generated by the SOR formula. ('None' if error)
                epsilon - The machine epsilon number ('None' if error)
    Returns: None
    
    >>> output_results()
    Traceback (most recent call last):
        ...
    TypeError: output_results() missing 4 required positional arguments: 'stopReason', 'maxIts', 'xSeqTol', and 'residualSeqTol'
    
    >>> output_results(STOP_REASON_NOT_DIAG_DOM)
    Traceback (most recent call last):
        ...
    TypeError: output_results() missing 3 required positional arguments: 'maxIts', 'xSeqTol', and 'residualSeqTol'
    
    >>> output_results(STOP_REASON_NOT_DIAG_DOM, 100)
    Traceback (most recent call last):
        ...
    TypeError: output_results() missing 2 required positional arguments: 'xSeqTol' and 'residualSeqTol'
    
    >>> output_results(STOP_REASON_NOT_DIAG_DOM, 100, 1)
    Traceback (most recent call last):
        ...
    TypeError: output_results() missing 1 required positional argument: 'residualSeqTol'
    """
    """    
    >>> output_results(STOP_REASON_NOT_DIAG_DOM, 100, 1, 1)
        Stopping Reason     | Max. Iterations | No. Iterations | Epsilon | X Seq. Tolerance | Res. Seq. Tolerance |
    Not Diagonally Dominant |       100       |      None      |  None   |        1         |          1          |
    """ 
    ## Confirm the filename of the output text    
    output_file = get_output_file(sys.argv)  
    
    ## Open writable file
    file = open(output_file, 'w')
    
    ##Generate headings line
    headings = '     Stopping Reason     | Max. Iterations |' \
                ' No. Iterations | Epsilon |' \
                ' X Seq. Tolerance | Res. Seq. Tolerance |'
    print(headings)
    
    ##Generate formatted stastical data
    stats = "{:^25}|{:^17}|{:^16}|{:^9}|{:^18}|{:^21}|" \
        .format(stopReason, str(maxIts), str(numIts), str(epsilon), str(xSeqTol), str(residualSeqTol) )
    print(stats)
    file.write(headings + '\n')
    file.write(stats + '\n')
    
    if stopReason in (STOP_REASON_X_SEQ_CON, STOP_REASON_RES_CON, STOP_REASON_MAX_ITS ):
        ## Only print results when appropriate to do so        
        print('Results: %s' % result)
        file.write('Results: %s' % result)
    file.close()
    sys.exit(0)

if __name__ == '__main__':
    ##doctest.testmod()
    ## First confirm the file to read the data from
    input_file = get_input_file(sys.argv)
    csr = row_iterator(input_file)
    sor_calc(csr, 100, 1.2) 
    