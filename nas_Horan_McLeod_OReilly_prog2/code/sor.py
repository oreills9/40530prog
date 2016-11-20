import argparse
from lib.input import Input
from lib.output import Output
from lib.sor_calc import SorCalc
from lib.globals import Globals

parser = argparse.ArgumentParser(description='SOR Calculator')

parser.add_argument('-i', '--infile', default='nas_SOR.in', type=str)
parser.add_argument('-ou', '--outfile', default='nas_Sor.out', type=str)
parser.add_argument('-m', '--maxits', default=100, type=int)
parser.add_argument('-om', '--omega', default=1.2, type=float)
parser.add_argument('-t', '--tol', default=Globals.E, type=float)
parser.add_argument('--check_diag', action='store_false')

args = parser.parse_args()
# Set tolerance value
Globals.E = args.tol
Globals.CHECK_DIAG = args.check_diag
input = Input(args.infile)
output_file = Output()
matrix_check = input.row_iterator()
if matrix_check.stopReason:
    # Exit condition is true so exit here
    output_file.output_results(args.outfile, matrix_check.stopReason, args.maxits, 0, 0)
else:
    # Matrix is valid so proceed with SOR calculation
    sor = SorCalc(matrix_check.csr, args.maxits, args.omega)
    sor_res = sor.sor_calc()
    output_file.output_results(args.outfile, sor_res.stopReason, args.maxits,
                               sor_res.xSeqTol, sor_res.residualSeqTol,
                               sor_res.numIts, sor_res.x_one, Globals.Em)