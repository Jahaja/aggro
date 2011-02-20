import logging
from aggro import Aggregator

logging.basicConfig(level=logging.DEBUG)

feeds = {
    "DN" : "http://www.dn.se/nyheter/m/rss",
    "Svd" : "http://www.svd.se/?service=rss&type=latest",
    "Expressen" : "http://www.expressen.se/1.573280?standAlone=true",
    "Aftonbladet" : "http://www.aftonbladet.se/rss.xml"
}

def new_entry(feed, entry, checksum):
    print feed, entry.date, entry.title

aggro = Aggregator(feeds, new_entry)
aggro.start()