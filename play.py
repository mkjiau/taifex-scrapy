import numpy as np
import pandas as pd
import csv
import io
import requests
import datetime
from datetime import timedelta
from calendar import monthrange
import pytz

def first_date_of_month(s):
    dt = datetime.datetime.strptime(s, '%Y/%m') # '2020/2'
    fd = dt.replace(day=1)
    return fd.strftime('%Y/%m/%d') # 2020/02/01

def last_date_of_month(s,nofuture=False):
    dt = datetime.datetime.strptime(s, '%Y/%m') # '2020/2'
    _day = monthrange(dt.year, dt.month)[1]
    # tday = (datetime.datetime.today() - timedelta(days=5)).day # debugging
    tday = datetime.datetime.today().day
    _day = tday if nofuture and _day > tday else _day
    ld = dt.replace(day=_day)
    return ld.strftime('%Y/%m/%d') # 2020/02/29

my_bias_day = 0
start_date = datetime.datetime.today() - timedelta(days=30) - timedelta(days=my_bias_day)
end_date = datetime.datetime.today() - timedelta(days=my_bias_day)

print(first_date_of_month('2020/5'))
print(last_date_of_month('2020/5'))
print(last_date_of_month('2020/5',nofuture=False))
print(last_date_of_month('2020/5',nofuture=True))

# print(pd.date_range('2014/10','2016/1', freq='MS').strftime("%Y/%m").tolist())

# for m in pd.date_range('2014/10','2016/1', freq='MS').strftime("%Y/%m").tolist():
#     print(m)

print(datetime.datetime.strptime('2020/5/3', '%Y/%m/%d').replace(hour=15, tzinfo=pytz.timezone('Asia/Taipei')))