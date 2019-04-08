# -*- coding: utf-8 -*-
import csv
import os
import pandas as pd
import numpy as np
from map_folder import MapDf, future_names, ETF_names, FutureMap, etf_price, OpFolderPath
from TimeProcess import strtostamp, toDatetime, stamptotime
from scipy import interpolate
from scipy.stats import kstest
import matplotlib.pyplot as plt

LogPath = 'E:/Pycharm/data/log'
InterPath = 'E:/Pycharm/analyze/Interpolate'
Log_Period = os.listdir(LogPath)
ex_date = '20180201'
AllData = pd.read_csv(os.path.join(InterPath, 'AllData.csv'))


def Interpolate(etf_old_time, etf_old_price, to_period):
    start_time = etf_old_time[0]
    end_time = etf_old_time[-1]
    t_new_before, t_new_end, price_new_before, price_new_end = [], [], [], []
    for tick in to_period:
        if tick < start_time:
            t_new_before.append(tick)
            price_new_before.append(etf_old_price[0])
        if tick > end_time:
            t_new_end.append(tick)
            price_new_end.append(etf_old_price[-1])
    etf_old_time = t_new_before + etf_old_time + t_new_end
    etf_old_price = price_new_before + etf_old_price + price_new_end
    f = interpolate.interp1d(etf_old_time, etf_old_price, kind='slinear')
    to_price = f(to_period)
    return to_price


def getFutureMap(period=Log_Period):
    date_list = []
    future_list = []
    for date in period:
        future_file = pd.read_csv(os.path.join(LogPath, date, 'Future.csv'), header=None, names=future_names)
        tmp_future_list = future_file['id'].drop_duplicates()
        for f in tmp_future_list:
            date_list.append(date)
            future_list.append(f)
    df = pd.DataFrame({'date': date_list, 'id': future_list}, columns=['date', 'id'])
    df.to_csv(os.path.join(LogPath, 'FutureMap.csv'))


def process_log(period=Log_Period):
    for date in period:
        etf_file = pd.read_csv(os.path.join(LogPath, date, 'ETF.csv'), header=None, names=ETF_names)
        etf_old_price = [x for x in etf_file.apply(lambda row: (row['AskPrice1'] + row['BidPrice1']) / 2, axis=1)]
        etf_old_time = [x for x in etf_file.apply(lambda row: strtostamp(date + row['time']), axis=1)]
        to_period = [x for x in range(int(strtostamp(date + '09:30:00')), int(strtostamp(date + '11:30:00')))] + \
                    [x for x in range(int(strtostamp(date + '13:00:00')), int(strtostamp(date + '14:57:00')))]
        etf_new_price = Interpolate(etf_old_time, etf_old_price, to_period)

        future_file = pd.read_csv(os.path.join(LogPath, date, 'future.csv'), header=None, names=future_names)
        future_list = future_file['id'].drop_duplicates()
        f_old_time, f_old_price = [], []
        for index, row in future_file.iterrows():
            if row['id'] == future_list[0]:
                f_old_price.append((row['AskPrice1']/1000 + row['BidPrice1']/1000) / 2)
                f_old_time.append(strtostamp(date + row['time']))
        f_new_price = Interpolate(f_old_time, f_old_price, to_period)
        diff = [(f_new_price[i] - etf_new_price[i]) for i in range(0, len(to_period))]
        df = pd.DataFrame({'time': to_period, 'f_new_price':f_new_price, 'etf_new_price': etf_new_price, 'diff': diff},
                          columns=['time', 'f_new_price', 'etf_new_price', 'diff'])
        df.to_csv(os.path.join(InterPath, date+'.csv'))
        print('Processed:'+date)


def merge(period=Log_Period):
    df = pd.DataFrame(columns=['time', 'f_new_price', 'etf_new_price', 'diff'])
    file_list = os.listdir(InterPath)
    for file_name in file_list:
        print(file_name)
        tmp_data = pd.read_csv(os.path.join(InterPath, file_name))
        df = pd.concat([df, tmp_data], ignore_index=True, sort=False)
        del df[df.columns[-1]]
    df.to_csv(os.path.join(InterPath, 'AllData.csv'))
    print(df)


