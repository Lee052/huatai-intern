# -*- coding: utf-8 -*-

import pandas as pd
import os
import csv
from datetime import datetime


OpFolderPath = 'E:/Pycharm/data/option_data'
VolFolderPath = 'E:/Pycharm/data/option_vol'
AnalyzePath = 'E:/Pycharm/analyze'
FutureMap = pd.read_csv('E:/Pycharm/data/log/FutureMap.csv')
VolAnalyzePath = os.path.join(AnalyzePath, 'vol_analyze')
etfPricePath = os.path.join(VolAnalyzePath, 'etf_price.csv')
MapPath = os.path.join(OpFolderPath, 'map.csv')
MapDf = pd.read_csv(MapPath)
future_names = ['time', 'id', 'OpenPrice', 'HighestPrice', 'LowestPrice', 'LastPrice', 'PreClosePrice',
                'PreSettlementPrice', 'SettlementPrice', 'Volume', '0.000000', 'AskPrice1', 'BidPrice1', 'AskVolume1',
                'BidVolume1', 'UpdateTime', 'UpdateMillisec', 'OpenInterest']
ETF_names = ['time', 'id', 'time2', 'OpenPrice', 'HighestPrice', 'LowestPrice', 'LastPrice', 'PreclosePrice', 'Num',
             '0.000000', 'AskPrice1', 'AskPrice2', 'AskPrice3', 'AskPrice4', 'AskPrice5', 'BidPrice1', 'BidPrice2',
             'BidPrice3', 'BidPrice4', 'BidPrice5', 'AskVol1', 'AskVol2', 'AskVol3', 'AskVol4', 'AskVol5', 'BidVol1',
             'BidVol2', 'BidVol3', 'BidVol4', 'BidVol5', 'signal', 'time3']

csv_path_list = [os.path.join(VolFolderPath, x) for x in os.listdir(VolFolderPath)]
Period = MapDf['date'].drop_duplicates().values
etf_price = pd.read_csv(etfPricePath, index_col=0)


# OptionMap = pd.DataFrame(columns=['expiry', 'date', 'strike', 'id', 'type', 'path'])


def create_map():
    csv_path_list = [os.path.join(VolFolderPath, x) for x in os.listdir(VolFolderPath)]
    OptionMap = {'expiry': [], 'date': [], 'strike': [], 'id': [], 'type': [], 'path': []}
    for csv_file in csv_path_list:
        if csv_file.find('副本') != -1:   # 跳过副本
            continue
        DailyMap = {'expiry': [], 'date': [], 'strike': [], 'id': [], 'type': [], 'path': []}
        with open(csv_file) as f:
            reader = csv.reader(f)
            for row in reader:
                tmp_date = os.path.split(csv_file)[1][-12:-4]
                if row[2] not in DailyMap['id']:
                    tmp_type = 'C' if row[22] == '1' else 'P'
                    DailyMap['expiry'].append(row[23])
                    strike = int(float(row[20])*1000)
                    DailyMap['date'].append(tmp_date)
                    DailyMap['strike'].append(strike)
                    DailyMap['id'].append(row[2])
                    DailyMap['type'].append(tmp_type)
                    DailyMap['path'].append(os.path.join(OpFolderPath, row[23], tmp_date, str(strike),
                                                         row[2]+tmp_type, row[2]+'vols_data.csv'))
        for k, v in OptionMap.items():
            OptionMap[k] += DailyMap[k]
        print(csv_file)
    MapDf = pd.DataFrame(OptionMap, columns=['expiry', 'date', 'strike', 'id', 'type', 'path'])
    MapDf.to_csv(os.path.join(OpFolderPath, 'map.csv'))


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        return 1
    return 0


def create_folder():
    with open(MapPath) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0]:
                mkdir(os.path.join(OpFolderPath, row[1]))
                mkdir(os.path.join(OpFolderPath, row[1], row[2]))
                mkdir(os.path.join(OpFolderPath, row[1], row[2], row[3]))
                mkdir(os.path.join(OpFolderPath, row[1], row[2], row[3], row[4]+row[5]))
    print('Done')
    return 0


names = ['timestamp', 'spot_price', 'id', 'OptionPrice', 'BidPrice', 'AskPrice', 'Sigma', 'BidSigma', 'AskSigma',
         'Delta', 'Vega', 'Gamma', 'Theta', 'Rho', 'RhoB', 'Risk_free_rate', 'Borrow_rate', 'time2expiry',
         'Delta_time_decay', 'Delta_time', 'strike', 'Z', 'type', 'expiry', 'etf_price']


def copy_file():
    MapDf = pd.read_csv(MapPath)
    csv_path_list = [os.path.join(VolFolderPath, x) for x in os.listdir(VolFolderPath)]
    for csv_file in csv_path_list:
        if csv_file.find('副本') != -1:   # 跳过副本
            continue
        tmp_date = os.path.split(csv_file)[1][-12:-4]
        daily_vol = pd.read_csv(csv_file, header=None, names=names)
        daily_opt_id = MapDf[MapDf.date == int(tmp_date)]['id']
        for opt_id in daily_opt_id:
            to_csv_path = MapDf[MapDf.date == int(tmp_date)][MapDf.id == int(opt_id)]['path'].values[0] #  为什么这么麻烦？
            daily_op_data = daily_vol[daily_vol.id == int(opt_id)].reset_index()
            del daily_op_data['index']
            daily_op_data.to_csv(to_csv_path)
        print(csv_file)


def control(c_map=0, c_folder=0, c_file=0):
    if c_map == 1:
        create_map()
    if c_folder == 1:
        create_folder()
    if c_file == 1:
        copy_file()


# control(c_file=1)

