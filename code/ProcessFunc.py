    # -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:59:44 2018

@author: lenovo
"""

from classes import Op_Data, F_Data, Option, Future
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import interpolate
import time
from TimeProcess import strtostamp, toDatetime


# 获得 某一日期某一个行权价的看涨或看跌期权的成交数字时间 ask1, bid1的价格和量。并只保留在交易时间内的交易信息
def ProcessOp(option, date):
    t, askprice1, bidprice1, askvol1, bidvol1 = [], [], [], [],[]
    option_data = csv.reader(open('E:/Pycharm/data/log/'+date+'/Option.csv', 'r'))
    for row in option_data:
        if row[1] == option and row[10] != '0' and row[15] != '0':
            timestamp = strtostamp(date+row[0])
            if timestamp:
                t.append(timestamp)
                askprice1.append(row[10])
                bidprice1.append(row[15])
                askvol1.append(row[20])
                bidvol1.append(row[25])
    return [t, askprice1, bidprice1, askvol1, bidvol1]


# 获得 某一日期某一个行权价的期货的 成交数字时间 ask1, bid1的价格和量。并只保留在交易时间内的交易信息
def ProcessF(future, date):
    future_data = csv.reader(open('E:/Pycharm/data/log/'+date+'/Future.csv', 'r'))
    t, askprice1, bidprice1, askvol1, bidvol1 = [], [], [], [], []
    for row in future_data:
        if row[1] == future and row[11] != '0.000000' and row[12] != '0.000000' and row[13] and row[14]:
            timestamp = strtostamp(date+row[0])
            if istradetime(date+row[0]):
                t.append(timestamp)
                askprice1.append(float(row[11])/1000000)
                bidprice1.append(float(row[12])/1000000)
                askvol1.append(row[13])
                bidvol1.append(row[14])
    return [t, askprice1, bidprice1, askvol1, bidvol1]


# 判断是否在一天内的交易时间
def istradetime(nowtime):
    if isinstance(nowtime, str):
        nowtime = toDatetime(nowtime)
    if isinstance(nowtime, float):
        nowtime = datetime.fromtimestamp(nowtime)
    if nowtime == 0:
        return 0
    if nowtime.hour < 9 or nowtime.hour >= 15:
        return 0
    elif nowtime.hour == 9 and nowtime.minute < 30:
        return 0
    elif nowtime.hour == 14 and nowtime.minute >= 57:
        return 0
    else:
        return 1


# 判断是否有盘口
def isavailable(optrade):
    pass


# 将时间序列（时分秒）转换成数字   
def ProcessTime(daytime, day_last=0):
    time_num = []
    for t in daytime:
        s = day_last*19800 + (t.hour-9)*3600 + (t.minute-30)*60 +t.second 
        time_num.append(s)
    return time_num


# 线性插值
def Interp1d_Slinear(t_previous, t_new, price):
    f = interpolate.interp1d(t_previous, price, kind='slinear')
    p_new = f(t_new)
    return p_new



# 计算一天的基差
def cal_res(call, put, future, date ,day_last):
    res = []
    K = float(Option(call).K)
    # 期权期货原始数据
    call_data = ProcessOp( call, date)  
    put_data = ProcessOp( put, date)
    f_data = ProcessF( future, date)
    if call_data[0] == [] or put_data[0] ==[]  or f_data[0] ==[]  :
        print('No data!')
        return [[],[],[]]
    t = f_data[2]
    # print(len(t),len(call_data[2]),len(put_data[0]))

    # 对期权进行线性插值,得到新的期权价格 
    c_ask_new,put_ask_new,c_bid_new,put_bid_new =[],[],[],[]
    c_ask_new = Interp1d_Slinear(call_data[2], t , call_data[0])[0]
    put_ask_new = Interp1d_Slinear(put_data[2], t , put_data[0])[0]
    c_bid_new = Interp1d_Slinear(call_data[2], t , call_data[1])[0]
    put_bid_new = Interp1d_Slinear(put_data[2], t , put_data[1])[0]
    c_data_new =(c_ask_new ,c_bid_new, t)
    p_data_new =(put_ask_new, put_bid_new,t)

    # 公式计算，记录买卖基差
    res_f, res_syn =[] , []
    for i in range(0,len(t)):
        tmp_f = p_data_new[0][i] + f_data[0][i] - c_data_new[1][i] - K/1000
        tmp_syn = p_data_new[1][i] + f_data[1][i] - c_data_new[0][i] - K/1000
        res_f.append(tmp_f)
        res_syn.append(tmp_syn)
        #print(p_data_new[1][i],f_data[1][i] ,c_data_new[0][i], K)
    res = [t,res_f,res_syn]
    #print(res[0])
    return (res)

def res_plt(res, a = 50, b = 20):
    plt.figure(figsize = (a,b))
    plt.plot(res[0],res[1],color='red')
    plt.plot(res[0],res[2],color='green')


#a = cal_res('10001286','10001295','IH1804','20180326',0)
#res_plt(a)


# 下单函数
def orderMaker(orderbook, volumn, direction):
    if direction == 1:
        orderbook[BidVol]


    

