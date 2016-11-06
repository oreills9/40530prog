import math
import sys

## Allowable reasons for exiting process
STOP_REASON_X_SEQ_CON = 'x Sequence Convergence'
STOP_REASON_RES_CON = 'Residual Convergence'
STOP_REASON_MAX_ITS = 'Max Iterations Reached'
STOP_REASON_DIVERGENCE = 'x Sequence Divergence'    
STOP_REASON_ZERO_DIAGONAL = 'Zero On Diagonal'
STOP_REASON_OTHER = 'Cannot Proceed'
STOP_REASON_ZERO_MATRIX = 'Zero Matrix Size'
STOP_REASON_INVALID_MATRIX = 'Invalid Matrix Input'
STOP_REASON_NOT_DIAG_DOM = 'Matrix Not Diagonally Dominant'


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
                    return_results(stopReason = STOP_REASON_ZERO_MATRIX)
                    return
            ## The last line is the vector B
            elif line_count == csr["N"] + 1:
                csr["B"] = formatted_line
                if (len(csr['B']) != csr["N"]):
                    return_results(stopReason = STOP_REASON_INVALID_MATRIX)
                    return
            ## All other lines are part of the matrix
            else:
                ## Validate row length and matrix row requirements
                row_check(formatted_line,line_count-1,csr["N"])
                ## Create CSR dict as we iterate through the lines
                csr = convert_csr(csr, formatted_line)

            line_count +=1

            ## Check line count N+2
    return(csr)

def row_check(row,row_number,N):
    running_sum = 0
    d = 0

    if(len(row)!= N):
        return_results(stopReason = STOP_REASON_INVALID_MATRIX)
        return

    for i in range(row_number):
        elem = row[i]
        if i == row_number:
            d = abs(elem)
            if elem == 0.0:
                return_results(stopReason = STOP_REASON_ZERO_DIAGONAL)
                return
        else:
            running_sum += abs(elem)
    
    if d < running_sum: 
        return_results(stopReason = STOP_REASON_NOT_DIAG_DOM)
        return

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

def sor_calc(csr,maxits,tol,omega):
    its = 0

    ## What does convergence?
    while converging and its <= maxits:
        x_zero = guess_x()
        x_one = new_x(x_zero,csr,omega)

        if vector_norm(x_one) - vector_norm(x_zero) < "tol formula involving mach eps":
            return_results(output_file, stopReason="Converted")
            return
        else: 
            converging = convergence_check(new_x)

    ## returns stop reason num its and x

def new_x(current,csr,omega):
    for i in range(csr["N"]):
        ssum = sor_sum(initial,csr)
        d = get_diagonal(csr,i)
        current[i] += (omega * ((csr["B"][i]) - ssum)/d)
    return current

def sor_sum(initial,csr):
    ## it gets sum excluding diagonal * x
    ## retuns this 
    ## Cian
    return

def get_diagonal():
    ## Cian
    return

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

def convergence_check():
    ## Cathal
    ## returns true if going good (converging towards a point)
    ## false if diverging
    ## vecrtor norm
    ## has to hold previous values
    ## check for diverging
    ## check for converging but not converged
    return

def get_input_file():
    ## Check if input filename is provided, if not default to 'nas_Sor.in'
    filename = 'nas_Sor.in' if len(sys.argv) < 2 else sys.argv[2]
    print(filename)        
    return filename
    
def get_output_file():
    ## Check if output filename is provided, if not default to 'nas_Sor.out'    
    filename = 'nas_Sor.out' if len(sys.argv) < 3 else sys.argv[3]
    print(filename)        
    return filename
    
def return_results(num_its = 0, x = None, stopReason = None, e = 0, max_its = 0, x_seq_tol = 0, res_seq_tol = 0):
    ## Confirm the filename of the output text    
    output_file = get_output_file()  
    
    ## Write out lines (with padding, when necessary)
    file = open(output_file, 'w')
    headings = 'Stopping Reason | Max No. of Iterations | Number of Iterations | Machine Epsilon | X Sequence Tolerance | Residual Sequence Tolerance'
    print(headings)
    results = stopReason + ' ' + str(max_its) + ' ' + str(num_its) + ' ' + str(e) + ' ' + str(x_seq_tol) + ' ' + str(res_seq_tol)
    print(results)
    file.write(headings)
    file.write(results)
    
    if stopReason in (STOP_REASON_X_SEQ_CON, STOP_REASON_RES_CON, STOP_REASON_MAX_ITS ):
        ## Only print results when appropriate to do so        
        print(x)
        file.write(x)
    file.close()
    sys.exit()

if __name__ == '__main__':
    ## First confirm the file to read the data from
    input_file = get_input_file()
    
    csr = row_iterator(input_file)
    #csr = row_iterator('input_file_1.txt')
    print(csr)
    norm = vector_norm([1, 2, 3])
    print(norm)
