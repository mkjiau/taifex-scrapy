# -*- coding: utf-8 -*-
import requests
import datetime
import pytz
from .utils import make_influx_line

# As offical data from taifex is released at 15:00 afterwards
# we select 15:00 Taipei time as data point's timestamp.
def setReleasTime(dt):
    return datetime.datetime.strptime(dt, '%Y/%m/%d') \
            .replace(hour=15, tzinfo=pytz.timezone('Asia/Taipei')) \
            .isoformat()

class TaifexScraperPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'dlPcRatioDown':
            # data = make_influx_line('dlPcRatioDown', {}, item, item['日期'])
            data = make_influx_line('dlPcRatioDown', {}, item, setReleasTime(item['日期']))
            requests.post('http://host.docker.internal:9001/telegraf', data=data.encode('utf-8'))
            # requests.post('http://localhost:9001/telegraf', data=data.encode('utf-8'))
            return item

        if spider.name == 'dlFutDataDown':
            data = make_influx_line('dlFutDataDown', {}, item, setReleasTime(item['交易日期']))
            requests.post('http://host.docker.internal:9001/telegraf', data=data.encode('utf-8'))
            return item

        return {}
