class Symbol:
 
 
    def __init__(self, symbol, output=False):
        self.url = 'https://finance.yahoo.com/quote/' + symbol
        self.symbol = symbol
        
        if output:
            print(self.url)
 
 
    def summary(self):
        dfs = pd.read_html(self.url, index_col=0)
        summary = pd.concat([dfs[0], dfs[1]])
        summary = summary.to_dict()[1]
        return summary
 
 
    def name(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'html.parser')
        name = soup.find('h1').text
        return name
 
 
    def history(self, period_open=None, period_close=None, frequency='day', filter='history', include_adjusted_close='true'):
 
        if period_open:
            period_open = dt.datetime.strptime(period_open, '%Y-%m-%d')
        else:
            period_open = dt.datetime.strptime('1970-01-01', '%Y-%m-%d')
 
        if period_close:
            period_close = dt.datetime.strptime(period_close, '%Y-%m-%d')
        else:
            period_close = dt.datetime.now()
 
        period_delta = (period_close - period_open).days
        
        period_open = period_open.timestamp()
        period_close = period_close.timestamp()
        period_delta = dt.timedelta(days=101)
 
        periods_open = int(period_open)
        periods_close = int(period_close)
        periods_delta = int(period_delta.total_seconds())

        if frequency == 'day':
            interval = '1d'
            frequency = '1d'
 
        elif frequency == 'month':
            interval = '1mo'
            frequency = '1mo'
 
        for period1 in range(periods_open, periods_close, periods_delta):
 
            period1 = dt.timedelta(seconds=period1)
            period2 = period1 + dt.timedelta(days=100)
            period1 = str(int(period1.total_seconds()))
            period2 = str(int(period2.total_seconds()))
 
            url = self.url + '/history'
            url += '?period1=' + period1 + '&period2=' + period2 + '&interval=' + interval + '&filter=' + filter + '&frequency=' + frequency + '&includeAdjustedClose=' + include_adjusted_close
 
            if period1 == str(periods_open):
                history = pd.read_html(url)[0][:-1]
            else:
                history_add = pd.read_html(url)[0][:-1]
                history = pd.concat([history_add, history])
 
        history = history.replace(['-', '.* Stock Split'], np.nan, regex=True)
        history = history.dropna(how='any')
 
        history['Date'] = pd.to_datetime(history['Date'])
        history = history.set_index('Date')
        history = history[::-1]

        dividend = history['Open'].str.contains('Dividend')
        price = history[~dividend].astype(float)
        dividend = history[dividend]

        dividend = dividend['Open']
        dividend = dividend.str.replace(' Dividend', '')
        dividend = dividend.astype(float)
        dividend.name = 'Dividend'

        return price, dividend