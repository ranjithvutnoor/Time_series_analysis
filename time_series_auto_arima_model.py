# -*- coding: utf-8 -*-
"""time series auto ARIMA model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eqjF4_R75OKhmgkfUHlGGs9fCUuqhflS
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime 
import plotly.express as px
plt.rcParams['figure.figsize'] = (10,8)
plt.rcParams['axes.grid'] = False

df =pd.read_csv('https://raw.githubusercontent.com/srivatsan88/YouTubeLI/master/dataset/nyc_energy_consumption.csv')
df.head()

df.info()

df['timeStamp'] = pd.to_datetime(df['timeStamp'])

df.info()

df.head()

fig  = px.line(df, x = 'timeStamp', y= 'demand', title='demand range slider')
fig = fig.update_xaxes(
 rangeslider_visible = True,
 rangeselector =dict(
     buttons =list([
                    dict(count=1,label='1y',step='year',stepmode='backward'),
                    dict(count=2,label='2y',step='year',stepmode='backward'),
                    dict(count=3,label='3y',step='year',stepmode='backward'),
                    dict(step='all')  
     ]
     )
 ) 
)
fig.show()

df_nyc = df.set_index('timeStamp')

df_nyc.plot(subplots=True)

print('Rows   : ',df.shape[0])
print('columns :',df.shape[1])
print('\n null-values : \n',df.isnull().any())
print('\n Feature  :  \n', df.columns.tolist())
print('\n unique values : \n', df.nunique())

df.query('demand!=demand')

df['demand']  = df['demand'].fillna(method = 'ffill')
df['temp'] = df['temp'].fillna(method='ffill')
df['precip'] = df['precip'].fillna(method='ffill')

df.query('demand!=demand')

print('\n missing values :  \n ', df.isnull().any())

df.plot(subplots=True)

df_nyc.resample('M').mean()
df_nyc.resample('M').mean().plot(subplots= True)

df_nyc_monthly =df_nyc.resample('M').mean()

pip install pmdarima

import pmdarima as pm
model = pm.auto_arima(df_nyc_monthly['demand'],
                      m=12,seasonal = True,
                      start_p = 0, start_q = 0, max_order =4, test = 'adf', error_action = 'ignore',
                      suppress_warnings = True,
                      stepwise = True, trace = True)

model.summary()

df_nyc_monthly

train = df_nyc_monthly[(df_nyc_monthly.index.get_level_values(0)>='2012-01-31') & (df_nyc_monthly.index.get_level_values(0)>='2017-04-30')]
test = df_nyc_monthly[(df_nyc_monthly.index.get_level_values(0)>='2017-04-30')]

test.shape

test

model.fit(train['demand'])

forecast = model.predict(n_periods=4,return_conf_int=True)

forecast

