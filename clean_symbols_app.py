"""Gets a list of symbols and creates a new list with the ones that exists.

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
