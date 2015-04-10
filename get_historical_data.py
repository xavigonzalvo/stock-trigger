#!/usr/bin/python
"""Parallel tool to get historical information of a list of symbols.

  <tool> --filename <symbols> --output_path <output>
"""

from datetime import date
from multiprocessing import Pool
import os
import signal
import time

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
flags.FLAGS.add_argument("--period", required=False, default='w',
                         help="One of w (week) or d (day)")
FLAGS = flags.Parse()


def InitWorker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def FetcherWorker(worker_id, fetcher, symbols):
    """Worker to fetch symbol information."""    
    for i in range(len(symbols)):
        symbol = symbols[i]
        current_year = date.today().year
        filename = '%s-%d-%d-week.csv' % (symbol, FLAGS.from_year, current_year)
        output = os.path.join(FLAGS.output_path, filename)
        if os.path.exists(output) and not FLAGS.overwrite:
            continue
        try:
            data = fetcher.GetHistorical(symbol, FLAGS.from_year,
                                         current_year, FLAGS.period)
        except YFetcher.YahooFinanceFetcherError, e:
            continue
        with open(output, 'w') as f:
            f.write(data)
    print 'Worker %d processed %d symbols' % (worker_id, len(symbols))
            

def main():
    if FLAGS.symbol:
        symbols = [FLAGS.symbol]
    else:
        symbols = util.SafeReadLines(FLAGS.filename)

    print "%d symbols to fetch" % len(symbols)
    fetcher = YFetcher.YahooFinanceFetcher()
    pool = Pool(FLAGS.num_threads, InitWorker)
    if len(symbols) > FLAGS.num_threads:
        chunk_size = len(symbols) / FLAGS.num_threads
        chunks = [symbols[x:x+chunk_size]
                  for x in xrange(0, len(symbols), chunk_size)]
    else:
        chunks = symbols
    print 'chunks: %d, chunk size: %d' % (len(chunks), chunk_size)
    for i in range(len(chunks)):
        pool.apply_async(FetcherWorker, [i, fetcher, chunks[i]])

    # Wait until all tasks finish.
    try:
        wait_seconds = chunk_size / 3
        print '\rWaiting %d seconds...' % wait_seconds
        time.sleep(wait_seconds)
    except KeyboardInterrupt as e:
        print 'STOPPING'
        # Signal all workers to quit
        pool.terminate()
        pool.join()
    else:
        pool.close()
        pool.join()
        print 'Processed %d symbols' % len(symbols)


if __name__ == "__main__":    
    main()
