# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 09:30:54 2018

@author: lenovo
"""

# 该文件处理需要用_thread 优化一下
from ProcessFunc import ProcessOp, ProcessF
import csv
import pandas as pd
from DateFuture import future_id, date
import _thread


# 根据Option文件夹路径读取期权价格(t,ask1,bid1) 生成PriceForRes文件
def ProcessOp_Res(filename):
    option = filename[-8:]
    day = filename[-17:-9]
    [t, askprice1, bidprice1, askvol1, bidvol1] = ProcessOp(option, day)
    columns = ['t', 'askprice1', 'bidprice1', 'askvol1', 'bidvol1']
    dataframe = pd.DataFrame({'t': t, 'askprice1': askprice1, 'bidprice1': bidprice1,
                              'askvol1': askvol1, 'bidvol1':bidvol1}, columns=columns)
    dataframe.to_csv(filename+'/DataForRes.csv')
    print('Processed:'+filename)
    return 0


# 根据期货文件夹名 读取期货数据(t,ask1,bid1) 并生成 E:\Pycharm\data\res_data\IH1804\20180315\DataForRes.csv
def ProcessF_Res(filename):
    date = filename[-8:]
    future = filename[-15:-9]
    [t, askprice1, bidprice1, askvol1, bidvol1] = ProcessF(future, date)
    columns = ['t', 'askprice1', 'bidprice1', 'askvol1', 'bidvol1']
    dataframe = pd.DataFrame({'t': t, 'askprice1': askprice1, 'bidprice1': bidprice1,
                              'askvol1': askvol1, 'bidvol1':bidvol1}, columns=columns)
    dataframe.to_csv(filename+'/FutureForRes.csv')
    print('Processed:'+filename)
    return 0


# 对所有日期的期货价格进行处理， 以及对所有的期权处理
def processAllF():
    for future in future_id:
        for day in date:
            filename = 'E:/Pycharm/data/res_data/'+future+'/'+day
            ProcessF_Res(filename)
    return 0


def processAllOp(future):
    filename = 'E:/Pycharm/data/res_data/'+future+'OpFolderPath.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0]:
                ProcessOp_Res(row[1])
    return 0


def main():
    processAllF()


main()


        
    




