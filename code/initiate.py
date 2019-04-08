
import pandas as pd
import csv
from DateFuture import future_id2, date2, date
import codecs
import os

ProcessedOptionData = {}
map_path = 'E:/Pycharm/data/option_map'
log_path = 'E:/Pycharm/data/log'
op_folder_path = 'E:/Pycharm/data/option_data'
vol_folder_path = 'E:/Pycharm/data/option_vol'
expiry = [x for x in os.listdir(op_folder_path)]
period = date2 + date


# 读取reff文件，处理成列表
def txtreader(filename):
    with codecs.open(filename, 'r', 'gbk') as f:
        reader = f.read()
        f_new = []
        for i in reader.split('|'):
            f_new.append(i.strip())
        return f_new


def init_resdata(future, date):
    for f in future:
        ProcessedOptionData[future] = {}
        for day in date:
            filename
    pass


def get_today_options(date, expiry):
    filename = 'E:/Pycharm/data/log/'+date+'/Option.csv'
    id_list = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] not in id_list:
                id_list.append(row[1])
    return id_list


def map_initiate():
    txtlist = [x for x in os.listdir(map_path) if os.path.splitext(x)[1] == '.txt']
    txtpath = [os.path.join(map_path, x) for x in txtlist]
    Alltxt = [txtreader(x) for x in txtpath]
    return Alltxt


def four_expiry(date):
    print(date)
    return [expiry_date for expiry_date in expiry for op_date in os.listdir(os.path.join(op_folder_path, expiry_date))
            if op_date == date]


def atm_op_id(date):
    expiry_list = four_expiry(date)
    etf_filepath = os.path.join(log_path, date, 'ETF.csv')
    with open(etf_filepath) as f:
        reader = csv.reader(f)
        for row in reader:
            etf_pre_closeprice = int(row[7])
            break
    atm_id_list = []
    for expiry_date in expiry_list:
        previous_strike = '0'
        for strike in os.listdir(os.path.join(op_folder_path, expiry_date,date)):
            if int(previous_strike) <= etf_pre_closeprice <= int(strike):
                tmp1 = abs(int(previous_strike)-int(etf_pre_closeprice))
                tmp2 = abs(int(etf_pre_closeprice)-int(strike))
                if tmp1 <= tmp2:
                    # print(int(previous_strike),int(etf_pre_closeprice),int(strike))
                    atm_id_list.append([expiry_date]+[previous_strike]+[x[0:8] for x in os.listdir(os.path.join(op_folder_path, expiry_date, date, previous_strike))])
                else:
                    atm_id_list.append([expiry_date]+[strike]+[x[0:8] for x in os.listdir(os.path.join(op_folder_path, expiry_date, date, strike))])
            previous_strike = strike
    return atm_id_list


def get_all_atm_op_id():
    all_atm_op_id = {}
    for day in period:
        all_atm_op_id[day] = atm_op_id(day)
    return all_atm_op_id

print(expiry)
atm_id = get_all_atm_op_id()
opt_map = map_initiate()

