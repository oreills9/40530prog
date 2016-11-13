import argparse
from lib.input import Input
from lib.sor_calc import SorCalc

parser = argparse.ArgumentParser(description='SOR Calculator')

parser.add_argument('--file', default='nas_SOR.in', type=str)
args = parser.parse_args()
input_file = Input(args.file)
csr = input_file.row_iterator()
print(csr)
sor = SorCalc(csr, 100, 1.2)
sor.sor_calc()
