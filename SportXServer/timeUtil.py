__author__ = '祥祥'
import time


SERVER_TIME_FORMAT = '%Y-%m-%d %X'

HOUR = 3600
DAY = HOUR * 24
MONTH = DAY * 30
YEAR = MONTH * 12

def getDatabaseTimeNow():
    return time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))

def getDatabaseTimeKeyOutOfDate():
    """
    返回时间：当前时间+一个月
    :return:
    """
    return time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time() + MONTH))

def dataBaseTime_toTimestemp(datetime):
    return time.mktime(datetime.timetuple())