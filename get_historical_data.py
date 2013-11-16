"""Parallel tool to get historical information of a list of symbols.

  <tool> --filename <symbols> --output_path <output>
"""

import os
from datetime import date
from multiprocessing import Pool

import flags
import util
import yahoo_finance_fetcher as YFetcher

flags.FLAGS.add_argument("--symbol", required=False,
                         help="A single symbol")
flags.FLAGS.add_argument("--filename", required=False,
                         help="Path to the list of symbols")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--overwrite",
                         help="Overwrite symbols", default=False,
                         action="store_true")
flags.FLAGS.add_argument("--num_threads", required=False, type=int, default=10,
                         help="Number of threads")
flags.FLAGS.add_argument("--from_year", required=False, type=int, default=2010,
                         help="Get data from this year")
FLAGS = flags.Parse()


def FetcherWorker(fetcher, symbol):
    """Worker to fetch symbol information."""
    current_year = date.today().year
    filename = '%s-%d-%d-week.csv' % (symbol, FLAGS.from_year, current_year)
    output = os.path.join(FLAGS.output_path, filename)
    if os.path.exists(output) and not FLAGS.overwrite:
        return
    print 'Fetching %s ...' % symbol
    try:
        data = fetcher.GetHistorical(symbol, FLAGS.from_year,
                                     current_year, 'w')
    except YFetcher.YahooFinanceFetcherError, e:
        print e
        return
    with open(output, 'w') as f:
        f.write(data)


def main():
    if FLAGS.symbol:
        symbols = [FLAGS.symbol]
    else:
        symbols = util.SafeReadLines(FLAGS.filename)

    print "%d symbols to fetch" % len(symbols)
    fetcher = YFetcher.YahooFinanceFetcher()
    count = 0
    pool = Pool(processes=FLAGS.num_threads)
    for symbol in symbols:
        pool.apply_async(FetcherWorker, [fetcher, symbol])
        count = count + 1
    pool.close()
    pool.join()
    print 'Fetched %d symbols' % count


if __name__ == "__main__":    
    main()
