# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:44:50 2018

@author: lenovo
"""
import codecs

# 处理成表格
filename = 'E:/Pycharm/data/log/reff030418.txt'


def txtreader(filename):
    with codecs.open(filename, 'r', 'gbk') as f:
        reader = f.read()
        f_new = []
        for i in reader.split('|'):
            f_new.append(i.strip())
        return f_new


txt = txtreader(filename)


# 根据期货和行权价及看涨看跌类型，获得期权合约id
def f_to_op(future, strike, callorput):
    name = '510050'+callorput+future[2:6]+'M0'+strike
    i = 0
    id = 0
    for str in txt:
        if str == name:
            id = txt[i-1]
            break
        i += 1
    return id


# print(txtreader(filename))

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