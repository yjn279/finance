class Order():

    def __init__(self, type_, price, volume, stoploss=None, takeprofit=None):
        self.type = type_
        self.price_open = price
        self.price_close = None
        self.volume = volume
        self.takeprofit = takeprofit
        self.stoploss = stoploss

    def close(self, price):
        self.price_close = price
        profit = self.price_close - self.price_open
        return profit


def main():
    pass


if __name__ == '__main__':
    for i in df:
        main()
