# -*- coding: utf-8 -*-
"""
Created on Thu May 10 12:59:10 2018

@author: kyle管欣欣
"""

#
# find marketday
# find_mkt.py
#


def f_findmarketday(x,y):
    '''此函数只剔除周末，可以用来预测'''
    from dateutil.parser import parse
    from matplotlib.pylab import date2num
    from matplotlib.pylab import num2date
    a1 = date2num(parse(x))
    a2 = date2num(parse(y))
    i = a1
    weekends = ['6', '0']
    market = []
    while i <= a2:
        if num2date(i).strftime('%w') not in weekends:
            market.append(num2date(i))
        i += 1
    return market

marketday = f_findmarketday('20180101','20180511')
for day in marketday:
    print(day)

    
def h_findmarketday(x,y):
    '''函数用于大陆历史交易日查询'''
    try:
        from dateutil.parser import parse
        import pandas_datareader as web
        import time
        import datetime
    
        SSE = web.DataReader('000001.SS', data_source='yahoo',start='1/1/2000',end=time.strftime('%m/%d/%Y'))
        marketday = list(SSE.index.date)
        market = [datetime.datetime.strptime(str(date),'%Y-%m-%d') for date in marketday]
        a1 = parse(x)
        a2 = parse(y)
        k1 = market.index(a1)
        k2 = market.index(a2)
        return [market[i] for i in range(k1, k2+1)]
    except ValueError:
        print('Please check your input and make sure that both your inputs are on market day')



print(h_findmarketday('20180115','20180423'))
