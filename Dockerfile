# docker build -t my-scrapyd-cron .

FROM docker.io/mkjiau/docker-scrapyd:py3-onbuild-1.0.0

RUN apt-get update
RUN apt-get -y install cron

WORKDIR /code
VOLUME [ "/code" ]
EXPOSE 6800
CMD [ "./run.sh" ]
