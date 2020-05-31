# -*- coding: utf-8 -*-

import scrapy


class TaifexScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    oi = scrapy.Field()
    pass
