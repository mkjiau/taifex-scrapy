# -*- coding: utf-8 -*-
from scrapy import FormRequest, Item, Field, Request, Spider
from scrapy.spiders import CSVFeedSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime, timedelta
import urllib
import pandas as pd
import io
from taifex_scraper.items import *
from ..utils import first_date_of_month, last_date_of_month

class DlpcratiodownSpider(Spider):
    name = 'dlPcRatioDown'
    allowed_domains = ['taifex.com.tw']

    def start_requests(self):
        # scrapy crawl -a start_month="2010/12" -a end_month="2011/3" dlPcRatioDown
        # scrapyd-client schedule --arg start_month="2010/12" --arg end_month="2011/3" -p taifex_scraper dlPcRatioDown
        if hasattr(self, 'start_month') and hasattr(self, 'end_month'):
            return self._month_range_requests(self.start_month, self.end_month)

        # scrapy crawl -a selected_date="2020/06/02" dlPcRatioDown
        # scrapyd-client schedule --arg selected_date="2020/06/02" -p taifex_scraper dlPcRatioDown
        selected_date = self.selected_date if hasattr(self, 'selected_date') else datetime.now().strftime('%Y/%m/%d')
        return self._selected_date_request(selected_date)
    
    def parse_data(self, response):

        df = pd.read_csv(io.StringIO(response.text.replace(',\r\n','\r\n')))

        # items = []
        # for index, row in df.iterrows():
        #     print(row['日期'], row['買權未平倉量'])
        #     item = TaifexScraperItem()
        #     item['date'] = row['日期']
        #     item['oi'] = row['買權未平倉量']
        #     # yield item
        #     items.append(item)

        items = df.to_dict(orient='records')
        
        return items

    def _month_range_requests(self, start_month, end_month):
        reqs = []

        for m in pd.date_range(start_month, end_month, freq='MS').strftime("%Y/%m").tolist():
            data = {
                'queryStartDate': first_date_of_month(m).strftime('%Y/%m/%d'), # '2019/03/20'
                'queryEndDate': last_date_of_month(m).strftime('%Y/%m/%d')     # '2019/04/19'
            }
            req = Request(url='https://www.taifex.com.tw/cht/3/dlPcRatioDown', 
                            method='POST', 
                            callback=self.parse_data,
                            headers={'Content-Type': 'application/x-www-form-urlencoded'},
                            body=urllib.parse.urlencode(data, doseq=True))
            reqs.append(req)
        return reqs

    def _selected_date_request(self, selected_date):
        data = {
            'queryStartDate': selected_date, # '2020/6/3'
            'queryEndDate': selected_date    # '2019/6/3'
        }
        req = Request(url='https://www.taifex.com.tw/cht/3/dlPcRatioDown', 
                        method='POST', 
                        callback=self.parse_data,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        body=urllib.parse.urlencode(data, doseq=True))
        return [req]
