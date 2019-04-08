import pandas as pd
import numpy as np
import os
from datetime import date as dt

VolAnalyzePath = 'E:/Pycharm/analyze/vol_analyze'


def daily_corr(bar):
    corr_dict = {}
    for name in ['cm_C', 'cm_P', 'nm_C', 'nm_P', 'cq_C', 'cq_P', 'nq_C', 'nq_P']:
        file = os.path.join(VolAnalyzePath, name+'.csv')
        sigma_list = pd.read_csv(file, index_col=0)
        date_list = sigma_list['date'].drop_duplicates().tolist()
        corr_list = []

        etf_price_list = sigma_list['etf_price'].tolist()
        # etf_change = [0]+[abs((etf_price_list[i+1]-etf_price_list[i])/etf_price_list[i]) for i in range(0, len(etf_price_list)-1)]
        etf_change = [0]
        for i in range(0, len(etf_price_list)-1):
            try:
                etf_change.append(np.abs((etf_price_list[i+1]-etf_price_list[i])/etf_price_list[i]))
            except ZeroDivisionError:
                etf_change.append(0)

        sigma_list['etf_change'] = etf_change
        sigma_list = sigma_list[sigma_list.etf_change >= bar]

        for date in date_list:
            daily_sigma = sigma_list[sigma_list.date == date]
            sigma_mean = (daily_sigma['AskSigma'] + daily_sigma['BidSigma']) / 2
            corr_list.append(sigma_mean.corr(daily_sigma['etf_price']))
            if date == 20180426 and name == 'cm_C':
                print(sigma_mean)
                print(daily_sigma['etf_price'])

        corr_dict[name] = corr_list
        date_list = [dt(int(str(x)[0:4]), int(str(x)[4:6]), int(str(x)[6:8])) for x in date_list]
    corr_dict['date'] = date_list
    df = pd.DataFrame(corr_dict, columns=['date', 'cm_C', 'cm_P', 'nm_C', 'nm_P', 'cq_C', 'cq_P', 'nq_C', 'nq_P'])
    df.to_csv('E:/Pycharm/analyze/vol_analyze/corr_2.csv')
    print(df)


def corr():
    corr_list = []
    for name in ['cm_C', 'cm_P', 'nm_C', 'nm_P', 'cq_C', 'cq_P', 'nq_C', 'nq_P']:
        file = os.path.join(VolAnalyzePath, name+'.csv')
        sigma_list = pd.read_csv(file, index_col=0)
        sigma_mean = (sigma_list['BidSigma'] + sigma_list['AskSigma'])/2
        corr_list.append(round(sigma_mean.corr(sigma_list['etf_price']),4))
    print(corr_list)


# corr()
daily_corr(0.0004)
