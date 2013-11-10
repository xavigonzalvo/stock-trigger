import urllib
import feedparser
from dateutil import parser

server = 'http://finance.yahoo.com/rss/headline?'
symbol = 'TEP.L'

data = urllib.urlencode({'s': symbol})

feed = feedparser.parse(server + data)

print server + data

for item in feed.entries:
        if 'published' in item.keys():
                dt = parser.parse(item['published'])
                print "%s/%s/%s" % (dt.day, dt.month, dt.year)
        if 'pubDate' in item.keys():
                dt = parser.parse(item['pubDate'])
                print dt
        print item.title
