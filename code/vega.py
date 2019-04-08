import os
import pandas as pd
import numpy as np
from map_folder import MapDf, etf_price, names, VolAnalyzePath, OpFolderPath

EODRiskPath = 'E:/Pycharm/data/EOD_riskTable'
MapDf = pd.read_csv('E:/Pycharm/data/option_data/map.csv')

def choose_option(criteria=0.05, volume=100, type ='P', timetoexpiry=0):
    if isinstance(criteria, float):
        etf_close_price = etf_price[['date', 'close_price']]
        tmp_target = [x * (1 - criteria) for x in etf_close_price['close_price']]
        etf_close_price['tmp_target'] = tmp_target
        target_strike = []
        target_data = pd.DataFrame(columns=['date'] + names + ['volume'])
        p_atm_df = pd.read_csv('E:/Pycharm/analyze/vol_analyze/p_target_data_0.0.csv', index_col=0)
        target_id = []
        for index, row in etf_close_price[223:].iterrows():
            single_date = row['date']
            single_price = row['tmp_target']
            daily_df = MapDf[MapDf.date == int(single_date[0:4] + single_date[5:7] + single_date[8:10])][MapDf.type == type]
            expiry_list = daily_df['expiry'].drop_duplicates().tolist()
            near_df = daily_df[daily_df.expiry == expiry_list[0]]
            far_df = daily_df[daily_df.expiry.isin(expiry_list[1:])]
            strike_all= daily_df['strike'].drop_duplicates().values.tolist()

            strike_list = np.sort(np.array([x for x in strike_all if x % 50 == 0]))
            x = np.abs(strike_list - single_price*1000).argmin()
            m = strike_list.flat[x]

            atm_vega = p_atm_df[p_atm_df.date == single_date]['Vega'].values
            atm_strike = p_atm_df[p_atm_df.date == single_date]['strike'].values * 1000
            atm_index = strike_list.tolist().index(int(atm_strike))

            multi = 0
            file_path = daily_df[daily_df.strike == m].drop_duplicates('expiry')['path'].values[timetoexpiry]
            op_file = pd.read_csv(file_path, index_col=0)
            for index1, row1 in op_file.iterrows():
                if row1[0].find(' 14:56') != -1:
                    row1['date'] = single_date
                    multi = float(atm_vega / row1['Vega'])
                    tmp_target_row = row1
                    break
            while multi > 10 and (x+1) < atm_index:
                m = strike_list.flat[x+1]
                file_path = daily_df[daily_df.strike == m].drop_duplicates('expiry')['path'].values[timetoexpiry]
                op_file = pd.read_csv(file_path, index_col=0)
                for index1, row1 in op_file.iterrows():
                    if row1[0].find('14:56:') != -1:
                        row1['date'] = single_date
                        multi = float(atm_vega/row1['Vega'])
                        tmp_target_row = row1
                        break
                x += 1
            df_path = os.path.join(EODRiskPath, (single_date[0:4] + single_date[5:7] + single_date[8:10])+'riskTable.csv')
            df = pd.read_csv(df_path, index_col=0)
            df_7 = df[df.StrategyID == 7]
            larger_strike = [strike for strike in strike_all if strike >= m]
            larger_strike_id1 = near_df[near_df.strike.isin(larger_strike)]['id'].values.tolist()
            larger_strike_id2 = far_df[far_df.strike.isin(larger_strike)]['id'].values.tolist()
            strike_id1 = near_df['strike'].values.tolist()
            strike_id2 = far_df['strike'].values.tolist()

            # print(strike_list, atm_index, atm_strike, x, m, multi, larger_strike, larger_strike_id1, larger_strike_id2)

            near_volume1 = np.sum(df_7[df_7.optionCode.isin(larger_strike_id1)]['netPositionToday'].values)
            near_volume2 = np.sum(df_7[df_7.optionCode.isin(strike_id1)]['netPositionToday'].values)
            far_volume1 = np.sum(df_7[df_7.optionCode.isin(larger_strike_id2)]['netPositionToday'].values)
            far_volume2 = np.sum(df_7[df_7.optionCode.isin(strike_id2)]['netPositionToday'].values)
            volume = np.min([near_volume1, near_volume2, 0]) + np.min([far_volume1, far_volume2, 0])
            tmp_id = tmp_target_row['id']
            tmp_target_row = [tmp_target_row]

            try:
                id_1 = target_id[-1]
                file_path = daily_df[daily_df.id == id_1].drop_duplicates('expiry')['path'].values[timetoexpiry]
                op_file = pd.read_csv(file_path, index_col=0)
                for index1, row1 in op_file.iterrows():
                    if row1[0].find('14:56:') != -1:
                        row1['date'] = single_date
                        tmp_target_row.append(row1)
                        break

                id_2 = target_id[-2]
                file_path = daily_df[daily_df.id == id_2].drop_duplicates('expiry')['path'].values[timetoexpiry]
                op_file = pd.read_csv(file_path, index_col=0)
                for index1, row1 in op_file.iterrows():
                    if row1[0].find('14:56:') != -1:
                        row1['date'] = single_date
                        tmp_target_row.append(row1)
                        break
            except FileNotFoundError:
                print('No such option today!')
            except IndexError:
                print(target_strike)
                print(target_id)

            if len(tmp_target_row) == 1:
                tmp_target_row[0]['volume'] = volume
            if len(tmp_target_row) == 2:
                tmp_target_row[0]['volume'] = volume * 0.5
                tmp_target_row[1]['volume'] = volume * 0.5
            if len(tmp_target_row) == 3:
                tmp_target_row[0]['volume'] = volume * 0.3333
                tmp_target_row[1]['volume'] = volume * 0.3333
                tmp_target_row[2]['volume'] = volume * 0.3333

            for rows in tmp_target_row:
                target_data = target_data.append(rows, ignore_index=True)
            target_strike.append(m)
            target_id.append(tmp_id)

            print('Processed:' + single_date)
            # print(single_date, strike_list, atm_strike, atm_index, m, x, multi)

        target_data.to_csv(os.path.join(VolAnalyzePath, 'p_target_data_'+str(criteria)+'5.csv'))

        # etf_close_price['target_strike'] = target_strike
        # print(etf_close_price)


