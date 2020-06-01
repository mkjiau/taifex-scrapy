# -*- coding: utf-8 -*-
from scrapy import FormRequest, Item, Field, Request, Spider
from scrapy.spiders import CSVFeedSpider, Rule
from scrapy.linkextractors import LinkExtractor
import datetime
from datetime import timedelta
import urllib
import pandas as pd
import io
from taifex_scraper.items import *
from ..utils import first_date_of_month, last_date_of_month


my_bias_day = 0
tx_contract_month = "202006"

start_date = datetime.datetime.today() - timedelta(days=30) - timedelta(days=my_bias_day)
end_date = datetime.datetime.today() - timedelta(days=my_bias_day)

data = {
    'queryStartDate': start_date.strftime('%Y/%m/%d'), # '2019/03/20'
    'queryEndDate': end_date.strftime('%Y/%m/%d')      # '2019/04/19'
}

class TaifexSpider(Spider):
    name = 'taifex'
    allowed_domains = ['taifex.com.tw']
    # start_urls = [SEARCH_QUERY]

    # def start_requests(self):
    #     yield FormRequest("https://www.taifex.com.tw/cht/3/dlPcRatioDown",
    #                                formdata=data,
    #                                callback=self.cb)
    # def start_requests(self):
    #     yield Request(url='https://www.taifex.com.tw/cht/3/dlPcRatioDown', 
    #                                 method='POST', 
    #                                 callback=self.parse_data,
    #                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
    #                                 body=urllib.parse.urlencode(data, doseq=True))
    def start_requests(self):
        month_reqs = []
        for m in pd.date_range('2000/1','2010/1', freq='MS').strftime("%Y/%m").tolist():
            data2 = {
                'queryStartDate': first_date_of_month(m).strftime('%Y/%m/%d'), # '2019/03/20'
                'queryEndDate': last_date_of_month(m).strftime('%Y/%m/%d')      # '2019/04/19'
            }
            req = Request(url='https://www.taifex.com.tw/cht/3/dlPcRatioDown', 
                            method='POST', 
                            callback=self.parse_data,
                            headers={'Content-Type': 'application/x-www-form-urlencoded'},
                            body=urllib.parse.urlencode(data2, doseq=True))
            month_reqs.append(req)
        return month_reqs
    
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
