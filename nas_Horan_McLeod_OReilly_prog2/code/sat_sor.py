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

    infile = open(input_file, "r")
    csr = {"val": [], "col": [], "row_start": [], "B" = [], "N" = 0.0}

    ## We want to perform as many of the checks and functions during
    ## the single iterations as possible. As we iterate through the input
    ## file we need populate the csr dict with the matrix size and the
    ## matrix values in csr format and the B vector on the last line
    line_count = 0
    for line in infile:
        ## Get line in list format, remove carriage returns and commas
        formatted_line = ([float(x) for x in line.rstrip().rsplit(',')])

        ## The first line is the matrix size so not part of the matrix
        if line_count == 0:
            csr["N"] = formatted_line[0]
            if (csr["N"] == 0.0):
                output_file(stop_reson = "Zero Matix Size")
                return
        ## The last line is the vector B
        elif line_count == csr["N"] + 1:
            csr["B"] = formatted_line
            if (len(B) !== csr["N"]):
                output_file(stop_reson = "Corrupt B")
                return
        ## All other lines are part of the matrix
        else:
            ## Validate row length and matrix row requirements
            row_check(formatted_line,line_count-1,csr["N"])
            ## Create CSR dict as we iterate through the lines
            csr = convert_csr(csr, formatted_line)

        line_count +=1

        ## Check line count N+2

def row_check(row,row_number,N):
    running_sum = 0

    if(len(row)!== N):
        output_file(stop_reson = "Not enough elements on row")
        return

    for i in range(row_number):
        elem = row[i]
        if i == row_number:
            d = abs(elem)
            if elem == 0.0:
                output_file(stop_reson = "Zero on diagonal")
                return
        else:
            running_sum += abs(elem)
    
    if d < running_sum: 
        output_file(stop_reson = "Not strictly diagonal dominant")
        return

def convert_csr(csr, row_contents):
    ## As strictly diagonally dominant, can assume each row has at least one elem.
    csr["row_start"].append(len(csr["col"]+1))

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
            output_file(stop_reson = "Converted")
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

def get_diagonal():
    ## Cian

def vector_norm(vector):
    ## Cathal

def convergence_check():
    ## Cathal
    ## returns true if going good (converging towards a point)
    ## false if diverging
    ## vecrtor norm
    ## has to hold previous values
    ## check for diverging
    ## check for converging but not converged

def output_file(num_its = 0, x = None, stop_reson = None):
    print("Output file contents")
    ## Stephen
    ## call sys.exit

