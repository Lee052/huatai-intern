# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:03:30 2018

@author: lenovo
"""

"""
Created on Thu Apr 19 12:52:31 2018

@author: lenovo
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

res = csv.reader(open('E:/Pycharm/workspace/test_o.csv','r'))
res_buy , res_sell = [], []
for row in res:
    res_buy.append(float(row[0]))
    res_sell.append(float(row[1]))


useful_data = [[],[]]
np_buy = np.array(res_buy)
np_sell = np.array(res_sell)
buy1 = np.percentile( np_buy, 5)
buy2 = np.percentile( np_buy, 95)
sell1 = np.percentile( np_sell, 5)
sell2 = np.percentile( np_sell, 95)

buy_chance , sell_chance , buy_price , sell_price= [] ,[],[], []
for i in range(0 ,len(res_buy)):
    if res_buy[i] < buy1:
        buy_chance.append(i) 
        buy_price.append(res_buy[i])
    if res_sell[i] > sell2:
        sell_chance.append(i)
        sell_price.append(res_sell[i])
useful_data[0].append(buy1)
useful_data[0].append(buy2)
useful_data[0].append(sell1)
useful_data[0].append( sell2)

plt.figure(figsize=(25,10))
plt.scatter( buy_chance, buy_price , color = 'red')
plt.scatter( sell_chance, sell_price , color = 'green')

print(useful_data, buy_chance)
