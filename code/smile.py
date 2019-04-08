# -*- coding: utf-8 -*-

import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime
from map_folder import MapDf, csv_path_list, OpFolderPath, VolFolderPath, AnalyzePath, VolAnalyzePath, etfPricePath
import numpy as np
Period = MapDf['date'].drop_duplicates().values
SmileMapPath = os.path.join(VolAnalyzePath, 'SmileMap.csv')
AtmMapPath = os.path.join(VolAnalyzePath, 'AtmMap.csv')
etf_price = pd.read_csv(etfPricePath)
SmileAlpha = pd.read_csv(os.path.join(VolAnalyzePath, 'SmileAlpha.csv'))
AtmMap = pd.read_csv(AtmMapPath)
SmileMap = pd.read_csv(SmileMapPath)
InsertData = pd.read_csv(os.path.join(VolAnalyzePath, 'InsertData.csv'))


def get_etf_price():
    etf_price = {'date': [], 'start_price': [], 'close_price': []}
    for csv_file in csv_path_list:
        if csv_file.find('副本') != -1:   # 跳过副本
            continue
        tmp_date = os.path.split(csv_file)[1][-12:-4]
        with open(csv_file) as f:
            reader = csv.reader(f)
            daily_etf_start = 0
            gaurantee_start, gaurantee_close = 0, 0
            for row in reader:
                if daily_etf_start == 0 and row[24] != '0.01':
                    daily_etf_start = row[24]
                if gaurantee_start == 0:
                    gaurantee_start = row[1]
                daily_etf_close = row[24]
                gaurantee_close = row[1]
            if daily_etf_start == '0':
                daily_etf_start = gaurantee_start
            if daily_etf_close == '0':
                daily_etf_close = gaurantee_close
            print(tmp_date)
            etf_price['date'].append(datetime.strptime(tmp_date, '%Y%m%d'))
            etf_price['start_price'].append(daily_etf_start)
            etf_price['close_price'].append(daily_etf_close)
    etf_price['pre_close_price'] = [etf_price['start_price'][0]] + etf_price['close_price'][:-1]
    print(etf_price)
    etf_price_df = pd.DataFrame(etf_price, columns=['date', 'start_price', 'close_price'])
    etf_price_df.to_csv(os.path.join(VolAnalyzePath, 'etf_price.csv'))


def smile_map():
    print("刷新smile_map.csv")
    etf_price = pd.read_csv(etfPricePath)
    # 读到的日期是2017-01-03的str
    SmileMap = pd.DataFrame(columns=['expiry', 'date', 'strike', 'id', 'type', 'path', 'is_atm'])
    for date in Period:
        DailySmileMap = pd.DataFrame(columns=['expiry', 'date', 'strike', 'id', 'type', 'path', 'is_atm'])
        etf_close_price = etf_price[etf_price.date == str(date)[0:4]+'-'+str(date)[4:6]+'-'+str(date)[6:8]]['close_price'].iloc[0]
        daily_option = MapDf[MapDf.date == date].reset_index()
        del daily_option['index']
        expiry_list = daily_option['expiry'].drop_duplicates()
        for expiry in expiry_list:
            # 处理看涨期权
            call_option = daily_option[daily_option.expiry == expiry][daily_option.type == 'C'].copy().drop_duplicates(subset=['strike'])
            del call_option[call_option.columns[0]]
            strike_list = np.sort(call_option['strike'].drop_duplicates())   # C P公用
            standard_strike = [x for x in strike_list if x % 50 == 0]
            gap = 50
            for strike in standard_strike:
                if abs(strike-etf_close_price*1000) <= gap:
                    gap = abs(strike-etf_close_price*1000)
                    atm_strike = strike
            atm_index = standard_strike.index(atm_strike)
            if (atm_index-2) < 0 and (atm_index+5) > len(standard_strike):
                smile_call_strike = standard_strike
            elif (atm_index-2) < 0:
                smile_call_strike = standard_strike[:atm_index + 5]
            elif (atm_index + 5) > len(standard_strike):
                smile_call_strike = standard_strike[atm_index-2:]
            else:
                smile_call_strike = standard_strike[atm_index - 2:atm_index + 5]

            # 处理看跌期权
            put_option = daily_option[daily_option.expiry == expiry][daily_option.type == 'P'].copy().drop_duplicates(subset=['strike'])
            del put_option[put_option.columns[0]]
            standard_strike = [x for x in strike_list if x % 50 == 0]
            gap = 50
            for strike in standard_strike:
                if abs(strike-etf_close_price*1000) <= gap:
                    gap = abs(strike-etf_close_price*1000)
                    atm_strike = strike
            atm_index = standard_strike.index(atm_strike)
            if (atm_index - 5) < 0 and (atm_index + 2) > len(standard_strike):
                smile_put_strike = standard_strike
            elif (atm_index - 5) < 0:
                smile_put_strike = standard_strike[:atm_index + 2]
            elif (atm_index + 2) > len(standard_strike):
                smile_put_strike = standard_strike[atm_index - 5:]
            else:
                smile_put_strike = standard_strike[atm_index - 5:atm_index + 2]
            smile_call = call_option[call_option['strike'].isin(smile_call_strike)]
            smile_put = put_option[put_option['strike'].isin(smile_put_strike)]
            smile_option = pd.concat([smile_call, smile_put], ignore_index=True)
            smile_option['is_atm'] = 0
            for index, row in smile_option.iterrows():
                if row['strike'] == atm_strike:
                    smile_option.at[index, 'is_atm'] = 1
            DailySmileMap = pd.concat([DailySmileMap, smile_option], ignore_index=True)
        SmileMap = pd.concat([SmileMap, DailySmileMap], ignore_index=True)
        print('Processed:' + str(date))
    SmileMap.to_csv(os.path.join(VolAnalyzePath, 'SmileMap.csv'))


