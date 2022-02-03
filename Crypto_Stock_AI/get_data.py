import datetime as dt
from pandas_datareader import data as pdr
import sys

end = dt.datetime.now()
start = end - dt.timedelta(days=3)

stocklist = ['GC=F']
stock = 0

try:
    df = pdr.get_data_yahoo(stocklist[stock], start, end)
except:
    print('es konnten keine Daten erhoben werden, bei der Aktie mit dem Kürzel "' + stocklist[stock] + '"')
    sys.exit()


print(df)
print('----')
print('----')

x = df.to_numpy()
print(x[0][0])

print('---')
print(len(x[0]))
print(len(x))


print('---')

print(type(x[0][0]))
x = int(x[0][0])
print(x)
