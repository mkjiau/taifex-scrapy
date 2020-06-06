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
scrapyd > scrapyd.log 2>&1 &
sleep 10

echo "deploying scrapy projects to scrapyd"
scrapyd-deploy
echo "all deployed"

echo "starting cron to execute scrapy schedules ..."
# echo -e "\n" >> /etc/cron.d/hello-cron
# echo -e "* * * * * root cd /code && /usr/local/bin/scrapyd-client schedule -p taifex_scraper taifex" >> /etc/cron.d/hello-cron
echo -e "* * * * * root cd /code && /usr/local/bin/scrapyd-client schedule -p taifex_scraper taifex" >> /etc/cron.d/scrapy-cron
chmod 0644 /etc/cron.d/scrapy-cron
service cron start


tail -f scrapyd.log