def atm_map():
    SmileWithAtm = SmileMap[SmileMap.is_atm == 1].copy().reset_index()
    del SmileWithAtm['index']
    del SmileWithAtm[SmileWithAtm.columns[0]]
    SmileWithAtm['atm_type'] = 0
    for date in Period:
        expiry_list = SmileWithAtm[SmileWithAtm.date == int(date)]['expiry'].drop_duplicates()
        print(expiry_list, date)
        for i in range(0, 4):
            index = SmileWithAtm[SmileWithAtm.expiry == expiry_list.iloc[i]][SmileWithAtm.date == int(date)].index
            print(expiry_list, date, index)
            SmileWithAtm.at[index, 'atm_type'] = i+1
    print(SmileWithAtm)
    SmileWithAtm.to_csv(os.path.join(VolAnalyzePath, 'AtmMap.csv'))


def istradetime(timestr):
    try:
        daytime = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        try:
            daytime = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            print(timestr)
            return -1
    if daytime.hour in [7, 8, 15]:
        return -1
    if daytime.hour == 9:
        if daytime.minute < 30:
            return -1
        else:
            return 0
    if daytime.hour == 14:
        if daytime.minute >= 57:
            return -1
        else:
            return 0
print(istradetime('2017-01-04 14:56:53.22'))



def atm_vol():
    name = ['cm', 'nm', 'cq', 'nq']
    for i in [1, 2, 3, 4]:
        for opt_type in ['C', 'P']:
            key = name[i-1] + '_' + opt_type
            # 存在有两个相同strike 到期日的合约 但是 一个有A一个没有 ，处理
            target_path = AtmMap[AtmMap.atm_type == i][AtmMap.type == opt_type].drop_duplicates('date')['path']
            sigma_df = pd.DataFrame(columns=['date', 'timestamp', 'id', 'Sigma', 'BidSigma', 'AskSigma', 'strike', 'etf_price'])
            for file_path in target_path:
                date = AtmMap[AtmMap.path == file_path]['date'].values
                tmp_df = pd.read_csv(file_path, index_col=0)[['timestamp', 'id', 'Sigma', 'BidSigma', 'AskSigma', 'strike', 'etf_price']]
                length = len(tmp_df['id'])
                for index, row in tmp_df.iterrows():
                    if row[0].find(' 09:30') != -1:
                        tmp_df = tmp_df.drop(range(0, index))
                        break
                for index, row in tmp_df.iterrows():
                    if row[0].find(' 14:57') != -1:
                        tmp_df = tmp_df.drop(range(index, length, 1))
                        break
                print(tmp_df)
                tmp_df['date'] = np.array([date] * len(tmp_df['id'].values))
                sigma_df = pd.concat([sigma_df, tmp_df], ignore_index=True, axis=0, sort=False)
            print(key)
            sigma_df.to_csv(os.path.join(VolAnalyzePath, key+'.csv'))


atm_vol()


