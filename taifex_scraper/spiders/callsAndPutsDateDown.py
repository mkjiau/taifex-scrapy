# -*- coding: utf-8 -*-
import scrapy


class CallsandputsdatedownSpider(scrapy.Spider):
    name = 'callsAndPutsDateDown'
    allowed_domains = ['http://example.com']
    start_urls = ['http://http://example.com/']

    def parse(self, response):
        pass
