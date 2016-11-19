import argparse
# from lib.input import Input
from lib.output import Output
from lib.sor_calc import SorCalc
from lib.bsm_calc import BsmCalc

parser = argparse.ArgumentParser(description='BSM Calculator')

#parser.add_argument('--infile', default='nas_SOR.in', type=str)
parser.add_argument('-s', '--strikeprice', default=10, type=float)
parser.add_argument('-t', '--time', default=1, type=float)
parser.add_argument('-v', '--volatility', default=0.2, type=float)
parser.add_argument('-r', '--rate', default=0.02, type=float)
parser.add_argument('-d', '--duration', default=100, type=float)
parser.add_argument('-m', '--maxits', default=100, type=int)
parser.add_argument('-o', '--omega', default=1.2, type=float)
parser.add_argument('-f', '--file', default='nas_BSM.out', type=str)

args = parser.parse_args()
output_file = Output()

bsm = BsmCalc(args.strikeprice, args.time, args.volatility, args.rate, args.duration) 
bsm_res = bsm.bsm_calc()
print(bsm_res)

sor = SorCalc(bsm_res, args.maxits, args.omega)
sor_res = sor.sor_calc()
output_file.output_results(args.file, sor_res.stopReason, args.maxits,
                               sor_res.xSeqTol, sor_res.residualSeqTol,
                               sor_res.numIts, sor_res.x_zero, sor_res.epsilon)