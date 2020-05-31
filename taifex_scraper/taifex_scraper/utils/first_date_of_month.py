def first_date_of_month(s):
    dt = datetime.datetime.strptime(s, '%Y/%m') # '2020/2'
    fd = dt.replace(day=1)
    return fd.strftime('%Y/%m/%d') # 2020/02/01