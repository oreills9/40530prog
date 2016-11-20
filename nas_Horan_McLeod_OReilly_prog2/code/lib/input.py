from lib.globals import Globals
from lib.output_object import OutputObject

class Input:

    def __init__(self, input_file):
        '''
        Input:
        File with following format:
        Line 1: Matrix size
        Line 2-N: N double values
        Line N+2: N values for B vector
        Output:
        Dictionary with format:
        {"val": [], "col": [], "row_start": [], "B" = [], "N" = 0.0}
        :param input_file: File with matrix, b vector
        :param output_file: Location of output file
        '''
        self.input_file = Globals.FILE_DIR + '/' + input_file
    def row_iterator(self):
        res = OutputObject()
        csr = {"val": [], "col": [], "row_start": [], "B": [], "N": 0.0}
        line_count = 0
        with open(self.input_file, "r") as infile:
            for line in infile:
                ## Get line in list format, remove carriage returns and commas
                formatted_line = ([float(x) for x in line.rstrip().rsplit(',')])
                ## The first line is the matrix size so not part of the matrix
                if line_count == 0:
                    csr["N"] = formatted_line[0]
                    if (csr["N"] == 0.0):
                        res.stopReason = Globals.STOP_REASON_ZERO_MATRIX
                        res.exit_state = True
                        return(res)
                ## The last line is the vector B
                elif line_count == csr["N"] + 1:
                    csr["B"] = formatted_line
                    if (len(csr['B']) != csr["N"]):
                        res.stopReason = Globals.STOP_REASON_INVALID_MATRIX
                        res.exit_state = True
                        return (res)
                ## All other lines are part of the matrix
                else:
                    ## Validate row length and matrix row requirements
                    row_check = self.row_check(formatted_line, line_count - 1, csr["N"])
                    if row_check.exit_state:
                        # This means there was an error so just write the output file
                        return(row_check)
                    ## Create CSR dict as we iterate through the lines
                    csr = self.convert_csr(csr, formatted_line)
                line_count += 1
            csr["row_start"].append(len(csr["val"]) + 1)
        res.exit_state = False
        res.csr = csr
        return(res)

    def row_check(self, row, row_number, N):
        '''
        :param row: String containing row elements
        :param row_number: Num of current row
        :param N: Size of matrix
        :return:
        '''
        running_sum = 0
        d = 0
        res = OutputObject()

        if (len(row) != N):
            res.stopReason = Globals.STOP_REASON_INVALID_MATRIX
            res.exit_state = True
            return (res)
        for i in range(int(N)):
            elem = row[i]
            if i == row_number:
                d = abs(elem)
                if elem == 0.0:
                    res.stopReason = Globals.STOP_REASON_ZERO_DIAGONAL
                    res.exit_state = True
                    return (res)
            else:
                running_sum += abs(elem)
        if (d < running_sum) and Globals.CHECK_DIAG:
            res.stopReason = Globals.STOP_REASON_NOT_DIAG_DOM
            res.exit_state = True
            return (res)
        res.exit_state = False
        return(res)

    def convert_csr(self, csr, row_contents):
        '''
        :param csr: Compressed Sparse Row format matrix
        :param row_contents: row element to put in CSR format
        :return:
        '''
        ## As strictly diagonally dominant, can assume each row has at least one elem.
        #print(len(csr["col"]) + 1)
        csr["row_start"].append(len(csr["col"]) + 1)

        for index, item in enumerate(row_contents):
            ## if the entry is zero then just move on
            if item == 0.0:
                continue
            else:
                ## The val will contain all non zero entries
                csr["val"].append(item)
                ## Index will restart for each row
                ## Want to add 1 so we dont start at 0
                csr["col"].append(index + 1)
        return csr