# merge(Log_Period)


def period_mean(period, start_time, end_time):
    start_time = strtostamp(start_time)
    end_time = strtostamp(end_time)
    data_cal = AllData[AllData.time.isin(range(int(start_time), int(end_time)+1))]
    del data_cal[data_cal.columns[0]]
    data_p1 = data_cal.iloc[:period]
    data_p2 = data_cal.iloc[period:]
    # 看下均值
    diff_mean = np.mean(data_p1['diff'])
    res = [(x-diff_mean) for x in data_p2['diff']]
    res_mean = np.mean(res)
    res_std = np.std(res)
    """
    print(diff_mean, kstest(res, 'norm'))
    plt.hist(res, 100)
    plt.show()
    """
    return [period, start_time, end_time, res_mean, res_std]


def moving_windows(start_time, end_time):
    start_time = strtostamp(start_time)
    end_time = strtostamp(end_time)
    data_cal = AllData[AllData.time.isin(range(int(start_time), int(end_time) + 1))]
    diff = data_cal['diff'].values
    length, median, mean = [], [], []
    print(len(diff)-1)

    for window_length in range(1, len(diff) - 1):
        if window_length == 600:
            rolling_mean = data_cal['diff'].rolling(window_length).mean().iloc[window_length-1:-1].values
            res = data_cal['diff'].iloc[window_length:].values - rolling_mean
            print(len(data_cal['diff'].iloc[window_length:]), len(res), len(rolling_mean))
            to_df = pd.DataFrame({'diff': data_cal['diff'].iloc[window_length:].values, 'res': res, 'moving_mean': rolling_mean})
            to_df.to_csv('E:/Pycharm/analyze/moving_test.csv')
            break



    """
    for window_length in range(1, len(diff)-1):
        if window_length == 600:
            res_list = []
            res_time = []
            res_ori = []
            for i in range(0, len(diff)-window_length):
                window_data = diff[i:i + window_length]
                window_mean = np.mean(window_data)
                tmp_res = diff[i + window_length] - window_mean
                res_list.append(tmp_res)
                res_time.append(i+window_length)
                res_ori.append(diff[i + window_length])
            res_df = pd.DataFrame({'time': res_time, 'basedif':res_ori, 'basedif-mean': res_list}, columns=['time', 'basedif', 'basedif-mean'])
            res_df.to_csv('E:/Pycharm/analyze/600length3.csv')
  
        if window_length % 60 == 0:
            res_list = []
            for i in range(0, len(diff)-window_length):
                window_data = diff[i:i + window_length]
                window_mean = np.mean(window_data)
                tmp_res = diff[i + window_length] - window_mean
                res_list.append(tmp_res)
            res_median = np.median(res_list)
            res_mean = np.mean(res_list)
            length.append(window_length)
            median.append(res_median)
            mean.append(res_mean)
            print('processed:' + str(window_length))
        
    moving = pd.DataFrame({'length': length, 'median': median, 'mean': mean}, columns=['length', 'median', 'mean'])
    moving.to_csv('E:/Pycharm/analyze/moving.csv')
    """

# moving_windows('2018040909:30:00', '2018042014:57:00')


