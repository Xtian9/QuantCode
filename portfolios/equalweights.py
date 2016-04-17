from core.stack import *
from core.baseclasses import Portfolio

class EqualWeightsPortfolio(Portfolio):

    def __init__(self):
        #self.__dict__.update(kwargs)
        super(EqualWeightsPortfolio, self).__init__()

    def generate_positions(self):
        super(EqualWeightsPortfolio, self).generate_positions()
        nassets = len(self.weights.columns)
        #FIXME: should only assign weights to assets which have signals
        self.weights.loc[:,:] = 1. / nassets

