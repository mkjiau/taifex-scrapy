# docker build -t my-scrapyd-cron .

FROM my-scrapyd-onbuild

RUN apt-get update
RUN apt-get -y install cron

WORKDIR /code
VOLUME [ "/code" ]
EXPOSE 6800
CMD [ "./run.sh" ]