class Position:
    def __init__(self, *order_list):
        self.etf_record = pd.DataFrame(columns=['time', 'id', 'etf_price', 'volume', 'value'])
        self.future_record = pd.DataFrame(columns=['time', 'id', 'future_price', 'volume', 'value'])
        self.option_record = pd.DataFrame(columns=['time', 'id', 'option_price', 'volume', 'value'])
        for order in order_list:
            if order.status != 'Deal':
                print('This order will not influence position!')
            else:
                if order.instrument == 'ETF':
                    self.etf_record = self.etf_record.append({'time': order.timestring, 'id': order.id, 'etf_price': order.price, 'volume': order.volume * order.direction,
                                                'value': order.price * order.volume * order.direction}, ignore_index=True)
                if order.instrument == 'Future':
                    self.future_record = self.future_record.append({'time': order.timestring, 'id': order.id, 'future_price': order.price, 'volume': order.volume * order.direction,
                                                   'value': order.price * order.volume * order.direction}, ignore_index=True)
                if order.instrument == 'Option':
                    self.option_record = self.option_record.append({'time': order.timestring, 'id': order.id, 'option_price': order.price, 'volume': order.volume * order.direction,
                                                   'value': order.price * order.volume * order.direction}, ignore_index=True)

    def add_order(self, order, inplace=False):
        result = Position(order)
        if not inplace:
            if order.instrument == 'ETF':
                result.etf_record = pd.concat([self.etf_record, result.etf_record], ignore_index=True)
                result.future_record = self.future_record
                result.option_record = self.option_record
            if order.instrument == 'Future':
                result.future_record = pd.concat([self.future_record, result.future_record], ignore_index=True)
                result.option_record = self.option_record
                result.etf_record = self.etf_record
            if order.instrument == 'Option':
                result.option_record = pd.concat([self.option_record, result.option_record], ignore_index=True)
                result.etf_record = self.etf_record
                result.future_record =self.future_record
            return result
        if inplace:
            if order.instrument == 'ETF':
                self.etf_record = pd.concat([self.etf_record, result.etf_record], ignore_index=True)
            if order.instrument == 'Future':
                self.future_record = pd.concat([self.future_record, result.future_record], ignore_index=True)
            if order.instrument == 'Option':
                self.option_record = pd.concat([self.option_record, result.option_record], ignore_index=True)
            return self

    def get_value(self):
        value = 0
        if not self.option_record.empty:
            value += np.sum(self.option_record['value'])
        if not self.future_record.empty:
            value += np.sum(self.future_record['value'])
        if not self.etf_record.empty:
            value += np.sum(self.etf_record['future'])
        return value

    def get_volume(self, instrument):
        if instrument == 'ETF':
            return np.sum(self.etf_record['volume'])
        if instrument == 'Future':
            return np.sum(self.future_record['volume'])
        if instrument == 'Option':
            return np.sum(self.option_record['volume'])

    def __str__(self):
        print(self.etf_record)
        print(self.future_record)
        print(self.option_record)
        return ''
    __repr__ = __str__

    def close(self, date):
        if self.option_record.empty == 0:
            option_exit = []
            for op_id in self.option_record['id']:
                try:
                    path = MapDf[MapDf.id == op_id][MapDf.date == date]['path']
                    file = pd.read_csv(path, index_col=0)
                    for index, row in file.iterrows():
                        if row[0].find('14:56:') != -1:
                            option_exit.append(row['BidPrice'])
                            break
                except FileNotFoundError:
                    print('cannot close this option'+ op_id)
                    option_exit.append(np.NaN)
            self.option_record['exit_price'] = option_exit
        return  self










"""
p, start, end, m, std= [], [], [], [], []
for date_start in Log_Period:
    for date_end in Log_Period[Log_Period.index(date_start)+1:]:
        for days in range(0, Log_Period.index(date_end) - Log_Period.index(date_start)):
            period = (days+1) * 14220
            tmp = period_mean(period, date_start+'09:30:00', date_end+'14:57:00')
            p.append(tmp[0])
            start.append(tmp[1])
            end.append(tmp[2])
            m.append((tmp[3]))
            std.append(tmp[4])
        print('processed:'+ date_start +'  ' +date_end)

df_final = pd.DataFrame({'period': p, 'start_time': start, 'end_time': end, 'res_mean': m, 'res_std': std},
                        columns=['period', 'start_time', 'end_time', 'res_mean', 'res_std'])
df_final.to_csv(os.path.join(InterPath, 'analyze.csv'))
"""


