import unittest, os, sys
from lib.globals import Globals
from lib.input import Input
from lib.output import Output
from lib.sor_calc import SorCalc

class TestInput(unittest.TestCase):
    def test_zero_matrix(self):
        input = Input("nas_SOR_invalid_n.in")
        matrix_check = input.row_iterator()
        self.assertEqual(matrix_check.stopReason, Globals.STOP_REASON_ZERO_MATRIX)

    def test_invalid_matrix(self):
        input = Input("nas_SOR_invalid_A.in")
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
        output_file = Output()
        # Get CSR format
        matrix_check = input.row_iterator()
        # Instantiate SOR instance and get result
        sor = SorCalc(matrix_check.csr, 100, 1.2)
        sor_res = sor.sor_calc()
        # Verify stop reason
        self.assertEqual(sor_res.stopReason, Globals.STOP_REASON_DIVERGENCE)

if __name__ == '__main__':
    unittest.main()

