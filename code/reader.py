# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:32:57 2018

@author: lenovo
"""
import csv
import codecs

reff030418 = 'E:/Pycharm/data/log/reff030418.txt'
reff030313 = 'E:/Pycharm/data/log/reff030313.txt'


# 读取reff文件，处理成列表
def txtreader(filename):
    with codecs.open(filename, 'r', 'gbk') as f:
        reader = f.read()
        f_new = []
        for i in reader.split('|'):
            f_new.append(i.strip())
        return f_new


# 根据期货和行权价及看涨看跌类型，获得期权合约id
def f_to_op(future, strike, callorput):
    txt = txtreader(reff030313)
    name = '510050'+callorput+future[2:6]+'M0'+strike
    i = 0
    id = 0
    for str in txt:
        if str == name:
            id = txt[i-1]
            break
        i += 1
    return id

def f_to_op2(future, strike, callorput):
    txt = txtreader(reff030418)
    name = '510050'+callorput+future[2:6]+'M0'+strike
    i = 0
    id = 0
    for str in txt:
        if str == name:
            id = txt[i-1]
            break
        i += 1
    return id


# 读某一个指定列
def read1column(filename, i):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        column = []
        for row in reader:
            if row[0]:
                column.append(row[i])
    return column


# 读第二、第三、第四列
def read3columns(filename):
    t, ask1, bid1 = [], [], []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0]:
                t.append(row[1])
                ask1.append(row[2])
                bid1.append(row[3])
    return [t, ask1, bid1]


# 读第一、第二、第三列
def Read3columns(filename):
    t, data1, data2 = [], [], []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0]:
                t.append(float(row[0]))
                data1.append(float(row[1]))
                data2.append(float(row[2]))
    return [t, data1, data2]
    

# 读二到六列
def read5columns(filename):
    t, askprice1, bidprice1, askvol1, bidvol1 = [], [], [], [], []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0]:
                t.append(row[1])
                askprice1.append(row[2])
                bidprice1.append(row[3])
                askvol1.append(row[4])
                bidvol1.append(row[5])
    
    
# 读某一日期的期权原始数据
def readoption(date):
    filename = 'E:/Pycharm/log/data/'+date+'/Option.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
    return reader


# 读某一日期的期货原始数据
def readfuture(date):
    filename = 'E:/Pycharm/log/data/'+date+'/Future.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
    return reader


# 读某一日期的etf原始数据
def readetf(date):
    filename = 'E:/Pycharm/log/data/'+date+'/ETF.csv'
    with open(filename,'r') as f:
        reader = csv.reader(f)
    return reader


"""
R0301
10001025
510050C1806A02700
50ETF购6月2651A
510050
50ETF
EBS
E
C
10185
2.6510
20171026
20180627
20180627
20180628
20180627
0
3495
0.1128
0.1124
2.6260
N
0.3725
0.0001
4099.67
12.00
7.00
1
1
30
1
10
0.0001
0000E
"""