# 包括 未完成的单 和 实际能操作的下单
class Order:
    def __init__(self, now_time, instrument, id, direction, price, volume):
        if isinstance(now_time, str):
            self.timestring = now_time
            self.timestamp = strtostamp(now_time)
        elif isinstance(now_time, int):
            self.timestamp = now_time
        else:
            print('TimeTypeError:' + now_time)

        if instrument in ['ETF', 'etf']:
            self.instrument = 'ETF'
        elif instrument in ['f',  'Future', 'future']:
            self.instrument = 'Future'
        else:
            print('InstrumentTypeError:' + instrument)

        self.std_time = toDatetime(self.timestring)
        self.id = id
        self.direction = direction
        self.price = price
        self.volume = volume
        self.isover = False
        self.status = 'Waiting'
        self.cash_flow = 0
        self.volume_deal = 0
        self.volume_remain = self.volume - self.volume_deal

    def make_orders(self):
        self.make_orders()

    def toDataFrame(self):
        order_df = pd.DataFrame({'timestring': self.timestring, 'timestamp': self.timestamp, 'datetime': self.std_time,
                                 'instrument': self.instrument, 'id': self.id, 'direction': self.direction,
                                 'price': self.price, 'volume': self.volume, 'isover': self.isover, 'status': self.status,
                                 'cash_flow': self.cash_flow}, index=[0], columns=['timestring', 'timestamp', 'datetime',
                                                                        'instrument', 'id', 'direction', 'price',
                                                                        'volume', 'isover', 'status', 'cash_flow'
                                                                        ])
        return order_df

    def get_info(self, type=0):
        if type == 0 and self.isover == False:
            print(self.timestring, self.timestamp, self.std_time, self.instrument, self.id,
                  self.direction, self.price, self.volume, self.volume_deal, self.volume_remain, self.isover,
                  self.status, self.cash_flow)
        if type == 0 and self.isover == True:
            print(self.timestring, self.timestamp, self.std_time, self.instrument, self.id,
                  self.direction, self.price, self.volume, self.volume_deal, self.volume_remain, self.isover,
                  self.status, self.cash_flow)
        if type == 1:
            print(self.toDataFrame())
        return 0

    def __str__(self):
        print(self.timestring, self.timestamp, self.std_time, self.instrument, self.id, \
              self.direction, self.price, self.volume, self.volume_deal, self.volume_remain, self.isover, \
              self.status, self.cash_flow)
        return ''
    __repr__ = __str__


class FutureOrder(Order):
    def __init__(self, now_time, id, direction, price, volume):
        Order.__init__(self, now_time, 'Future', id, direction, price, volume)

    def make_orders(self):
        self.status = 'Reporting'
        self.status = 'Reported'
        self.status = 'Deal'
        self.volume_deal = self.volume
        self.volume_remain = self.volume - self.volume_deal
        self.isover = True
        self.cash_flow = -(self.direction * self.volume * self.price)
        return self


class ETFOrder(Order):
    def __init__(self, now_time, direction, price, volume):
        Order.__init__(self, now_time, 'ETF', '510050', direction, price, volume)

    def make_orders(self):
        self.status = 'Reporting'
        self.status = 'Reported'
        self.status = 'Deal'
        self.volume_deal = self.volume
        self.volume_remain = self.volume - self.volume_deal
        self.isover = True
        self.cash_flow = -(self.direction * self.volume * self.price)
        return self

    # make_orders 返回实际下的单 默认成功


class OptionOrder(Order):
    pass


class Signal:
    def __init__(self):
        pass
    # 存一些信号公用的方法


