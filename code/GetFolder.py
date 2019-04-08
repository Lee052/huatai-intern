# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 09:13:39 2018

@author: lenovo
"""


import os
from DateFuture import date2, future_id2
import pandas as pd
import codecs

# 创建期权的文件夹 期货-时间-期权
OpFolderPath = {}
filename = 'E:/Pycharm/data/log/reff030313.txt'


# 创建文件夹
def mkdir(path):
    folder = os.path.exists(path)  
    if not folder:                   
        os.makedirs(path) 
           

# 根据option_id.csv生成期权文件夹
def CreatOpFolder(period, future):
    for f in future:
        option = Get_Option(f)
        OpFolderPath[f] = []
        for day in period:
            for opt in option:
                filename = 'E:/Pycharm/data/res_data/'+f+'/'+day+'/'+opt
                mkdir(filename)
                OpFolderPath[f].append(filename)


# 获取以 某天 以某一期货 为标的的 期权合约id 并生成csv E:\Pycharm\data\OptionID\IH1804\option_id
def Get_Option(future):
    with codecs.open(filename, 'r', 'gbk') as f:
        reader = f.read()
        f_new = []
        for i in reader.split('|'):
            f_new.append(i.strip())
        option_id = []
        for i in range(0, len(f_new)):
            if len(f_new[i]) > 10 and f_new[i][7:11] == future[2:6]:
                option_id.append(f_new[i-1])
        dataframe = pd.DataFrame({'': option_id})
        dataframe.to_csv('E:/Pycharm/data/OptionID/'+future+'/option_id2.csv')
        return option_id


CreatOpFolder(date2, future_id2)
for key in OpFolderPath:
    dataframe = pd.DataFrame({'key': OpFolderPath[key]})
    dataframe.to_csv('E:/Pycharm/data/res_data/'+key+'OpFolderPath2.csv')
print(OpFolderPath)
