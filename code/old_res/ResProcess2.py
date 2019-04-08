# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:22:27 2018

@author: lenovo
"""
from DateFuture import future_id, date
from ProcessFunc import ProcessF
import pandas as pd


# 根据期货文件夹名 读取期货数据 并生成 E:\Pycharm\data\res_data\IH1804\20180315\FutureForRes.csv
def ProcessF_Res(filename):
    date = filename[-8:]
    future = filename[-15:-9]
    [ask1, bid1, t] = ProcessF(future, date)
    columns = ['t', 'ask1', 'bid1']
    dataframe = pd.DataFrame({'t': t, 'ask1': ask1, 'bid1': bid1}, columns=columns)
    dataframe.to_csv(filename+'/FutureForRes.csv')
    print('Processed:'+filename)
    return 0


def main():
    for future in future_id:
        for day in date:
            filename = 'E:/Pycharm/data/res_data/'+future+'/'+day
            ProcessF_Res(filename)
    return 0 


main()