# 从模型中传出TradingSignal 存交易信号公用的方法
class TradingSignal(Signal):
    def __init__(self, now_time, instrument, id, direction, price, volume):
        if isinstance(now_time, str):
            self.timestring = now_time
            self.timestamp = strtostamp(now_time)
        elif isinstance(now_time, float):
            self.timestamp = now_time
            self.timestring = stamptotime(now_time)
        else:
            print('TimeTypeError:' + now_time)
        self.std_time = toDatetime(self.timestring)
        self.id = id
        self.direction = direction
        self.price = price
        self.volume = volume
        self.instrument =instrument

    def order_tracker(self):
        self.order_tracker()

    def judge1(self):
        self.judge1()

    def get_info(self, type=0):
        if type == 0:
            print(self.timestring, self.timestamp, self.std_time,  self.instrument, self.id,
                  self.direction, self.price, self.volume)
        if type == 1:
            pass


class ETFTradingSignal(TradingSignal):
    def __init__(self, now_time, direction, price, volume):
        TradingSignal.__init__(self, now_time, 'ETF', '510050', direction, price, volume)

    def order_tracker(self):
        self.path = os.path.join(LogPath, self.timestring[0:8], 'ETF.csv')
        df = pd.read_csv(self.path, header=None, names=ETF_names)
        df['timestamp'] = strtostamp([self.timestring[0:8]+x for x in df['time'].tolist()])
        index_pointer = 0
        for index, row in df.iterrows():
            if row['timestamp'] > self.timestamp:
                index_pointer = index
                break
        info_buffer = df.loc[index_pointer - 2: index_pointer]
        return info_buffer

# judge1返回 能下的单
    def judge1(self):
        info_buffer = self.order_tracker()
        if self.direction == 1:
            tmp_info = info_buffer.iloc[-2].copy()
            five_volume = tmp_info[['BidVol1', 'BidVol2', 'BidVol3', 'BidVol4', 'BidVol5']]
            five_price = tmp_info[['BidPrice1', 'BidPrice2', 'BidPrice3', 'BidPrice4', 'BidPrice5']]
            sum_volume = np.cumsum(five_volume).tolist()
            index = -1
            for cumsum in sum_volume:
                if cumsum > self.volume:
                    index = sum_volume.index(cumsum)
                    break
            if index == -1:
                print('CannotCoverAll')
                trade_info = pd.DataFrame({'time': tmp_info['time'], 'timestamp': tmp_info['timestamp'],
                                           'type': ['Bid1', 'Bid2', 'Bid3', 'Bid4', 'Bid5'],
                                           'price': five_price.tolist(),
                                           'volume': five_volume.tolist()
                                           }, columns=['time', 'timestamp', 'type', 'price', 'volume'])
            else:
                trade_info = pd.DataFrame({'time': tmp_info['time'], 'timestamp': tmp_info['timestamp'],
                                           'type': ['Bid1', 'Bid2', 'Bid3', 'Bid4', 'Bid5'][0: index+1],
                                           'price': five_price[0: index+1].tolist(), 'volume': five_volume[0: index].tolist() +
                                           [self.volume - ([0]+sum_volume[:-1])[index]]
                                           }, columns=['time', 'timestamp', 'type', 'price', 'volume'])

            order_list = [ETFOrder(self.timestring, self.direction, row['price'], row['volume'])
                              for index, row in trade_info.iterrows()]
            return order_list
        if self.direction == -1:
            tmp_info = info_buffer.iloc[-2].copy()
            five_volume = tmp_info[['AskVol1', 'AskVol2', 'AskVol3', 'AskVol4', 'AskVol5']]
            five_price = tmp_info[['AskPrice1', 'AskPrice2', 'AskPrice3', 'AskPrice4', 'AskPrice5']]
            sum_volume = np.cumsum(five_volume).tolist()
            index = -1
            for cumsum in sum_volume:
                if cumsum > self.volume:
                    index = sum_volume.index(cumsum)
                    break
            if index == -1:
                print('CannotCoverAll')
                trade_info = pd.DataFrame({'time': tmp_info['time'], 'timestamp': tmp_info['timestamp'],
                                           'type': ['Ask1', 'Ask2', 'Ask3', 'Ask4', 'Ask5'],
                                           'price': five_price.tolist(),
                                           'volume': five_volume.tolist()
                                           }, columns=['time', 'timestamp', 'type', 'price', 'volume'])
            else:
                trade_info = pd.DataFrame({'time': tmp_info['time'], 'timestamp': tmp_info['timestamp'],
                                           'type': ['Ask1', 'Ask2', 'Ask3', 'Ask4', 'Ask5'][0: index+1],
                                           'price': five_price[0: index + 1].tolist(), 'volume': five_volume[0: index].tolist() +
                                           [self.volume - ([0]+sum_volume[:-1])[index]]
                                           }, columns=['time', 'timestamp', 'type', 'price', 'volume'])
        # 主观觉得能成交的单子  前一时刻量价判断的结果 时间取得是下单命令的时间
            order_list = [ETFOrder(self.timestring, self.direction, row['price'], row['volume'])
                          for index, row in trade_info.iterrows()]
            return order_list


