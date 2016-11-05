## MATRIX_SIZE 0 as first file of line
MATRIX_SIZE = 0

def row_iterator(input_file):
    infile = open(input_file, "r")
    
    csr = {"val": [], "col": [], "row_start": [], "B" = [], "N" = 0.0}

    line_count = 0
    for line in infile:
        formatted_line = ([float(x) for x in line.rstrip().rsplit(',')])
        
        if line_count == 0:
            csr["N"] = formatted_line[0]
            if (N == 0.0):
                output_file(stop_reson = "Zero Matix Size")
                return
        elif line_count == N+1 
            csr["B"] = formatted_line
            if (len(B) !== N):
                output_file(stop_reson = "Corrupt B")
                return
        else:
            row_check(formatted_line,line_count-1,csr["N"])
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
    ## As strictly diaganolly dominant, can assume each row has at least one elem.
    csr["row_start"].append(len(csr["col"]+1))

    for index, item in enumerate(row_contents):
        if item == 0.0:
            continue
        else:
            csr["val"].append(item)
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

