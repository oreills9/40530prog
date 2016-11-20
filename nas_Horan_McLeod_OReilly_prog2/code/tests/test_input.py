import unittest, os, sys
from lib.globals import Globals
from lib.input import Input
from lib.sor_calc import SorCalc

class TestInput(unittest.TestCase):
    def test_zero_matrix(self):
        input = Input("nas_SOR_invalid_n.in")
        matrix_check = input.row_iterator()
        self.assertEqual(matrix_check.stopReason, Globals.STOP_REASON_ZERO_MATRIX)

    def test_invalid_vector(self):
        input = Input("nas_SOR_invalid_b.in")
        matrix_check = input.row_iterator()
        self.assertEqual(matrix_check.stopReason, Globals.STOP_REASON_INVALID_MATRIX)

    def test_invalid_row_check(self):
        row=[1,2,3]
        row_number = 1
        N = 2
        input = Input("nas_SOR.in")
        matrix_check = input.row_check(row, row_number, N)
        self.assertEqual(matrix_check.stopReason, Globals.STOP_REASON_INVALID_MATRIX)

    def test_zero_diag_matrix(self):
        input = Input("nas_SOR_small_zero_diag.in")
        matrix_check = input.row_iterator()
        self.assertEqual(matrix_check.stopReason, Globals.STOP_REASON_ZERO_DIAGONAL)

    def test_convergence(self):
        # This mock CSR should converge
        mock_csr = {'row_start': [1, 4, 7, 10, 12, 16],
                    'val': [20.0, 3.0, 4.0, 40.0, 8.0, 1.0, 1.0, 50.0,
                            3.0, 1.0, 80.0, 1.0, 4.0, 1.0, 91.0],
                    'col': [1, 3, 4, 2, 3, 4, 1, 3, 5, 3, 4, 1, 2, 3, 5],
                    'B': [1.0, 2.0, 3.0, 4.0, 5.0], 'N': 5.0}
        mock_vector_1 = [0.030871965421411247, 0.03685855370407361, 0.05611212386095177,
                         0.04922563458310093, 0.05236801065401529]
        mock_vector_2 = [0.031911272320802216, 0.037684610495063824, 0.05624120792502128,
                         0.049311254964504496, 0.05231025383984205]
        tol = 0.001
        sor = SorCalc(mock_csr, 100, 1.2)
        converge = sor.convergence_check(mock_vector_1, mock_vector_2, tol)
        # Verify stop reason
        self.assertEqual(converge, True)

    def test_small_diag_dom(self):
        input = Input("nas_SOR_small_diag_dom.in")
        # Get CSR format
        matrix_check = input.row_iterator()
        # Instantiate SOR instance and get result
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_X_SEQ_CON)

    def test_small_diag_dom_LT_dom(self):
        input = Input("nas_SOR_small_diag_dom_LT_dom.in")
        # Get CSR format
        matrix_check = input.row_iterator()
        # Instantiate SOR instance and get result
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_X_SEQ_CON)

    def test_sor_eigen_gt_one(self):
        Globals.check_diag = False
        input = Input("nas_SOR_Eigen_gt_1.in")
        matrix_check = input.row_iterator()
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_DIVERGENCE)

    def test_sor_eigen_lt_one(self):
        Globals.check_diag = False
        input = Input("nas_SOR_Eigen_lt_1.in")
        matrix_check = input.row_iterator()
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_RES_CON)

    def test_sor_transpose_eigen_lt_one(self):
        Globals.check_diag = False
        input = Input("nas_SOR_transpose.in")
        matrix_check = input.row_iterator()
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_RES_CON)

    def test_large_diag_dom(self):
        input = Input("nas_SOR_large.in")
        # Get CSR format
        matrix_check = input.row_iterator()
        # Instantiate SOR instance and get result
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_RES_CON)

if __name__ == '__main__':
    unittest.main()

