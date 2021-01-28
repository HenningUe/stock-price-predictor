'''
Created on 13.11.2020

@author: HenningUe
'''

import datetime
import pandas as pd

df1 = pd.DataFrame({'a1': [0, 0, 1, 1, 2],
                   'b': [0, 0, 1, 1, 1],
                   'c': [11, 8, 10, 6, 6]})

df2 = pd.DataFrame({'a2': [0, 1, 1, 1, 3],
                   'b': [0, 0, 0, 1, 1],
                   'd': [22, 24, 25, 33, 37]})

x = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=("", "_1"))
x = pd.DatetimeIndex(['2008-01-01', '2008-01-02', '2008-01-03'], dtype='datetime64[ns]', freq=None)

k = 1
