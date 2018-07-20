#!/usr/bin/env python2
"""Tool to get historical information of a list of symbols.

  <tool> --filename <symbols> --output_path <output>

The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import date
import os
import time

import flags
import util
import alpha_advantage_fetcher as finance_fetcher

flags.FLAGS.add_argument("--symbol", required=False,
                         help="A single symbol")
flags.FLAGS.add_argument("--filename", required=False,
                         help="Path to the list of symbols")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--overwrite",
                         help="Overwrite symbols", default=False,
                         action="store_true")
flags.FLAGS.add_argument("--from_year", required=False, type=int, default=2010,
                         help="Get data from this year")
flags.FLAGS.add_argument("--period", required=False, default='w',
                         help="One of w (week) or d (day)")
FLAGS = flags.Parse()


def fetch_data(worker_id, fetcher, symbols):
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
        except finance_fetcher.Error as e:
            pass
        with open(output, 'w') as f:
            f.write(data)
    print ('Worker %d processed %d symbols' % (worker_id, len(symbols)))


def main():
    if FLAGS.symbol:
        symbols = [FLAGS.symbol]
    else:
        symbols = util.SafeReadLines(FLAGS.filename)

    print ('%d symbols to fetch' % len(symbols))
    fetcher = finance_fetcher.FinanceFetcher()
    fetch_data(worker_id=0, fetcher=fetcher, symbols=symbols)
    print ('Processed %d symbols' % len(symbols))


if __name__ == '__main__':
    main()
