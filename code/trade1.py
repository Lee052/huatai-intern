# -*- coding: utf-8 -*-

from analyze import res_chance
import csv
from reader import read3columns, read1column, Read3columns
import time
from datetime import datetime
from classes import OpTrade2, FutureTrade2
from atm import atm_option
from ProcessFunc import istradetime
from TimeProcess import stamptotime


def trade_1(array, data, future=0):
    average_f = data[1]
    average_syn = data[4]
    f_90 = data[2]
    f_10 = data[3]
    syn_90 = data[5]
    syn_10 = data[6]
    res_f = array[1]
    res_syn = array[2]
    t = array[0]
    profit, longshort = 0, 0
    tick = {}
    for i in range(0, len(t)):
        if float(res_f[i]) < float(f_10) and longshort != 1:
            chance = float(t[i])
            trade = iftrade(future, chance, 1)
            if trade:
                profit -= float(res_f[i])
                profit -= 0.2/1000 + 1.5/10000
                longshort += 1
                tick[t[i]] = 'buy'
                print('time:'+stamptotime(float(t[i]))+' buy!'+' longshort:'+str(longshort)+' profit:'+str(round(profit, 6))+' res_f:'+str(round(float(res_f[i]), 6)))
                print(trade)

        elif float(res_syn[i]) > float(syn_90) and longshort != -1:
            chance = float(t[i])
            trade = iftrade(future, chance, -1)
            if trade:
                profit += float(res_syn[i])
                profit -= 0.2 / 1000 + 1.5 / 10000
                longshort += -1
                tick[t[i]] = 'sell'
                print('time:'+stamptotime(float(t[i]))+' sell! '+'longshort:'+str(longshort)+' profit:'+str(round(profit,4))+' res_syn:'+str(round(float(res_syn[i]), 6)))
                print(trade)
            
        roe = round(profit/2.6 * 250/25, 4)

    return roe


# 判断是否可以交易  先判断期货的交易时间是否在开盘时间内
def iftrade(future, tick, buysell):
    ftime = datetime.fromtimestamp(tick)
    if not istradetime(ftime):
        return 0
    callID = atm_option(future, tick, 'C')
    putID = atm_option(future, tick, 'P')
    callTrade = OpTrade2(callID, future, tick)
    putTrade = OpTrade2(putID, future, tick)
    fTrade = FutureTrade2(future, tick)
    if buysell == 1:
        if callTrade.BidVol1 > 0 and putTrade.AskVol1 > 0 and fTrade.AskVol1 > 0:
            if istradetime(callTrade.Now_time) and istradetime(putTrade.Now_time) and istradetime(fTrade.Now_time):
                return [stamptotime(callTrade.Now_time), callTrade.id, stamptotime(putTrade.Now_time), putTrade.id, fTrade.id, stamptotime(fTrade.Now_time)]
        else:
            return 0
    if buysell == -1:
        if callTrade.AskVol1 > 0 and putTrade.BidVol1 > 0 and fTrade.BidVol1 > 0:
            if istradetime(callTrade.Now_time) and istradetime(putTrade.Now_time) and istradetime(fTrade.Now_time):
                return [stamptotime(callTrade.Now_time), callTrade.id, stamptotime(putTrade.Now_time), putTrade.id, fTrade.id, stamptotime(fTrade.Now_time)]
        else:
            return 0
    

# 收益最高的参数
def findbestparam(future):
    profit = {}
    bestprofit = 0
    filename = 'E:/Pycharm/analyze/' + future + 'atm_res2.csv'
    res_data = read3columns(filename)
    for i in range(0, 50):
        for j in range(50, 100):
            data = res_chance(future, i, j)
            tmp = trade_1(res_data, data, future)
            profit[tmp] = [i, j]
            if tmp > bestprofit:
                bestprofit = tmp
            print(tmp, [i, j])
    return [bestprofit, profit[bestprofit]]


# 交易成本
def tradecost(trade, timestamp):
    ftrade = trade.futuretrade
    ctrade = trade.calltrade
    ptrade = trade.puttrade
    futurecost = ftrade.K*3000/10000
    optioncost = 0.0002 * 300000
    impactcost = 0.0001 * 300000 + 0.2*3000
    cost = futurecost + optioncost + impactcost
    return cost


def deposit(restrade):
    ftrade = restrade.ftrade
    ctrade = trade.ctrade
    ptrade = trade.ptrade
    fdeposit = ftrade.money * 0.3
    if ctrade.







def main():
    future = 'IH1803'
    data = res_chance(future, 10, 90)
    filename = 'E:/Pycharm/analyze/' + future + 'atm_res2.csv'
    res_data = read3columns(filename)
    result = trade_1(res_data, data, future)
    print(result)


main()