def atm_price():
    etf_price = (pd.read_csv(etfPricePath, index_col=0))[['date', 'close_price']]
    # AtmPrice = pd.DataFrame(columns=['date', 'etf', 'cm_c', 'cm_p', 'nm_c', 'nm_p', 'cq_c', 'cq_p', 'nq_c', 'nq_p'])
    # print((len(etf_price)))
    atm_price = {}
    name = ['cm', 'nm', 'cq', 'nq']
    for i in [1, 2, 3, 4]:
        for opt_type in ['C', 'P']:
            key = name[i-1] + '_' + opt_type
            tmp_price_list = []
            # 存在有两个相同strike 到期日的合约 但是 一个有A一个没有 ，处理
            target_path = AtmMap[AtmMap.atm_type == i][AtmMap.type == opt_type].drop_duplicates('date')['path']

            for file_path in target_path:
                with open(file_path) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[1].find('14:56') != -1:
                            tmp_price_list.append(row[7])
                            break
            # print(len(target_path), len(Period))
            atm_price[key] = tmp_price_list
            print(key)
    atm_df = pd.DataFrame(atm_price, columns=['cm_C', 'cm_P', 'nm_C', 'nm_P', 'cq_C', 'cq_P', 'nq_C', 'nq_P'])
    AtmPrice = pd.concat([etf_price, atm_df], axis=1)
    AtmPrice.to_csv(os.path.join(VolAnalyzePath, 'AtmPrice.csv'))


def smile_spots(date, expiry, show_insert=0):
    spots = SmileMap[SmileMap.expiry == int(expiry)][SmileMap.date == int(date)].copy()
    call_spots = spots[spots.type == 'C']
    put_spots = spots[spots.type == 'P']
    call_path = call_spots['path']
    put_path = put_spots['path']
    call_strike = call_spots['strike']
    put_strike = put_spots['strike']
    call_delta, put_delta = [], []
    call_sigma, put_sigma = [], []
    for call in call_path:
        with open(call) as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[1].find('14:56') != -1:
                    tmp_delta = float(row[10])
                    tmp_sigma = float(row[8])
                    call_delta.append(tmp_delta)
                    call_sigma.append(tmp_sigma)
                    break
    for put in put_path:
        with open(put) as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[1].find('14:56') != -1:
                    tmp_delta = float(row[10])
                    tmp_sigma = float(row[8])
                    put_delta.append(tmp_delta)
                    put_sigma.append(tmp_sigma)
                    break

    print(put_strike, call_strike, put_sigma, call_sigma)
    plt.figure(figsize=(30, 15))
    plt.scatter(call_strike, call_sigma, color='red')
    plt.scatter(put_strike, put_sigma, color='green')
    if show_insert == 1:
        info = InsertData[InsertData.date == str(date)[0:4]+'-'+str(date)[4:6]+'-'+str(date)[6:8]][InsertData.expiry ==
                                            str(expiry)[0:4]+'-'+str(expiry)[4:6]+'-'+str(expiry)[6:8]]
        plt.scatter(info['callStrike'], info['callSigma'], color='black')
        plt.scatter(info['putStrike'], info['putSigma'], color='black')

    plt.show()


# 取希腊数字 的数据
def smile_with_alpha():
    SmileData = SmileMap.copy()
    smile_sigma, smile_delta = [], []
    smile_path = SmileData['path']
    for file_path in smile_path:
        with open(file_path) as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[1].find('14:56') != -1:
                    tmp_delta = float(row[10])
                    tmp_sigma = (float(row[8]) + float(row[9]))/2
                    if float(tmp_sigma) != 0.0 and float(tmp_delta) != 0.0:
                        smile_delta.append(tmp_delta)
                        smile_sigma.append(tmp_sigma)
                        break
            if float(tmp_sigma) == 0.0 or float(tmp_delta) == 0.0:
                with open(file_path) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[1].find('14:55') != -1:
                            tmp_delta = float(row[10])
                            tmp_sigma = (float(row[8]) + float(row[9])) / 2
                            smile_delta.append(tmp_delta)
                            smile_sigma.append(tmp_sigma)
                            break
    smile_alpha = pd.DataFrame({'sigma': smile_sigma, 'delta': smile_delta}, columns=['sigma', 'delta'])
    print(len(SmileData['date']), len(smile_delta))
    SmileAlpha = pd.concat([SmileData, smile_alpha], axis=1)
    del SmileAlpha[SmileAlpha.columns[0]]
    SmileAlpha.to_csv(os.path.join(VolAnalyzePath, 'SmileAlpha.csv'))


