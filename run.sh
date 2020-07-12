#!/bin/bash
set -eo pipefail

echo "current directory is $(pwd)"
# cd /code

if [[ -f "twistd.pid" ]]; then
  echo "twistd.pid exists"
  rm twistd.pid
  echo "twistd.pid removed"
fi

if [[ -f "scrapyd.log" ]]; then
  echo "scrapyd.log exists"
  rm scrapyd.log
  echo "scrapyd.log removed"
fi

echo "launch scrapyd"
touch scrapyd.log
scrapyd > scrapyd.log 2>&1 &
sleep 3

echo "deploying the scrapy project onto scrapyd"
scrapyd-deploy
echo "The project deployed and the following spiders ready"
scrapyd-client spiders -p taifex_scraper

echo "starting cron to execute scrapy schedules ..."
if [[ -f "/etc/cron.d/scrapy-cron" ]]; then
  echo "/etc/cron.d/scrapy-cron exists"
  rm -fr /etc/cron.d/scrapy-cron
  echo "/etc/cron.d/scrapy-cron removed"
fi
# echo -e "*/2 * * * * root cd /code && /usr/local/bin/scrapyd-client schedule -p taifex_scraper dlPcRatioDown" >> /etc/cron.d/scrapy-cron

# At 17:00 (GMT+8) on every day-of-week from Monday through Friday.
echo -e "0 9 * * 1-5 root cd /code && /usr/local/bin/scrapyd-client schedule -p taifex_scraper dlPcRatioDown" >> /etc/cron.d/scrapy-cron
echo -e "0 9 * * 1-5 root cd /code && /usr/local/bin/scrapyd-client schedule -p taifex_scraper dlFutDataDown" >> /etc/cron.d/scrapy-cron

chmod 0644 /etc/cron.d/scrapy-cron
service cron start


tail -f scrapyd.log