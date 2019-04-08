import tushare as ts
'''
daily_k = ts.get_report_data(2014,3)
daily_k.to_csv('E:/Pycharm/data/bonus.net_profit.csv')
'''
daily_k = ts.profit_data(top=2000)
print(daily_k)



