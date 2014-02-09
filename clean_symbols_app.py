"""Gets a list of symbols and creates a new list with the ones that exists.
"""

import sys

import flags
import util
import yahoo_finance_fetcher

flags.FLAGS.add_argument("--input", required=True,
                         help="Path to the list of symbols")
flags.FLAGS.add_argument("--output", required=True,
                         help="Path to the new list of symbols")
FLAGS = flags.Parse()


def main():
    symbols = util.SafeReadLines(FLAGS.input)
    total = len(symbols)
    print 'Processing %d symbols' % total
    fetcher = yahoo_finance_fetcher.YahooFinanceFetcher()
    new_list = {}
    count = 0
    for symbol in symbols:
        try:
            name = fetcher.GetName(symbol)
            if name:
                new_list[symbol] = 1
        except yahoo_finance_fetcher.YahooFinanceFetcherError, e:
            pass
        progress = count / float(total) * 100
        sys.stdout.write("%.1f %%\r" % progress)
        sys.stdout.flush()
        count += 1
    with open(FLAGS.output, 'w') as f:
        f.writelines(new_list)


if __name__ == "__main__":    
    main()
