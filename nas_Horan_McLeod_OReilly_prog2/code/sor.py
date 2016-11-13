import argparse
from lib.input import Input
from lib.sor_calc import SorCalc

parser = argparse.ArgumentParser(description='SOR Calculator')

parser.add_argument('--infile', default='nas_SOR.in', type=str)
parser.add_argument('--outfile', default='nas_Sor.out', type=str)
args = parser.parse_args()
input_file = Input(args.infile)
csr = input_file.row_iterator()
print(csr)
sor = SorCalc(csr, 100, 1.2, args.outfile)
sor.sor_calc()
