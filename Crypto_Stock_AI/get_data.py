import datetime as dt
import pandas_datareader.data as pdr


import sys
end = dt.datetime.now()
start = end - dt.timedelta(days=3)

stocklist = ['GC=F', 'AMC']
stock = 1

try:
    df = pdr.get_data_yahoo(stocklist[stock], start, end)
except:
    print('es konnten keine Daten erhoben werden, bei der Aktie mit dem Kürzel "' + stocklist[stock] + '"')
    sys.exit()

x = df.to_numpy()

print(x)


def get_value(stock, start, end):
    try:
        df = pdr.get_data_yahoo(stock, start, end)

    except:
        print('es konnten keine Daten erhoben werden bei der Aktie mit dem Kürzel "' + stock + '"')
        return []

    return df.to_numpy()
