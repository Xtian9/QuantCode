from core.stack import *
from core.baseclasses import Portfolio

class HedgeRatioWeightsPortfolio(Portfolio):

    def __init__(self):
        super(HedgeRatioWeightsPortfolio, self).__init__()

    def generate_positions(self):
        super(HedgeRatioWeightsPortfolio, self).generate_positions()
        
        # note absolute number of shares cancels out 
        total_invested = self.x_prices + self.y_prices * self.beta

        weight_x = self.x_prices / total_invested
        weight_y = self.y_prices * self.beta / total_invested

        self.weights.iloc[:, 0] = weight_x
        self.weights.iloc[:, 1] = weight_y

