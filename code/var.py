
import csv
from DateFuture import date2,date
from reader import read1column, f_to_op, f_to_op2
import pandas as pd

future_id = ['IH1803', 'IH1804', 'IH1805', 'IH1806', 'IH1809']
period = date2+date


def GetAllAtm(futureID):
    atm_strike = {}
    atm_id = {}
    for future in futureID:
        name1 = 'E:/Pycharm/analyze/'+future+'atm_id.csv'
        name2 = 'E:/Pycharm/analyze/'+future+'atm_id2.csv'
        atm_filepath = []
        with open(name2) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0]:
                    atm_filepath.append(row[1])
        try:
            with open(name1) as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0]:
                        atm_filepath.append(row[1])
        except FileNotFoundError:
            pass
        atm_strike[future] = atm_filepath

    for future in futureID:
        atm_id[future] = {}
        i = 0
        for day in period:
            try:
                index = atm_strike[future][i].find(day)
                strike = atm_strike[future][i][index + 15:index + 19]
                callID = f_to_op(future, strike, 'C')
                putID = f_to_op(future, strike, 'P')
                if callID == 0 and putID == 0:
                    callID = f_to_op2(future, strike, 'C')
                    putID = f_to_op2(future, strike, 'P')
                atm_id[future][day] = [callID, putID]
            except IndexError:
                pass
            i += 1
    return atm_id


def GetVar(atm_id):
    var_array = atm_id
    for day in period:
        filename = 'E:/Pycharm/data/201805vol/' + day + '_vol/vols_' + day + '.csv'
        try:
            with open(filename) as f:
                reader = csv.reader(f)
                for row in reader:
                    for future in future_id:
                        try:
                            callID = atm_id[future][day][0]
                            putID = atm_id[future][day][1]
                        except KeyError:
                            continue
                        if callID == 0 or putID == 0:
                            continue
                        if row[2] == callID and row[0].find('14:56:') != -1:
                            var_array[future][day][0] = row[4]
                        elif row[2] == putID and row[0].find('14:56:') != -1:
                            var_array[future][day][1] = row[4]

        except FileNotFoundError:
            print('No such file or directory:'+filename)
    return atm_id


def main():
    atm = GetAllAtm(future_id)
    var = GetVar(atm)
    for future in future_id:
        var_array = var[future]
        c_var = []
        p_var = []
        t = []
        columns = ['date', 'c', 'p']
        for day in period:
            try:
                if float(var_array[day][0]) < 1:
                    c_var.append(var_array[day][0])
                    p_var.append(var_array[day][1])
                    t.append(day)
            except KeyError:
                continue
        dateframe = pd.DataFrame({'date': t, 'c': c_var, 'p': p_var}, columns=columns)
        dateframe.to_csv('E:/Pycharm/analyze/vol/'+future+'.csv')


main()

