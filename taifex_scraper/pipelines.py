# -*- coding: utf-8 -*-
import requests
from .utils import make_influx_line

class TaifexScraperPipeline(object):
    def process_item(self, item, spider):
        data = make_influx_line('dlPcRatioDown', {}, item, item['日期'])
        requests.post('http://localhost:9001/telegraf', data=data.encode('utf-8'))
        return item
