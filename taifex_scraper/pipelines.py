# -*- coding: utf-8 -*-
import requests
import datetime
import pytz
from .utils import make_influx_line
import os

# As offical data from taifex is released at 15:00 afterwards
# we select 15:00 Taipei time as data point's timestamp.
def setReleasTime(dt):
    _dt = datetime.datetime.strptime(dt, '%Y/%m/%d')
    return pytz.timezone('Asia/Taipei').localize(_dt).replace(hour=15).isoformat()

class TaifexScraperPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'dlPcRatioDown':
            # data = make_influx_line('dlPcRatioDown', {}, item, item['日期'])
            data = make_influx_line('dlPcRatioDown', {}, item, setReleasTime(item['日期']))
            requests.post(os.getenv("TELEGRAF_URL"), data=data.encode('utf-8'))
            return item

        if spider.name == 'dlFutDataDown':
            tag_set = {
                "契約": item["契約"],
                "到期月份(週別)": item["到期月份(週別)"],
                "是否因訊息面暫停交易": item["是否因訊息面暫停交易"],
                "交易時段": item["交易時段"]
            }
            field_set = {
                "開盤價": item["開盤價"],
                "最高價": item["最高價"],
                "最低價": item["最低價"],
                "收盤價": item["收盤價"],
                "漲跌價": item["漲跌價"],
                "漲跌%": item["漲跌%"],
                "成交量": item["成交量"],
                "結算價": item["結算價"],
                "未沖銷契約數": item["未沖銷契約數"],
                "最後最佳買價": item["最後最佳買價"],
                "最後最佳賣價": item["最後最佳賣價"],
                "歷史最高價": item["歷史最高價"],
                "歷史最低價": item["歷史最低價"],
                "價差對單式委託成交量": item["價差對單式委託成交量"]
            }
            data = make_influx_line('dlFutDataDown', tag_set, field_set, setReleasTime(item['交易日期']))
            requests.post(os.getenv("TELEGRAF_URL"), data=data.encode('utf-8'))
            return item

        return {}
