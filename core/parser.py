import argparse

parser = argparse.ArgumentParser(description='General arguments for running strategy backtests')

parser.add_argument('-o', '--outdir' , action='store'     , dest='outdir' ,  default='output', help='output directory')
parser.add_argument('-s', '--save'   , action='store_true', dest='save'   ,                    help='save backtest results')
parser.add_argument('-f', '--full'   , action='store_true', dest='full'   ,                    help='save full backtest results')
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',                    help='verbose output')

