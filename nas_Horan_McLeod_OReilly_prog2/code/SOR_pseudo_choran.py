import os
MATRIX_SIZE = 0
VALUES = 1
COLUMNS = 2
ROW_START = 3
VECTOR = 4

def sor(input_file):
    #Read input file
    file_contents = read_input_file(input_file)
    m = int(file_contents[MATRIX_SIZE].rstrip())
    csr = get_csr(file_contents)
    b = file_contents[VECTOR].rstrip().rsplit(',')

    #Set initial conditions
    w = 1.25
    maxits = 100
    x = [val for val in [0] * m]
    epsilon = get_epsilon()
    for i in range(size):
        row_sum, diag, total =0
        # Then we go through the column entries for that row
        for j in range(csr['row_start'][i], csr['row_start'][i+1]-1):
            #If it is zero then there wont be any diag?
            if i == csr['cols'][j]:
                diag = csr['vals'][csr['row_start'][i]]
                check_for_diagonal(diag)
            else:
                row_sum += csr['vals'][j]
        check_for_row_dominance(row_sum, diag)

    return(True)

def check_for_row_dominance(r_sum, diagonal=0):
    check_for_diagional(diagonal)
    if r_sum < diagonal:
        return('Not row diagonal dominant')

def check_for_diagional(diag):
    if diag == 0:
        return('Zero on diagonal')

def get_x_value(size, csr):
    # Verify that matrix is
    # 1/ Diagonally dominant
    # 2/ Has non-zeo diagonal values
    # 3/ Is Symmetric positive
    # Start by iterating through the rows
    for i in range(size):
        print("ROW: %s" % i)
        sum =0
        diag=0
        total=0
        # Then we go through the column entries for that row
        for j in range(csr['row_start'][i], csr['row_start'][i+1]-1):
            #print('rs %s' % csr['row_start'][i])
            #print('re %d' % (csr['row_start'][i+1] -1))
            #print('cols %d' % csr['cols'][j])
            print('val %s' % csr['vals'][j])
            if i == csr['cols'][j]:
                if csr['vals'][csr['row_start'][i]] == 0:
                    return('Zero on diagonal')
                else:
                    diag=csr['vals'][j]
                    print('diag %s' % diag)
            else:
                sum += csr['vals'][j]
                total += sum * x[j]
        if sum>diag:
            print(sum, diag)
            return('Not row diagonal dominant')
    return(True)

def read_input_file(file):
    with open(file) as f:
        lines = f.readlines()
        return(lines)

def get_csr(file_list):
    result = {}
    result['vals'] = ([int(x) for x in file_list[VALUES].rstrip().rsplit(',')])
    result['cols'] = ([int(x) for x in file_list[COLUMNS].rstrip().rsplit(',')])
    result['row_start'] = ([int(x) for x in file_list[ROW_START].rstrip().rsplit(',')])
    return(result)

if __name__ == '__main__':
    sor('/Users/cathalhoran/sor1.txt')