choose_option(criteria=0.05)


def add_tomorrow(**kwargs):
    delta = str(kwargs['delta'])
    vega = str(kwargs['vega'])
    p_target_data = pd.read_csv(os.path.join(VolAnalyzePath, 'p_target_data_0.055.csv'), index_col=0)
    target_data = pd.DataFrame(columns=['date'] + names + ['tomorrow_bid1'])
    date_list = p_target_data['date'].drop_duplicates().tolist()
    udly_change = kwargs['delta'] / len(date_list) * 2.858
    vol_change = kwargs['vega'] / len(date_list) * 100
    print(udly_change, vol_change)
    for index, row in p_target_data.iterrows():
        date = row['date']
        try:
            tomorrow = date_list[date_list.index(date)+1]
        except IndexError:
            print('The last day:' + row['date'])
            break
        tomorrow = tomorrow[0:4] + tomorrow[5:7] + tomorrow[8:10]
        tomorrow_path = os.path.join(OpFolderPath, str(row['expiry']), tomorrow, str(int(row['strike'] * 1000)),
                                     str(row['id']) + 'P', str(row['id']) + 'vols_data.csv')
        try:
            tomorrow_df = pd.read_csv(tomorrow_path, index_col=0)
            for index1, row1 in tomorrow_df.iterrows():
                if row1[0].find('14:56:') != -1:
                    tomorrow_bid1 = row1['BidPrice']
                    tomorrow_vega = row1['Vega']
                    tomorrow_delta = row1['Delta']
                    break
            row['tomorrow_bid1'] = tomorrow_bid1
            row['tomorrow_vega'] = tomorrow_vega
            row['tomorrow_delta'] = tomorrow_delta
            row['tomorrow_delta_cost'] = tomorrow_delta * udly_change
            row['tomorrow_vega_cost'] = tomorrow_vega * vol_change
        except FileNotFoundError:
            row['tomorrow_bid1'] = None
            row['tomorrow_vega'] = None
            row['tomorrow_delta'] = None
            row['tomorrow_delta_cost'] = None
            row['tomorrow_vega_cost'] = None
            print('NoTomorrowData:', row['date'])
        target_data = target_data.append(row, ignore_index=True)

    target_data.to_csv(os.path.join(VolAnalyzePath, 'p_target_data_0.05_'+delta+'_'+vega+'.csv'))

    to_cal_names = ['date', 'tomorrow_bid1', 'OptionPrice', 'tomorrow_delta_cost', 'tomorrow_vega_cost', 'volume']
    to_cal = pd.read_csv(os.path.join(VolAnalyzePath, 'p_target_data_0.05_'+delta+'_'+vega+'.csv'), index_col=0)[to_cal_names]
    to_cal['profit'] = to_cal.apply(lambda row2: (row2['tomorrow_bid1'] - row2['OptionPrice'] + row2['tomorrow_delta_cost']+
                               row2['tomorrow_vega_cost']) * (-row2['volume']), axis=1)
    to_cal['cum_profit'] = np.cumsum(to_cal['profit'])
    gb = to_cal.groupby('date')['profit'].sum()
    gb2 = np.cumsum(gb.values).tolist()
    gb2 = [round(x, 4) for x in gb2]
    to_df = pd.DataFrame({'date': date_list[:-1], 'cum_profit_'+delta+'_'+vega: gb2}, columns=['date', 'cum_profit_'+delta+'_'+vega] )
    to_cal.to_csv(os.path.join(VolAnalyzePath, 'p_target_data_0.05_'+delta+'_'+vega+'_cal.csv'))
    return to_df


def main():
    final_df = pd.DataFrame()
    for i in [0, 0.05, 0.1, 0.15, 0.2]:
        for j in [-0.1, 0, 0.1, 0.2, 0.3]:
            tmp_df = add_tomorrow(delta=i, vega=j)
            if final_df.empty:
                final_df = tmp_df
            else:
                final_df = final_df.merge(tmp_df, on='date')
            print(final_df)
    final_df.to_csv(os.path.join(VolAnalyzePath, 'vega_delta2.csv'))


main()
