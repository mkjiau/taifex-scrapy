# -*- coding: utf-8 -*-
import scrapy


class DloptdatadownSpider(scrapy.Spider):
    name = 'dlOptDataDown'
    allowed_domains = ['http://example.com']
    start_urls = ['http://http://example.com/']

    def parse(self, response):
        pass
