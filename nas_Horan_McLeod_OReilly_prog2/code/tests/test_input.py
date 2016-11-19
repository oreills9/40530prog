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

    def test_small_diag_dom(self):
        input = Input("nas_SOR_small_diag_dom.in")
        # Get CSR format
        matrix_check = input.row_iterator()
        # Instantiate SOR instance and get result
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_DIVERGENCE)

    def test_small_diag_dom_LT_dom(self):
        input = Input("nas_SOR_small_diag_dom_LT_dom.in")
        # Get CSR format
        matrix_check = input.row_iterator()
        # Instantiate SOR instance and get result
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_DIVERGENCE)

    def test_sor_eigen_gt_one(self):
        input = Input("nas_SOR_Eigen_gt_1.in")
        matrix_check = input.row_iterator()
        # Verify stop reason
        self.assertEqual(matrix_check.stopReason, Globals.STOP_REASON_NOT_DIAG_DOM)

    def test_sor_eigen_lt_one(self):
        input = Input("nas_SOR_Eigen_lt_1.in")
        matrix_check = input.row_iterator()
        # Verify stop reason
        self.assertEqual(matrix_check.stopReason, Globals.STOP_REASON_NOT_DIAG_DOM)

    def test_sor_transpose_eigen_lt_one(self):
        input = Input("nas_SOR_Eigen_lt_1.in")
        matrix_check = input.row_iterator()
        # Verify stop reason
        self.assertEqual(matrix_check.stopReason, "TRANSPOSE?")

    def test_large_diag_dom(self):
        input = Input("nas_SOR_large.in")
        # Get CSR format
        matrix_check = input.row_iterator()
        # Instantiate SOR instance and get result
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_DIVERGENCE)


if __name__ == '__main__':
    unittest.main()

