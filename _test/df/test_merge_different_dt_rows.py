'''
Created on 13.11.2020

@author: HenningUe
'''

import datetime as dt
import pandas as pd
import numpy as np

idx1 = pd.DatetimeIndex(['2008-01-01', '2008-01-03', '2008-01-06'], dtype='datetime64[ns]', freq=None)
df1 = pd.DataFrame({'a1': [0, 0, 1]}, index=idx1)

idx2 = pd.DatetimeIndex(['2008-01-01', '2008-01-02', '2008-01-04'], dtype='datetime64[ns]', freq=None)
df2 = pd.DataFrame({'a1': [np.NaN, np.NaN, np.NaN]}, index=idx2)

x = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=("", "_1"))
df1.combine_first(df2)

k = 1
