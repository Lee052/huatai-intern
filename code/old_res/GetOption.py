# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:30:08 2018

@author: lenovo
"""

# 获取以 某天 以某一期货 为标的的 期权合约id 并生成csv E:\Pycharm\data\OptionID\IH1804\option_id

import codecs
import pandas as pd

filename = 'E:/Pycharm/data/log/reff030418.txt'


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
        dataframe.to_csv('E:/Pycharm/data/OptionID/'+future+'/option_id.csv')
        return option_id
    


