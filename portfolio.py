class PortFolio:
 
 
    def __init__(self, symbols, per, path):
 
        per = np.array(per)
 
        if len(symbols) == len(per):
            if sum(per) == 100:
                self.symbols = symbols
                self.per = per / 100

            else:
                print('Sum of per is not 100.')
        else:
            print('Length of per is not same as number of symbols.')

        for symbol in symbols:

            price = pd.read_csv(f'{path}/{symbol}_price.csv', usecols=['Date', 'Close*'])
            dividend = pd.read_csv(f'{path}/{symbol}_dividend.csv')
            
            price['Date'] = pd.to_datetime(price['Date'])
            dividend['Date'] = pd.to_datetime(dividend['Date'])
            price = price.set_index('Date')
            dividend = dividend.set_index('Date')

            price.columns = [symbol]
            dividend.columns = [symbol]

            if symbol == symbols[0]:
                prices = price
                dividends = dividend
            else:
                prices = prices.join(price, how='outer')
                dividends = dividends.join(dividend, how='outer')
 
        self.prices = prices
        self.dividends = dividends
        self.period_delta = prices.count()


    def returns(self):

        profits = np.prod(self.prices.pct_change() + 1)
        profits = profits ** (1 / self.period_delta) - 1
        profits = sum(profits * self.per)

        yields = (self.dividends / self.prices).sum()
        yields = yields / self.period_delta
        yields = sum(yields * self.per)

        return profits, yields

 
    def risks(self):
        profits, _ = self.returns()
        risks = (self.prices - profits).std()
        risks = risks / np.sqrt(self.period_delta)
        risks = risks * self.per
        return risks
 
 
    def var(self, vars):
 
        corr = self.prices.corr()
 
        vars = vars.values.reshape(1, -1)
        var = np.dot(vars, corr)
        var = np.dot(var, vars.T)
        var = np.sqrt(var.reshape(-1))
 
        return var[0]