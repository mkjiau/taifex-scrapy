# TAIFEX Scraper

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

This is a [Scrapy](https://github.com/scrapy/scrapy) project which can be used to crawl [TAIFEX](https://www.taifex.com.tw) website to scrape information about Taiwan futures and options. 


## Installation
Using CMD is prefered.

##### Prepare Python 3.6 in any way
```
# e.g. use anaconda to create a Python 3.6 env named python36, and activate it 
CMD> conda activate python36
```

##### Create and activate a virtual environment.
```
(python36) CMD> pipenv shell
```
##### Install all dependencies.
```
(taifex-scrapy) (python36) CMD> pipenv install
```


## Crawling

##### Directly Activate taifex-scrapy 
```
CMD> C:\Users\{YOUR_NAME}\.virtualenvs\taifex-scrapy-lMUq6lYm\Scripts\activate
```

##### Start the crawler
```
(taifex-scrapy) CMD> scrapy crawl taifex
```
Data will be stored in `json` file located at `data/taifex.json`.


## Scrapyd
```
docker run --rm --name aaaa -p 6800:6800  my-scrapyd-a

scrapyd-deploy -l
scrapyd-deploy

scrapyd-client projects
scrapyd-client spiders -p taifex_scraper

scrapyd-client schedule -p taifex_scraper taifex

#scrapyd-client schedule -p taifex_scraper \* 
#scrapyd-client schedule -h
```

## ScrapyRT
```
# https://scrapyrt.readthedocs.io/en/stable/api.html#scrapyrt-http-api
curl -v "http://localhost:9080/crawl.json?spider_name=taifex&start_requests=true"
```

## References
https://github.com/mkjiau/IMDB-Scraper





