Aggro is a simple feed aggregator written in python using gevent<br>

## Installation

To install the requirements: <br>
pip install -r requirements.txt<br>

And to install aggro:<br>

python setup.py install<br>

## Usage

Code examples can be found in the examples folder.

This is from the examples/basic.py file:

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
    aggro.start() # runs indefinitely

This will kick off the aggregator observing the four given feeds at the given update interval (default 60 seconds). <br>
Whenever a new entry is found the given new_entry_handler is called.