import flags
import os

from yahoo_finance_fetcher import *

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the list of symbols")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--output_valid_symbols_path", required=True,
                         help="Output file containing a list of valid symbols")
FLAGS = flags.Parse()


def main():
    symbols = []
    with open(FLAGS.filename) as f:
        for symbol in f.readlines():
            symbols.append(symbol.strip())

    print "%d symbols to fetch" % len(symbols)
    fetcher = YahooFinanceFetcher()
    count = 0
    valid_symbols = []
    for symbol in symbols:
        filename = '%s-%d-%d-week.csv' % (symbol, 2010, 2013)
        output = os.path.join(FLAGS.output_path, filename)
        if os.path.exists(output):
            valid_symbols.append(symbol)
            continue
        print 'Fetching %s ...' % symbol
        try:
            data = fetcher.GetHistorical(symbol, 2010, 2013, 'w')
        except Error, e:
            print e
            continue
        with open(output, 'w') as f:
            f.write(data)
        count = count + 1
        valid_symbols.append(symbol)
    print 'Fetched %d symbols' % count
    with open(FLAGS.output_valid_symbols_path, 'w') as f:
        f.writelines('\n'.join(valid_symbols))


if __name__ == "__main__":    
    main()
