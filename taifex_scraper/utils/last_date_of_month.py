import datetime
from calendar import monthrange

def last_date_of_month(s,nofuture=False):
    dt = datetime.datetime.strptime(s, '%Y/%m') # '2020/2'
    _day = monthrange(dt.year, dt.month)[1]
    # tday = (datetime.datetime.today() - timedelta(days=5)).day # debugging
    tday = datetime.datetime.today().day
    _day = tday if nofuture and _day > tday else _day
    ld = dt.replace(day=_day)
    return ld #.strftime('%Y/%m/%d') # 2020/02/29