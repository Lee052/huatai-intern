import csv
import os
from basic_info import info_to_id
import pandas as pd
import logging
from initiate import atm_id, period, log_path
import matplotlib.pyplot as plt
from datetime import datetime


op_folder_path = 'E:/Pycharm/data/option_data'
vol_folder_path = 'E:/Pycharm/data/option_vol'
vol_path = [os.path.join(vol_folder_path, x) for x in os.listdir(vol_folder_path)
            if os.path.isdir(os.path.join(vol_folder_path, x))]
vol_csv_path = [os.path.join(vol_folder_path, x, 'vols_'+x[0:8]+'.csv') for x in os.listdir(vol_folder_path)
                if os.path.isdir(os.path.join(vol_folder_path, x))]
expiry = [x for x in os.listdir(op_folder_path)]
keys = ['cm_c', 'cm_p', 'nm_c', 'nm_p', 'cq_c', 'cq_p', 'nq_c', 'nq_p']


def get_option_vol():
    """
    for file_path in vol_path:
        date = os.path.split(file_path)[1][:8]
        date_folder = [os.path.join(op_folder_path, x, date) for x in expiry
                       if os.path.exists(os.path.join(op_folder_path, x, date))]
        if len(date_folder) <= 0:
            continue
        # print(date_folder)
        call_file = [os.path.join(i, strike_folder, op_folder) for i in date_folder for strike_folder in os.listdir(i)
                     for op_folder in os.listdir(os.path.join(i, strike_folder)) if op_folder.find('C')]
        put_file = [os.path.join(i, strike_folder, op_folder) for i in date_folder for strike_folder in os.listdir(i)
                    for op_folder in os.listdir(os.path.join(i, strike_folder)) if op_folder.find('P')]
        op_file = call_file+put_file
        op_id = [os.path.split(x)[1][:8] for x in op_file]
    """
    for csv_path in vol_csv_path[55:]:
        date = os.path.split(csv_path)[1][5:13]
        date_folder_list = [os.path.join(op_folder_path, x, date) for x in expiry if
                            os.path.exists(os.path.join(op_folder_path, x, date))]
        if not date_folder_list:
            print('No such option path'+csv_path)  # 有些期权文件夹没建立 因为期权数据被污染 或者是vol数据太多
            continue
        vol_dict = {}
        with open(csv_path) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] not in vol_dict:
                    vol_dict[row[2]] = [row]
                else:
                    vol_dict[row[2]].append(row)
        for key, value in vol_dict.items():
            try:
                to_op_path = [os.path.join(date_folder, strike, id, key+'vols_data.csv') for date_folder in date_folder_list
                          for strike in os.listdir(date_folder) for id in os.listdir(os.path.join(date_folder, strike)) if id.find(key) != -1][0]
            except IndexError:  # 意味着 to_op_path = [] 也就是 某个期权id(key)有交易数据 但是 map中找不到 因此没有创建文件夹
                print(key+'该期权不在map中， 没有对应文件夹')
                continue
            finally:
                dateframe = pd.DataFrame()
                dateframe.to_csv(to_op_path)
                # print(to_op_path)
                with open(to_op_path, 'w') as f:
                    writer = csv.writer(f)
                    for row in value:
                        writer.writerow(row)   # 存在问题 ：行与行之间存在空格 处理时需注意
        print('processed:'+csv_path)
# get_option_vol()


def atm_vol():
    i = 0
    atmvol = {}
    eight_path = [[os.path.join(op_folder_path, atm_id[date][i][0], date, atm_id[date][i][1], atm_id[date][i][2+j] + corp) for
            date in period] for i in (0, 1, 2, 3) for j, corp in [(0,'C'), (1, 'P')]]
    # print(eight_path)
    for one_atm_list in eight_path:
        one_vol_list = []
        for daily_atm_path in one_atm_list:
            try:
                csv_file = os.listdir(daily_atm_path)[0]
            except IndexError:
                print(daily_atm_path+'该路径下没有期权波动率文件， 应为没有该日期的vol文件')
                continue
            with open(os.path.join(daily_atm_path, csv_file)) as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0].find('14:56:') != -1:
                        one_vol_list.append(row[7])
                        break
        atmvol[keys[i]] = one_vol_list
        i += 1
    return atmvol


def plot():
    etf_closeprice = []
    atmvol = atm_vol()
    # print(atm_id[period[6]])
    for date in period:
        etf_filepath = os.path.join(log_path, date, 'ETF.csv')
        with open(etf_filepath) as f:
            reader = csv.reader(f)
            for row in reader:
                tmp_etf_closeprice = int(row[7])/1000
        etf_closeprice.append(tmp_etf_closeprice)
    print(len(etf_closeprice), len(atmvol['cm_p']))
    for key, value in atmvol.items():  # 0420没有期权标准差数据
        value.append(0)
    for key, value in atmvol.items():
        float_value = []
        for vol in value:
            tmp = float(vol)
            float_value.append(tmp)
        atmvol[key] = float_value
    date_excel = [datetime.strptime(x, '%Y%m%d') for x in period]
    cm = [(atmvol['cm_c'][i] + atmvol['cm_p'][i]) / 2 for i in range(0, len(date_excel))]
    nm = [(atmvol['nm_c'][i] + atmvol['nm_p'][i]) / 2 for i in range(0, len(date_excel))]
    cq = [(atmvol['cq_c'][i] + atmvol['cq_p'][i]) / 2 for i in range(0, len(date_excel))]
    nq = [(atmvol['nq_c'][i] + atmvol['nq_p'][i]) / 2 for i in range(0, len(date_excel))]
    df = pd.DataFrame({'date': date_excel, '50etf': etf_closeprice,'cm_c': atmvol['cm_c'], 'cm_p': atmvol['cm_p'], 'nm_c': atmvol['nm_c'], 'nm_p': atmvol['nm_p'],
                       'cq_c': atmvol['cq_c'], 'cq_p': atmvol['cq_p'], 'nq_c': atmvol['nq_c'], 'nq_p': atmvol['nq_p'],
                       'cm': cm, 'nm': nm, 'cq': cq, 'nq': nq}, columns=['date']+['50etf']+keys+['cm','nm','cq','nq'])
    df.to_csv('E:/Pycharm/analyze/atm_vol_20180201_20180420.csv')
    # print(atmvol)
    """
    plt.figure(figsize=(50, 15))
    plt.plot(etf_closeprice, color='yellow')
    plt.plot(atmvol['cm_c'], color='red')
    plt.plot(atmvol['cm_p'], color='green')
    plt.show()
    """



plot()



