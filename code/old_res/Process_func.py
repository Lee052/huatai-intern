# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:59:44 2018

@author: lenovo
"""


import csv
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import interpolate
import pandas as pd


#  2650  购4月 10001247 沽4月10001256

call_time, c_price_ask, c_price_bid, put_time, p_price_ask, p_price_bid  = [] , [], [] ,[] ,[], []
f_time , f_price_ask, f_price_bid = [], [], []
date_str = ['0417']
#'0411','0412','0413','0417','0418','0419','0420']

"""['0315','0316','0319','0320','0321','0322','0323','0326','0327',
            '0328','0329','0330','0402','0403','0404','0409','0410']
"""

Op_str = [['10001247','10001256'],['10001286','10001295'],
          ['10001167','10001169'],['10001242','10001245']]


# 处理单一日期 某两个同一个行权价的看涨看跌期权 的价格
def ProcessOp(single_date , single_op ):
    call_time, c_price_ask, c_price_bid = [] , [], [] 
    put_time, p_price_ask, p_price_bid = [] ,[], []
    option_data = csv.reader(open('E:/Pycharm/log/data/2018'+ single_date +'/Option.csv','r'))
    for row in option_data :
        if row[1] == single_op[0] and  row[10] != '0' and row[15] != '0':
            c_price_ask.append(row[10])
            c_price_bid.append(row[15])
            call_time.append(datetime.strptime(row[0][0:8], '%H:%M:%S'))
        if row[1] == single_op[1] and row[10] != '0' and row [15] != '0':
            p_price_ask.append(row[10])
            p_price_bid.append(row[15])
            put_time.append(datetime.strptime(row[0][0:8], '%H:%M:%S'))
    return ([c_price_ask , c_price_bid , call_time , p_price_ask , p_price_bid, put_time])

            
# 处理单一日期 某一期货价格
def ProcessF(single_date, single_f):
    future_data = csv.reader(open('E:/Pycharm/log/data/2018'+ single_date +'/Future.csv','r'))
    f_time , f_price_ask, f_price_bid = [], [], []
    for row in future_data:
        if row[1] == single_f and row[11] != '0.000000' and row[12] != '0.000000':
            temp1 = float(row[11])/1000000
            temp2 = float(row[12])/1000000
            f_price_ask.append(temp1)
            f_price_bid.append(temp2)
            f_time.append(datetime.strptime(row[0][0:8], '%H:%M:%S'))
    return ([f_time , f_price_ask, f_price_bid ])

# 将时间序列（时分秒）转换成数字
def ProcessTime(time , single_date = '0'):
    time_num = []
    for t in time:
        s = (t.hour-9)*3600 + (t.minute-30)*60 +t.second 
        time_num.append(s)
    return time_num
 
# 线性插值
def Interp1d_Slinear( t_previous , t_new, price):
    f = interpolate.interp1d( t_previous, price, kind='slinear') 
    p_new = f(t_new)
    return p_new

# 计算基差
def cal_res( op_data , f_data , K):
    res = []
    for i in range(0,len(f_price_ask)):
    tmp_f = p_new_ask[i] + f_price_ask[i] - c_new_bid[i] - 2.75
    tmp_syn = p_new_bid[i] + f_price_bid[i] - c_new_ask[i] - 2.75
    res_f.append(tmp_f)
    res_syn.append(tmp_syn)
    
print(c_price_ask)
