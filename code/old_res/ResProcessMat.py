from ProcessFunc import ProcessOp
import csv
import pandas as pd
from DateFuture import date

future_id = ['IH1809']

# 根据Option文件夹路径读取期权价格 生成PriceForRes文件
def ProcessOp_Res(filename):
    option = filename[-8:]
    day = filename[-17:-9]
    [t, ask1, bid1] = ProcessOp(option, day)
    columns = ['t', 'ask1', 'bid1']
    dataframe = pd.DataFrame({'t': t, 'ask1': ask1, 'bid1': bid1}, columns=columns)
    dataframe.to_csv(filename+'/PriceForRes.csv')
    print('Processed:'+filename)
    return 0


def main():
    for future in future_id:
        filename = 'E:/Pycharm/data/res_data/'+future+'OpFolderPath.csv'
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0]:
                    ProcessOp_Res(row[1])


main()