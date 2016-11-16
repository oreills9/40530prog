import argparse
from lib.input import Input
from lib.output import Output
from lib.sor_calc import SorCalc

parser = argparse.ArgumentParser(description='SOR Calculator')

parser.add_argument('--infile', default='nas_SOR.in', type=str)
parser.add_argument('--outfile', default='nas_Sor.out', type=str)
parser.add_argument('--maxits', default=100, type=int)
parser.add_argument('--omega', default=1.2, type=float)
args = parser.parse_args()

input = Input(args.infile)
output_file = Output()
matrix_check = input.row_iterator()
if matrix_check.stopReason:
    # Exit condition is true so exit here
    print('check %s' % matrix_check.stopReason)
    output_file.output_results(args.outfile, matrix_check.stopReason, args.maxits, 0, 0)
else:
    # Matrix is valid so proceed with SOR calculation
    sor = SorCalc(matrix_check.csr, args.maxits, args.omega)
    sor_res = sor.sor_calc()
    print('result %s' % sor_res.stopReason)
    output_file.output_results(args.outfile, sor_res.stopReason, args.maxits,
                               sor_res.xSeqTol, sor_res.residualSeqTol,
                               sor_res.numIts, sor_res.x_zero, sor_res.epsilon)