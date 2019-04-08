import pandas as pd
import csv
import os
import xlrd
import numpy as np
from datetime import datetime, time
from datetime import date as dt
from map_folder import MapDf, VolAnalyzePath

EODPath = 'E:/Pycharm/data/EOD_report'
EODRiskPath = 'E:/Pycharm/data/EOD_riskTable'


def process_eod(folder_path, to_path):
    path_list = [os.path.join(EODPath, filename) for filename in os.listdir(folder_path)]
    for file in path_list:
        date = file[-14:-6]
        data = xlrd.open_workbook(file)
        table = data.sheet_by_name('riskTable')
        vol_nums = table.ncols
        dict = {}
        names = table.row_values(0)
        for i in range(0, vol_nums):
            values = table.col_values(i)
            dict[values[0]] = values[1:]
        df = pd.DataFrame(dict, columns=names)
        df.to_csv(os.path.join(to_path, date+'riskTable.csv'))
        print('Processed:' + date)


def get_vega(folder_path, to_path):
    path_list = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]
    vega_df = pd.DataFrame(columns=['date', 'vega', 'vega1', 'vega2', 'vega3', 'vega4'])
    for file in path_list:
        date = file[-21:-13]
        df = pd.read_csv(file, index_col=0)
        # days_list = [dt(int(str(day)[0:4]), int(str(day)[4:6]),int(str(day)[6:8])) for day in expiry_list]
        date_list = np.sort(np.array([x for x in df['maturityDate'].drop_duplicates() if x != 0.0]))
        df_7 = df[df.StrategyID == 7]
        vega1 = np.sum(df_7[df_7.maturityDate == date_list[0]]['vegaNotionalToday'])
        vega2 = np.sum(df_7[df_7.maturityDate == date_list[1]]['vegaNotionalToday'])
        vega3 = np.sum(df_7[df_7.maturityDate == date_list[2]]['vegaNotionalToday'])
        vega4 = np.sum(df_7[df_7.maturityDate == date_list[3]]['vegaNotionalToday'])
        vega1 = vega1 if vega1 else 0
        vega2 = vega2 if vega2 else 0
        vega3 = vega3 if vega3 else 0
        vega4 = vega4 if vega4 else 0
        vega = vega1 + vega2 + vega3 + vega4
        vega_df = vega_df.append({'date': date, 'vega': vega, 'vega1': vega1, 'vega2': vega2, 'vega3': vega3, 'vega4': vega4}
                       , ignore_index=True)
        print('processed:' + date)
    vega_df.to_csv(to_path)
    return 0


process_eod(EODPath, EODRiskPath)
# get_vega(EODRiskPath, os.path.join(VolAnalyzePath, 'position_vega.csv'))



def main(param, folder_path, to_path):
    if param == 0:
        process_eod(folder_path, to_path)
    if param == 1:
        get_vega(folder_path, to_path)
    return 0


# main(0, EODRiskPath, os.path.join(VolAnalyzePath, 'position_vega.csv'))