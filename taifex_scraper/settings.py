# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from pathlib import Path
import os

# dotenv
# set PYTHON_ENV=production && scrapy crawl dlPcRatioDown  
PYTHON_ENV = '' if os.environ.get("PYTHON_ENV") == None else os.environ.get("PYTHON_ENV")
PYTHON_ENV = PYTHON_ENV.strip()
if PYTHON_ENV == "production":
    env_path = Path('.') / '.env.production'
else:
    env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

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