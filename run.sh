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
# echo -e "\n" >> /etc/cron.d/hello-cron
# echo -e "* * * * * root cd /code && /usr/local/bin/scrapyd-client schedule -p taifex_scraper taifex" >> /etc/cron.d/hello-cron
echo -e "* * * * * root cd /code && /usr/local/bin/scrapyd-client schedule -p taifex_scraper dlPcRatioDown" >> /etc/cron.d/scrapy-cron
chmod 0644 /etc/cron.d/scrapy-cron
service cron start


tail -f scrapyd.log