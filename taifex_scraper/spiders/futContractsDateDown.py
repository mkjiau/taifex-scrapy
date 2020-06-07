# -*- coding: utf-8 -*-
import scrapy


class FutcontractsdatedownSpider(scrapy.Spider):
    name = 'futContractsDateDown'
    allowed_domains = ['http://example.com']
    start_urls = ['http://http://example.com/']

    def parse(self, response):
        pass
