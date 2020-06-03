FROM my-scrapyd-onbuild

# VOLUME /etc/scrapyd/ /var/lib/scrapyd/
EXPOSE 6800
CMD ["scrapyd"]