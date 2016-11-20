import argparse
from lib.output import Output
from lib.sor_calc import SorCalc
from lib.bsm_calc import BsmCalc
from lib.globals import Globals

parser = argparse.ArgumentParser(description='BSM Calculator')

parser.add_argument('-s', '--strikeprice', default=10, type=float)
parser.add_argument('-ti', '--time', default=5, type=float)
parser.add_argument('-v', '--volatility', default=0.2, type=float)
parser.add_argument('-r', '--rate', default=0.02, type=float)
parser.add_argument('-i', '--intervals', default=10, type=int)
parser.add_argument('-m', '--maxits', default=100, type=int)
parser.add_argument('-o', '--omega', default=1.2, type=float)
parser.add_argument('-to', '--tolerance', default=Globals.E, type=float)
parser.add_argument('-f', '--file', default='nas_BSM.out', type=str)

args = parser.parse_args()

# Set tolerance value
Globals.E = args.tolerance

output_file = Output()

bsm = BsmCalc(args.strikeprice, args.time, args.volatility, args.rate, args.intervals) 
bsm_res = bsm.bsm_calc()

sor = SorCalc(bsm_res, args.maxits, args.omega)
sor_res = sor.sor_calc()
output_file.output_results(args.file, sor_res.stopReason, args.maxits,
                               sor_res.xSeqTol, sor_res.residualSeqTol,
                               sor_res.numIts, sor_res.x_one, sor_res.epsilon)