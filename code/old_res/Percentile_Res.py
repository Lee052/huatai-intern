# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 17:12:08 2018

@author: lenovo
"""

import csv
import pandas as pd
import numpy as np
from datetime import datetime

date = ['0315','0316','0319','0320','0321','0322','0323','0326','0327',
            '0328','0329','0330','0402','0403','0404','0409','0410',
            '0411','0412','0413','0417','0418','0419','0420']

option_id = [['10001247','10001256'],['10001286','10001295'],
          ['10001167','10001169'],['10001242','10001245']]
future_id = ['IH1804','IH1805','IH1806','IH1809']

#获得一天或一段时间的期货的ATM期权合约的基差
def GetRes(future , period):
    res = [[],[]]
    for i in range(0,len(period)):
        filename ='E:/Pycharm/log/res_data/IH18042018'+date[i]+'res.csv'
        with open(filename) as f:
            data = csv.reader(f)
            for row in data:
                if  row[0] != 0:
                    res[0].append(float(row[1]))
                    res[1].append(float(row[2]))
    return res
    

#计算一短时间内的收收益率
def CalPercentile( future , date):
    res = GetRes( future, date )
    dateframe = pd.DataFrame({'buy':res[0] , 'sell':res[1] })
    dateframe.to_csv('E:/Pycharm/log/res_data/'+future)
    for i in [0,1]:
        a = np.array(res[i])
        S1 = np.percentile(a,90)
        S2 = np.percentile(a,10)
    return (S1 ,S2)

#计算一天内收益率
def CalProfit( future, date , minute = 0):
    res = GetRes( future, date)
    f = Future(future).get_ATM()
    today = datetime.strptime(date,'%m%d')
    dueday = datetime.strptime( future[4:5]+'18','%m%d')
    Tremain = dueday.__sub__(today).days
    r = []
    for buy_res in res[0]:
        r.append( buy_res/ )

    
    
    with open(filename) as f:
        data = csv.reader(f)
        for row in date:
            if row[]
    for i in range(0,19888):
        
    

print(ProcessOneFuture('IH1805','0418'))

    
                
                
                
                
        
        
        