# 插入数据
def slot():
    Date, Expiry = [], []
    callSigma1, putSigma1, callSigma2, putSigma2, callSigma3, putSigma3,etf_close, timetoexpiry \
        = [], [], [], [], [], [], [], []
    diff_c_1050, diff_p_1050, diff_c_2550, diff_p_2550, diff_25,diff_10 = [], [], [], [], [], []
    for date in Period:
        expiry_list = [x for x in SmileAlpha[SmileAlpha.date == int(date)]['expiry'].drop_duplicates()]
        etf_close_price = etf_price[etf_price.date == str(date)[0:4] + '-' + str(date)[4:6] + '-' + str(date)[6:8]]['close_price'].iloc[0]
        for expiry in expiry_list:
            if date == expiry:
                continue

            timetoexpiry.append(expiry_list.index(expiry)+1)
            etf_close.append(etf_close_price)
            Date.append(datetime.strptime(str(date), '%Y%m%d'))
            Expiry.append(datetime.strptime(str(expiry), '%Y%m%d'))
            daily_smile = SmileAlpha[SmileAlpha.date == int(date)][SmileAlpha.expiry == int(expiry)]
            del daily_smile[daily_smile.columns[0]]
            # 存在同一个strike的 暂时舍弃了一个
            call_smile = daily_smile[daily_smile.type == 'C'].drop_duplicates(subset=['strike'])
            call_smile.sort_values(by='delta', inplace=True)
            call_sigma = [x for x in call_smile['sigma']]
            call_delta = [x for x in call_smile['delta']]
            call_strike = [x for x in call_smile['strike']]
            call_10 = interplot(call_delta, call_sigma, 0.1)
            call_25 = interplot(call_delta, call_sigma, 0.25)
            call_50 = interplot(call_delta, call_sigma, 0.5)
            callSigma1.append(call_10)
            callSigma2.append(call_25)
            callSigma3.append(call_50)
            put_smile = daily_smile[daily_smile.type == 'P'].drop_duplicates(subset=['strike'])
            put_smile.sort_values(by='delta', inplace=True)
            put_sigma = [x for x in put_smile['sigma']]
            put_delta = [x for x in put_smile['delta']]
            put_strike = [x for x in put_smile['strike']]
            put_10 = interplot(put_delta, put_sigma, -0.1)
            put_25 = interplot(put_delta, put_sigma, -0.25)
            put_50 = interplot(put_delta, put_sigma, -0.5)
            putSigma1.append(put_10)
            putSigma2.append(put_25)
            putSigma3.append(put_50)
            # putStrike2.append(interplot(put_delta, put_strike, -0.25))
            diff_10.append((put_10 - call_10)/call_10)
            diff_25.append((put_25 - call_25)/call_25)
            diff_c_1050.append((call_10 - call_50)/call_50)
            diff_c_2550.append((call_25 - call_50)/call_50)
            diff_p_1050.append((put_10 - put_50)/put_50)
            diff_p_2550.append((put_25 - put_50)/put_50)
    # print(len(Period), len(diff), len(putSigma), len(putStrike), len(callSigma), len(callStrike))
    InsertData = pd.DataFrame({'date': Date, 'expiry': Expiry, 'callSigma_0.1': callSigma1, 'callSigma_0.25': callSigma2, 'callSigma_0.5': callSigma3, 'putSigma_-0.1': putSigma1,
                               'putSigma_-0.25': putSigma2, 'putSigma_-0.5': putSigma3, 'diff_10': diff_10, 'diff_25': diff_25, 'diff_c_1050': diff_c_1050,
                               'diff_c_2550': diff_c_2550, 'diff_p_1050': diff_p_1050, 'diff_p_2550': diff_p_2550,
                               'etf_close': etf_close, 'timetoexpiry': timetoexpiry},
                              columns=['date', 'expiry', 'callSigma_0.1', 'callSigma_0.25', 'callSigma_0.5', 'putSigma_-0.5', 'putSigma_-0.25',
                                       'putSigma_-0.1', 'diff_10', 'diff_25', 'diff_c_1050', 'diff_c_2550', 'diff_p_1050', 'diff_p_2550', 'etf_close', 'timetoexpiry'])
    InsertData.to_csv(os.path.join(VolAnalyzePath, 'InsertData5.csv'))


def interplot(call_delta, call_sigma, x):
    if call_delta[0] > x:
        k = (call_sigma[1] - call_sigma[0]) / (call_delta[1] - call_delta[0])
        insert_delta = call_sigma[0] - k * (call_delta[0] - x)
    elif call_delta[-1] < x:
        k = (call_sigma[-2] - call_sigma[-1]) / (call_delta[-2] - call_delta[-1])
        insert_delta = call_sigma[-1] + k * (x - call_delta[-1])
    else:
        for i in range(0, len(call_delta) - 1):
            if call_delta[i] <= x <= call_delta[i + 1]:
                k = (call_sigma[i + 1] - call_sigma[i]) / (call_delta[i + 1] - call_delta[i])
                insert_delta = k * (x - call_delta[i]) + call_sigma[i]
    return insert_delta

# slot()

# smile_with_alpha()


def control(refresh_etf=0, refresh_option=0, refresh_atm_map=0, refresh_atm_price=0):
    if refresh_etf == 1:
        get_etf_price()
    if refresh_option == 1:
        smile_map()
    if refresh_atm_map == 1:
        atm_map()
    if refresh_atm_price == 1:
        atm_price()
    return 0


# control(refresh_etf=1)

# smile_spots('20170104', '20170125', show_insert=1)

