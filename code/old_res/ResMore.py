# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:02:23 2018

@author: lenovo
"""
from ProcessFunc import cal_res
import pandas as pd

date = ['0315','0316','0319','0320','0321','0322','0323','0326','0327',
            '0328','0329','0330','0402','0403','0404','0409','0410',
            '0411','0412','0413','0417','0418','0419','0420']

option_id = [['10001247','10001256'],['10001286','10001295'],
          ['10001167','10001169'],['10001242','10001245']]
future_id = ['IH1804','IH1805','IH1806','IH1809']

for i in range(0,len(date)):
    date[i] = '2018'+ date[i]


res04, res05, res06, res09 = [], [], [], []
res = [res04, res05, res06, res09]


def ResAllFuture(period):
    for i in range(0, 4):
        option = option_id[i]
        future = future_id[i]
        res[i] = ResMoreDay(option, future, period )
# print(res[i])
    return res


def ResMoreDay(option, future, period):
    count = 0
    res = [[], [], []]
    for day in period:
        day_last = count
        res_day = cal_res(option[0], option[1], future, day , day_last)
        dataframe = pd.DataFrame({'0':res_day[0] ,'1': res_day[1],'2':res_day[2]})
        dataframe.to_csv( 'E:/Pycharm/data/res_data1'+future+day+'res.csv' , index = False , sep = ',')
        print('Processed:',option[0],option[1],future,day)
        for i in (0,1,2):
            res[i].append(res_day[i])
        count += 1
    return res
    
a=ResAllFuture(date)     
        
        
        
        
            
        
        
        
        
    

