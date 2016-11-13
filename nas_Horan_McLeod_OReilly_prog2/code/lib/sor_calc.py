import math
from lib.globals import Globals
from lib.output import Output

class SorCalc:
    '''
     :param csr: dict in CSR format
     :param maxits: max num of iterations
     :param omega: relaxation factor
     :return:
    '''
    def __init__(self, csr, maxits, omega, output_file):
        self.maxits = maxits
        self.csr = csr
        self.omega = omega
        self.output_file = output_file

    def sor_calc(self):
        output_file = Output()
        reason = ''
        x_zero = self.guess_x(self.csr["N"])
        x_zero_norm = 0
        ## What does convergence?
        for i in range(0, self.maxits):
            x_one = self.new_x(x_zero)
            x_one_norm = self.vector_norm(x_one)
            res_norm = self.residual_norm(x_one)
            xSeqTol = self.get_tol(x_one_norm)
            resSeqTol = self.get_tol(res_norm)

            if x_one_norm - x_zero_norm < xSeqTol:
                reason = Globals.STOP_REASON_DIVERGENCE
            elif res_norm < resSeqTol:
                reason = Globals.STOP_REASON_RES_CON

            else:
                converging = self.convergence_check(x_one, x_zero, xSeqTol)
                if converging:
                    reason = Globals.STOP_REASON_DIVERGENCE
                x_zero = x_one
                x_zero_norm = x_one_norm

            if i + 1 >= self.maxits:
                reason = Globals.STOP_REASON_MAX_ITS

            if len(reason) > 0:
                output_file.output_results(self.output_file, reason, self.maxits, xSeqTol, resSeqTol, \
                                           numIts=i, result=x_zero)

    def guess_x(self, i):
        '''
        Initial guess for x vector
        :return: list of zeros corresponding to matrix size
        '''
        list_zeroes = [0] * int(i)
        return list_zeroes

    def new_x(self, current):
        '''
        :param current: current X vector
        :return: new X vector
        '''
        for i in range(0, int(self.csr["N"])):
            sor_return = self.sor_sum(current, i)
            ssum = sor_return["sorSum"]
            d = sor_return["diag"]
            print(sor_return)
            current[i] += (self.omega / d) * ((self.csr["B"][i]) - ssum)
            print('Current[i] ' + str(current[i]))
        return current

    def sor_sum(self, current, i):
        '''

        :param current: current X vector
        :param i: location in row
        :return: dict with digonal value and row sum
        '''
        ssum = 0
        for j in range(self.csr["row_start"][i] - 1, self.csr["row_start"][i + 1] - 1):
            ssum += self.csr["val"][j] * current[self.csr["col"][j] - 1]
            if self.csr["col"][j] == i + 1:
                d = self.csr["val"][j]
        return {"sorSum": ssum, "diag": d}

    def residual_norm(self, current):
        '''
        Calculate residual error
        :param current: current X vector
        :return:
        '''
        product = self.prod_mat_vec(current)
        res = self.guess_x(self.csr["N"])

        for i in range(0, int(self.csr["N"])):
            res[i] = self.csr["B"][i] - product[i]
        res_norm = self.vector_norm(res)
        return res_norm

    def prod_mat_vec(self, current):
        '''
        :param current: current X vector
        :return: list of product values
        '''
        prod = self.guess_x(self.csr["N"])
        for i in range(0, int(self.csr["N"])):
            for j in range(self.csr["row_start"][i] - 1, self.csr["row_start"][i + 1] - 1):
                prod[i] += self.csr["val"][j] * current[self.csr["col"][j] - 1]
        return prod

    def vector_norm(self, vector):
        '''
        alculate simple verctor norm
        :param vector: list of vector entries
        :return: scalar value representing vector norm
        '''
        val = 0
        for elem in vector:
            val += elem ** 2
        ## Check for zero vector
        if val == 0:
            return (0)
        else:
            return (math.sqrt(val))

    def convergence_check(self, prev_x, cur_x, tol):
        '''
        Check that current and previous vectors are converging
        :param prev_x: previous X vector calculation
        :param cur_x:  the latest X vector calculation
        :param tol: The tolerance given the current X values
        :return: boolean
        '''
        x_diff = self.vector_norm(cur_x) - self.vector_norm(prev_x)
        if x_diff <= tol:
            return False
        else:
            return True

    def get_tol(self, vector_norm):
        '''
        Calculate current error tolerance
        :param vector_norm: norm of current X vector
        :return:
        '''
        tolerance = Globals.E + ((4 * Globals.Em) * abs(vector_norm))
        return tolerance
