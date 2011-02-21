# coding=UTF-8
from datetime import datetime

import feedparser
import gevent
from zlib import adler32
import logging
from collections import deque

logger = logging.getLogger("aggregator")

class AggregatorException(Exception):
    pass

class Aggregator(object):
    _checksums_per_feed = 500
    checksums = {}

    def __init__(self, feeds, new_entry_handler, min_date=None, update_interval=60):
        if not callable(new_entry_handler):
            raise AggregatorException("Given new_entry_handler is not callable")

        if not isinstance(feeds, dict):
            raise AggregatorException("The feeds parameter must be a dict.")

        if min_date and not isinstance(min_date, datetime):
            raise AggregatorException("The optional min_date parameter, if given, must be an instance of datetime")

        self.feeds = feeds
        self.new_entry_handler = new_entry_handler
        self.checksums = dict([(feed, deque(maxlen=self._checksums_per_feed)) for feed in self.feeds.keys()])
        self.min_date = min_date
        self.update_interval = update_interval

    def start(self):
        logger.info("Starting aggregation of %d feeds" % len(self.feeds))
        workers = []
        for feed, url in self.feeds.iteritems():
            workers.append(gevent.spawn(self.worker, feed, url))

        gevent.joinall(workers)

    def worker(self, feed, url):
        logger.info("Work starting for feed %s" % feed)
        last_etag = None
        last_modified = None
        while True:
            d = feedparser.parse(url, etag=last_etag, modified=last_modified)
            if d and hasattr(d, 'status'):
                if d.status == 304:
                    logger.info("Feed '%s' returned status code 304 (Not Modified)." % feed)
                elif d.status in (301, 302):
                    self.handle_redirect(feed, d)
                elif d.status == 200:
                    last_etag = d.etag if hasattr(d, "etag") else None
                    last_modified = d.modified if hasattr(d, "modified") else None
                    gevent.spawn(self.parse, feed, d)
                else:
                    self.handle_unknown_status(feed, d)
            else:
                logging.warning("Received response for feed %s did not contain a HTTP status code. Response discarded." % feed)

            gevent.sleep(self.update_interval)

    def handle_redirect(self, feed, document):
        logger.info("Redirect found for feed %s, updated url will be used next update." % feed)
        if hasattr(document, "href") and document.href:
            self.feeds[feed] = document.href

    def handle_unknown_status(self, feed, d):
        logger.warning("Feed responded with an unknown status code of %d" % d.status)

    def get_checksum(self, entry):
        checksum = adler32(entry.title.encode("utf-8") + entry.id.encode("utf-8"))
        return checksum

    def parse(self, feed, document):
        if not document:
            logger.warning("Feed (%s) seems empty" % feed)

        new_items = 0
        for entry in document.entries:
            checksum = self.get_checksum(entry)
            if checksum not in self.checksums[feed] and (not self.min_date or entry.date > self.min_date):
                new_items += 1
                self.checksums[feed].append(checksum)
                gevent.spawn(self.new_entry_handler, feed, entry, checksum)

        logger.info("%d new items found for feed %s." % (new_items, feed))

