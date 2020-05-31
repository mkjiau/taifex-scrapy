# -*- coding: utf-8 -*-

BOT_NAME = 'taifex_scraper'

SPIDER_MODULES = ['taifex_scraper.spiders']
NEWSPIDER_MODULE = 'taifex_scraper.spiders'

# Saving the output in json format
FEED_URI = 'data/%(name)s.json'
FEED_FORMAT = 'json'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'taifex_scraper.pipelines.TaifexScraperPipeline': 300,
}