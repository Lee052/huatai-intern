# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 12:52:31 2018

@author: lenovo
"""

import csv
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import interpolate
import pandas as pd

"""
9月认购期权数据 2750 10001233
9月认沽期权数据 2750 10001234
期货 IH1809
"""
option_data = csv.reader(open('E:/Pycharm/log/Option.csv','r'))
future_data = csv.reader(open('E:/Pycharm/log/Future.csv','r'))
call_time, c_price_ask, c_price_bid, put_time, p_price_ask, p_price_bid  = [] , [], [] ,[] ,[], []
f_time , f_price_ask, f_price_bid = [], [], []
for row in option_data :
    if row[1] == '10001233' and row[10] != '0' and row[15] != '0':
         #print(option_data.line_num , row)
        c_price_ask.append(row[10])
        c_price_bid.append(row[15])
        call_time.append(datetime.strptime(row[0][0:8], '%H:%M:%S'))
    if row[1] == '10001234' and row[10] != '0' and row [15] != '0':
        p_price_ask.append(row[10])
        p_price_bid.append(row[15])
        put_time.append(datetime.strptime(row[0][0:8], '%H:%M:%S'))

for row in future_data:
    if row[1] == 'IH1809' and row[11] != '0.000000' and row[12] != '0.000000':
        temp1 = float(row[11])/1000000
        temp2 = float(row[12])/1000000
        f_price_ask.append(temp1)
        f_price_bid.append(temp2)
        f_time.append(datetime.strptime(row[0][0:8], '%H:%M:%S'))

c_time_new = f_time
p_time_new = f_time
f_time_num , c_time_num , p_time_num = [],[],[]
''' 转成数字'''
for t in f_time:
    s = (t.hour-9)*3600 + (t.minute-30)*60 +t.second
    f_time_num.append(s)
for t in call_time:
    s = (t.hour-9)*3600 + (t.minute-30)*60 +t.second
    c_time_num.append(s)
for t in put_time:
    s = (t.hour-9)*3600 + (t.minute-30)*60 +t.second
    p_time_num.append(s)

f_call =interpolate.interp1d( c_time_num, c_price_bid, kind='slinear') 
f_put = interpolate.interp1d( p_time_num , p_price_ask, kind= 'slinear')
syn_call = interpolate.interp1d( c_time_num, c_price_ask, kind='slinear')
syn_put = interpolate.interp1d( p_time_num , p_price_bid, kind= 'slinear')
c_new_bid = f_call(f_time_num)
p_new_ask = f_put( f_time_num)
c_new_ask = syn_call(f_time_num)
p_new_bid = syn_put(f_time_num)


res_f , res_syn= [] , []
for i in range(0,len(f_price_ask)):
    tmp_f = p_new_ask[i] + f_price_ask[i] - c_new_bid[i] - 2.75
    tmp_syn = p_new_bid[i] + f_price_bid[i] - c_new_ask[i] - 2.75
    res_f.append(tmp_f)
    res_syn.append(tmp_syn)
    print(p_new_bid[i] , f_price_bid[i] ,c_new_ask[i] )
"""
r_f, r_syn = [] , []
IH = 2750
T_remain = 110
for i in range(0 , len(res_f)):
     r_tmp1 = abs(res_f[i])*1000/ IH * 250/ T_remain
     r_tmp2 = abs(res_syn[i])*1000 /IH * 250/ T_remain
     r_f.append(r_tmp1)
     r_syn.append(r_tmp2)

"""
    
"""看极端点
    if tmp_f > -0.02 and i>5000 :
        print(p_new_ask[i] , f_price_ask[i] , c_new_bid[i] , tmp_f , i)
        print(p_new_ask[i+10] , f_price_ask[i+10] , c_new_bid[i+10] , tmp_f , i+100)
"""    
"""
dataframe = pd.DataFrame({'0':res_f ,'1': res_syn})
dataframe.to_csv( "test_o.csv" , index = False , sep = ',')    
 """   
""" 对期权进行插值
Trade_time = {}
for t in f_time:
    if t not in Trade_time:
        Trade_time[t]= []
call ={ca

for row in :
"""
    
#print(len(c_time_new),len(p_time_new),len(c_price_new), len(p_price_new),len(f_time),len(f_price))
"""
plt.figure(figsize=(50,20))
plt.plot(f_time_num,res_f,color = 'red')
plt.plot(f_time_num,res_syn,color = 'green')
"""
plt.figure(figsize =(50,20))
plt.plot(f_time_num, res_f ,color ='red')
plt.plot(f_time_num, res_syn , color = 'green')





"""
plt.xlim(datetime.datetime(1900,1,1,9,30),datetime.datetime(1900,1,1,11,30))
plt.xlim(datetime.datetime.strptime('09:30:00', '%H:%M:%S'),datetime.datetime.strptime('11:30:00', '%H:%M:%S'))
"""
"""
plt.plot(call_time , call_price, color = 'red')
plt.plot(put_time , put_price, color = 'green')
plt.figure(2)
plt.plot(f_time, f_price, color = 'blue')
plt.show()
"""