class FutureTradingSignal(TradingSignal):
    def __init__(self, now_time, timetoexpiry, direction, price, volumn):
        TradingSignal.__init__(self, now_time, 'Future', '510050', direction, price, volumn)
        self.id = FutureMap[FutureMap.date == int(self.timestring[0:8])]['id'].iloc[timetoexpiry]   # 完成FutureMap

    def order_tracker(self):
        self.path = os.path.join(LogPath, self.timestring[0:8], 'Future.csv')
        df = pd.read_csv(self.path, header=None, names=future_names)
        df = df[df.id == self.id].reset_index(drop=True)
        df['timestamp'] = strtostamp([self.timestring[0:8] + x for x in df['time'].tolist()])
        index_pointer = 0
        for index, row in df.iterrows():
            if row['timestamp'] > self.timestamp:
                index_pointer = index
                break
        info_buffer = df.loc[index_pointer-2: index_pointer]
        return info_buffer

    # judge1返回 能下的单
    def judge1(self):
        info_buffer = self.order_tracker()
        if self.direction == 1:
            tmp_info = info_buffer.iloc[-2].copy()
            volume = tmp_info['AskVolume1']
            price = tmp_info['AskPrice1']
            if volume >= self.volume:
                trade_info = pd.DataFrame({'time': tmp_info['time'], 'timestamp': tmp_info['timestamp'], 'id': self.id,
                                           'type': 'Ask1', 'price': [price], 'volume': [self.volume]
                                           }, columns=['time', 'timestamp', 'type', 'price', 'volume'])
            else:
                trade_info = pd.DataFrame({'time': tmp_info['time'], 'timestamp': tmp_info['timestamp'], 'id': self.id,
                                           'type': 'Ask1', 'price': [price], 'volume': [volume]
                                           }, columns=['time', 'timestamp', 'type', 'price', 'volume'])
                print('CannotCoverAll')
            order_list = [FutureOrder(self.timestring, self.id, self.direction, row['price'], row['volume'])
                          for index, row in trade_info.iterrows()]
            return order_list

        if self.direction == -1:
            tmp_info = info_buffer.iloc[-2].copy()
            volume = tmp_info['BidVolume1']
            price = tmp_info['BidPrice1']
            if volume >= self.volume:
                trade_info = pd.DataFrame({'time': tmp_info['time'], 'timestamp': tmp_info['timestamp'], 'id': self.id,
                                           'type': 'Bid1', 'price': price, 'volume': [self.volume]
                                           }, columns=['time', 'timestamp', 'type', 'price', 'volume'])
            else:
                trade_info = pd.DataFrame({'time': tmp_info['time'], 'timestamp': tmp_info['timestamp'], 'id': self.id,
                                           'type': 'Ask1', 'price': price, 'volume': [volume]
                                           }, columns=['time', 'timestamp', 'type', 'price', 'volume'])
                print('CannotCoverAll')
        # 主观觉得能成交的单子  前一时刻量价判断的结果 时间取得是下单命令的时间
            order_list = [FutureOrder(self.timestring, self.id, self.direction, row['price'], row['volume'])
                          for index, row in trade_info.iterrows()]
            return order_list


