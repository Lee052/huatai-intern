from reader import read1column
import csv
from ProcessFunc import istradetime
from TimeProcess import strtostamp


filename = 'E:/Pycharm/data/log/20180315/Option.csv'
date ='20180315'
t = []
tradet = []
with open(filename) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[1] == '10001247':
            if istradetime(date+row[0]) and strtostamp(date+row[0]):
                tradet.append(row[0])
            else:
                print(row)
print(tradet[-1])