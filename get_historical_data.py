"""Parallel tool to get historical information of a list of symbols.

  <tool> --filename <symbols> --output_path <output>
"""

import flags
import os
from multiprocessing import Pool

import yahoo_finance_fetcher as YFetcher

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the list of symbols")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_threads", required=False, type=int, default=10,
                         help="Number of threads")
FLAGS = flags.Parse()


def FetcherWorker(fetcher, symbol):
    """Worker to fetch symbol information."""
    filename = '%s-%d-%d-week.csv' % (symbol, 2010, 2013)
    output = os.path.join(FLAGS.output_path, filename)
    if os.path.exists(output):
        return
    print 'Fetching %s ...' % symbol
    try:
        data = fetcher.GetHistorical(symbol, 2010, 2013, 'w')
    except YFetcher.YahooFinanceFetcherError, e:
        print e
        return
    with open(output, 'w') as f:
        f.write(data)


def main():
    symbols = []
    with open(FLAGS.filename) as f:
        for symbol in f.readlines():
            symbols.append(symbol.strip())

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
