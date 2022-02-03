import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import numpy

end = dt.datetime.now()
start = end - dt.timedelta(days=3)

stocklist = ['BTC-EUR']


df = pdr.get_data_yahoo(stocklist[0], start, end)
print(df)
print('----')
print('----')

x = df.to_numpy()
print(x[0][4])

print('---')
print(len(x[0]))
print(len(x))