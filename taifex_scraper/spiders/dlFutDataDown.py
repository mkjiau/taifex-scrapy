# -*- coding: utf-8 -*-
from scrapy import FormRequest, Item, Field, Request, Spider
from scrapy.spiders import CSVFeedSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime, timedelta
import urllib
import pandas as pd
import io
# from taifex_scraper.items import *
from ..utils import first_date_of_month, last_date_of_month

class DlfutdatadownSpider(Spider):
    name = 'dlFutDataDown'
    allowed_domains = ['taifex.com.tw']

    selected_date = datetime.now().strftime('%Y/%m/%d')
    start_month = None
    end_month = None
    commodity_id = 'TX'

    def start_requests(self):
        # scrapy crawl -a start_month="2010/12" -a end_month="2011/3" -a commodity_id="TE" dlFutDataDown
        # scrapyd-client schedule --arg start_month="2010/12" --arg end_month="2011/3" -p taifex_scraper dlFutDataDown
        if self.start_month != None and self.end_month != None:
            return self.__month_range_requests(self.start_month, self.end_month, self.commodity_id)

        # scrapy crawl -a selected_date="2020/06/02" dlFutDataDown
        # scrapyd-client schedule --arg selected_date="2020/06/02" -p taifex_scraper dlFutDataDown
        return self.__selected_date_request(self.selected_date, self.commodity_id)
    
    def parse_data(self, response):
        df = pd.read_csv(io.StringIO(response.text.replace(',\r\n','\r\n').replace(" ","")))

        # 交易日期
        # 契約
        # 到期月份(週別)
        df['開盤價'] = df["開盤價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['最高價'] = df["最高價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['最低價'] = df["最低價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['收盤價'] = df["收盤價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['漲跌價'] = df["漲跌價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['漲跌%'] = df["漲跌%"].apply(lambda s: s.replace('%', '')).apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['成交量'] = df["成交量"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['結算價'] = df["結算價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['未沖銷契約數'] = df["未沖銷契約數"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['最後最佳買價'] = df["最後最佳買價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['最後最佳賣價'] = df["最後最佳賣價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['歷史最高價'] = df["歷史最高價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['歷史最低價'] = df["歷史最低價"].apply(lambda s: 0 if s == '-' else s).apply(lambda s: float(s))
        df['是否因訊息面暫停交易'] = df["是否因訊息面暫停交易"].apply(lambda s: '' if s != s else s)
        # 交易時段
        df['價差對單式委託成交量'] = df["價差對單式委託成交量"].apply(lambda s: '' if s != s else s)

        items = df.to_dict(orient='records')
        
        return items

    def __month_range_requests(self, start_month, end_month, commodity_id):
        reqs = []

        for m in pd.date_range(start_month, end_month, freq='MS').tolist():
            m = m.strftime("%Y/%m")
            data = {
                'queryStartDate': first_date_of_month(m).strftime('%Y/%m/%d'), # '2019/03/20'
                'queryEndDate': last_date_of_month(m).strftime('%Y/%m/%d'),    # '2019/04/19'
                'commodity_id': commodity_id,
                'down_type': 1
            }
            req = Request(url='https://www.taifex.com.tw/cht/3/dlFutDataDown', 
                            method='POST', 
                            callback=self.parse_data,
                            headers={'Content-Type': 'application/x-www-form-urlencoded'},
                            body=urllib.parse.urlencode(data, doseq=True))
            reqs.append(req)
        return reqs

    def __selected_date_request(self, selected_date, commodity_id):
        data = {
            'queryStartDate': selected_date, # '2020/6/3'
            'queryEndDate': selected_date,   # '2019/6/3'
            'commodity_id': commodity_id, # 'all', 'TX', 'MTX', 'TE', 'TF', etc. see https://www.taifex.com.tw/cht/3/dlFutDailyMarketView
            'down_type': 1
        }
        req = Request(url='https://www.taifex.com.tw/cht/3/dlFutDataDown', 
                        method='POST', 
                        callback=self.parse_data,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        body=urllib.parse.urlencode(data, doseq=True))
        return [req]
