import unittest, os, sys
from lib.input import Input
from lib.globals import Globals

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

if __name__ == '__main__':
    unittest.main()

