import math
from lib.globals import Globals
from lib.output_object import OutputObject
import numpy as np

class SorCalc:
    '''
     :param csr: dict in CSR format
     :param maxits: max num of iterations
     :param omega: relaxation factor
     :return:
    '''
    def __init__(self, csr, maxits, omega):
        self.maxits = maxits
        self.csr = csr
        self.omega = omega

    def sor_calc(self):
        res = OutputObject()
        # Assume exit state false at start and set when exiting
        res.exit_state = False
        # Set initial vector guess to zero for previous calculation
        x_zero = self.guess_x(self.csr["N"])
        # Initial norm will be zero also
        x_zero_norm = 0
        # Need to remember previous X diff value for divergence check
        # Since initial guess is zero we need to ensure divergence check
        # will not pass divergence check as X_zero will be 0
        res.prev_diff = self.vector_norm(self.new_x(x_zero))
        # Set maxits here so it is in object whenever returned
        res.maxits = self.maxits
        for i in range(0, self.maxits):
            res.numIts = i
            res.x_one = self.new_x(x_zero)
            x_one_norm = self.vector_norm(res.x_one)
            res_norm = self.residual_norm(res.x_one)
            res.xSeqTol = self.get_tol(x_one_norm)
            res.residualSeqTol = self.get_tol(res_norm)
            #if x_one_norm - x_zero_norm > res.prev_diff:
            cur_diff = abs(x_one_norm - x_zero_norm)
            if cur_diff > res.prev_diff:
                res.stopReason = Globals.STOP_REASON_DIVERGENCE
                res.exit_state = True
            elif res_norm < res.residualSeqTol:
                res.stopReason = Globals.STOP_REASON_RES_CON
                res.exit_state = True
            else:
                converging = self.convergence_check(x_zero, res.x_one, res.xSeqTol)
                if converging:
                    res.stopReason = Globals.STOP_REASON_X_SEQ_CON
                    res.exit_state = True
                x_zero = res.x_one
                x_zero_norm = x_one_norm
                res.prev_diff = cur_diff
            if res.exit_state:
                return(res)
        # At this point we can assume it has reached maxits
        res.stopReason = Globals.STOP_REASON_MAX_ITS
        res.exit_state = True
        return(res)

    def guess_x(self, i):
        '''
        Initial guess for x vector
        :return: list of zeros corresponding to matrix size
        '''
        list_zeroes = [0] * int(i)
        return list_zeroes

    def new_x(self, current):
        '''
        Calculating new or current X vector
        :param current: current X vector
        :return: new X vector
        '''
        local_current = current[:]
        for i in range(0, int(self.csr["N"])):
            sor_return = self.sor_sum(local_current, i)
            ssum = sor_return["sorSum"]
            d = sor_return["diag"]
            local_current[i] += (self.omega / d) * ((self.csr["B"][i]) - ssum)
        return local_current

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
        Get the product of the matrix and the vector for residual calculation
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
        x_diff = abs(self.vector_norm(cur_x) - self.vector_norm(prev_x))
        if x_diff > tol:
            return False
        else:
            return True

    def get_tol(self, vector_norm):
        '''
        Calculate current error tolerance
        :param vector_norm: norm of current X vector
        :return:
        '''
        tolerance = (Globals.E) + ((4 * Globals.Em) * abs(vector_norm))
        return tolerance
