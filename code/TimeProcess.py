import time
from datetime import datetime
import math

# 日内字符串时间转化为datetime
def toDatetime(timestr):
    try:
        daytime = datetime.strptime(timestr, '%Y%m%d%H:%M:%S.%f')
    except ValueError:
        try:
            daytime = datetime.strptime(timestr, '%Y%m%d%H:%M:%S')
        except ValueError:
            return 0
    return daytime


# 时间戳转化为datetime     datetime =datetime.fromtimestamp(timestamp)


# 从时间戳到字符串时间
def stamptotime(timestamp):
    timelocal = time.localtime(timestamp)
    year = timelocal.tm_year
    month = timelocal.tm_mon
    day = timelocal.tm_mday
    hour = timelocal.tm_hour
    min = timelocal.tm_min
    sec = timelocal.tm_sec
    if isinstance(timestamp, float):
        microsec = int(math.modf(timestamp)[0] * 1000000)
        datenow = datetime(year, month, day, hour, min, sec, microsec)
        datenow = datenow.strftime('%Y%m%d%H:%M:%S.%f')
    if isinstance(timestamp, int):
        datenow = datetime(year, month, day, hour, min, sec)
        datenow = datenow.strftime('%Y%m%d%H:%M:%S')
    return datenow

# print(stamptotime(1517882647.836207))

# 从带年月日的字符串时间到时间戳
def strtostamp(timestr):
    if isinstance(timestr, str):
        try:
            tick = datetime.strptime(timestr, '%Y%m%d%H:%M:%S.%f')
            tick = tick.microsecond / 1000000 + time.mktime(tick.timetuple())
        except ValueError:
            try:
                tick = datetime.strptime(timestr, '%Y%m%d%H:%M:%S')
                tick = time.mktime(tick.timetuple())
            except ValueError:
                print(timestr)
                return 0
        return tick
    elif isinstance(timestr, list):
        return [strtostamp(timestrs) for timestrs in timestr]



def f(datetime_time):
    if isinstance(datetime_time, time):
        return (datetime_time.hour*3600+datetime_time.minute*60+datetime_time.second+datetime_time.microsecond/1000000)/(24*3600)
    elif isinstance(datetime_time, int):
        return float(datetime_time)
    elif isinstance(datetime_time, datetime):
        if datetime_time.year >= 1900:
            return (datetime_time.toordinal()-datetime(1900, 1, 1).toordinal()+1)+\
               (datetime_time.hour*3600+datetime_time.minute*60+datetime_time.second+datetime_time.microsecond/1000000)/(24*3600)
    elif isinstance(datetime_time, float):
        return datetime_time
    else:
        return datetime_time


def f2(datetime_time):
    if isinstance(datetime_time, time):
        return (datetime_time.hour*3600+datetime_time.minute*60+datetime_time.second+datetime_time.microsecond/1000000)/(24*3600)
    elif isinstance(datetime_time, int):
        return float(datetime_time)
    elif isinstance(datetime_time, datetime):
        if datetime_time.year >= 1900:
            return (datetime_time.toordinal()-datetime(1900, 1, 1).toordinal()+2)+\
               (datetime_time.hour*3600+datetime_time.minute*60+datetime_time.second+datetime_time.microsecond/1000000)/(24*3600)
    elif isinstance(datetime_time, float):
        return datetime_time


def g(date_time):
    if isinstance(date_time, dt):
        return dt(date_time.year-1900, date_time.month, date_time.day)
    elif isinstance(date_time, float):
        if date_time == 0.0:
            return 0
        else:
            return dt.fromordinal(int(date_time) - 366)
    elif isinstance(date_time, int):
        if date_time == 0:
            return 0
        else:
            return dt.fromordinal(date_time - 366)


converters = {'callorput': f, 'maturityDate': g, 'multi': f2, 'netPositionToday': f, 'gammaToday': f, 'vegaToday': f,
              'thetaToday': f, 'closingPriceTodayUnderlyer' :f, 'volToday': f, 'deltaNotionalToday': f,
              'deltaSensOfVolToday': f, 'vegaNotionalToday': f, 'gammaNotionalToday': f, 'thetaNotionalToday': f,
              'rohToday': f, 'robToday': f, 'rhoNotionalToday': f, 'robNotionalToday': f, 'brBase': f, 'BR': f,
              'RF': f, 'StrategyID': f}


class Time:
    def __init__(self, *args, **kwargs):
        if isinstance(args, int):

        if kwargs['std_time']:
            self.std_time = kwargs['std_time']
            self.timestamp =