class OptionTradingSignal(Signal):
    def __init__(self, **kwargs):
        TradingSignal.__init__(kwargs['now_time'], 'Option', kwargs['id'], kwargs['direction'], kwargs['price'], kwargs['volume'])



class Cost:
    def __init__(self, order):
        self.std_time = order.std_timen
        if order.instrument == 'ETF':
            pass
        if order.instrument == 'Future':
            self.deposit_ratio = 0.3
            if order.status == 'Deal':
                self.deposit = (order.volume * order.price) * 0.3
                self.charge = (order.volume * order.price) * 0.0001
        if order.instrument == 'Option':
            if self.direction == -1:
                etf_date = str(self.std_time.year)+'-'+str(self.std_time.month)+'-'+str(self.std_time.day)
                S = etf_price[etf_price['date'] == etf_date]['pre_close_price'].values
                self.charge = 10
                self.deposit_ratio = order.option.C + np.max(0.12 * S - max(order.option.K - S), 0.07 * S)


class Time:
    def __init__(self, *args, **kwargs):
        if isins
        if kwargs['std_time']:
            self.std_time = kwargs['std_time']
            self.timestamp =


class MktInfo:
    def __init__(self, target_id, **kwargs):
        if target_id == 510050:
            if kwargs['period']:
                self.start_time = kwargs['period'][0]
                self.end_time = kwargs['']
                date = std_d





class Option:
    def __init__(self, **kwargs):
        if kwargs['id']:
            pass



    #  etf交易成本


a = FutureTradingSignal('2018020711:22:51', 1, 1, 200, 3)
A = FutureTradingSignal('2018020711:22:51', 2, 1, 200, 3)
b = a.judge1()[0].make_orders()
B = A.judge1()[0].make_orders()
"""
c = Position()
c = c.add_order(B)
c = c.add_order(b)
print('________')
print(c.future_record)
print('______')
print(c.get_value())
"""


def back_test(array, lower_percentile, upper_percentile, position_limit=0):
    # 持仓
    position = Position()
    # 上下限
    bar1 = np.percentile(array['diff'].values, lower_percentile)
    bar2 = np.percentile(array['diff'].values, upper_percentile)
    position_limit = position_limit
    # 整个时间跨度走一遍
    order_list = []
    for index, row in array.iterrows():
        if row['diff'] < bar1 and position.get_volume('Future') in [0, 1]:
            # print(stamptotime(row['time']), 1)
            signal1 = ETFTradingSignal(row['time'], 1, 0, 1000)
            signal2 = FutureTradingSignal(row['time'], 1, -1, 0, 1)
            for order in signal1.judge1()+signal2.judge1():
                order_list.append(order.make_orders())
                position = position.add_order(order.make_orders())
        elif row['diff'] > bar2 and position.get_volume('Future') in [-1, 0]:
            # print(stamptotime(row['time']), -1)
            signal1 = ETFTradingSignal(row['time'], -1, 0, 1000)
            signal2 = FutureTradingSignal(row['time'], 1, 1, 0, 1)
            for order in signal1.judge1()+signal2.judge1():
                order_list.append(order.make_orders())
                position = position.add_order(order.make_orders())
    print(position)
    order_df = pd.DataFrame(columns=['timestring', 'timestamp', 'datetime', 'instrument', 'id', 'direction', 'price',
                                     'volume', 'isover', 'status', 'cash_flow'])
    for order in order_list:
        order = order.toDataFrame()
        order_df = order_df.append(order, ignore_index=True)

    order_df.to_csv('E:/Pycharm/analyze/orders_15_85.csv')


def main():
    array = pd.read_csv('E:/Pycharm/analyze/interpolate/AllData.csv', index_col=0)
    back_test(array, 15, 85)


main()




