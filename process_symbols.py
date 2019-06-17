#!/usr/bin/env python3
"""Process data of a list of symbols in parallel.

  for f in `ls data/csv/*.csv`; do echo $f; done > /tmp/list
  <bin> --filename /tmp/list --num_weeks 10 --output_path data/res/ \
        --num_threads=10

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

from absl import logging
from multiprocessing import Pool, Manager, Process
from multiprocessing.pool import ThreadPool

import flags
import util
import signal
import symbol_data_generator
import time

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_days", type=int, default=30,
                         help="Number of days. Starting from last")
flags.FLAGS.add_argument("--window", type=int, default=5,
                         help="Number of days to average over")
flags.FLAGS.add_argument("--num_threads", required=False, type=int, default=10,
                         help="Number of threads")
flags.FLAGS.add_argument("--make_graphs", default=False,
                         help="Generate graph of each symbol",
                         action="store_true")
flags.FLAGS.add_argument("--iexcloud_token", required=True,
                         help="iexcloud token")
FLAGS = flags.Parse()


def _process_worker(runner, filename, num_days, window, output_path, make_graphs):
  runner.Run(filename, num_days, window, output_path, make_graphs)


def main():
  logging.set_verbosity(logging.INFO)
  data_files = util.SafeReadLines(FLAGS.filename)
  print('Processing %d files' % len(data_files))
  pool = ThreadPool(FLAGS.num_threads)
  manager = Manager()
  lock = manager.Lock()
  runner = symbol_data_generator.Runner(
      lock, iexcloud_token=FLAGS.iexcloud_token)
  for data_file in data_files:
    _process_worker(runner, data_file, FLAGS.num_days,
                    FLAGS.window, FLAGS.output_path,
                    FLAGS.make_graphs)

  # try:
  #   wait_seconds = len(data_files) / FLAGS.num_threads / 2
  #   print('\rWaiting %d seconds...' % wait_seconds)
  #   time.sleep(wait_seconds)
  # except KeyboardInterrupt as e:
  #   print('STOPPING')
  #   # Signal all workers to quit
  #   pool.terminate()
  #   pool.join()
  # else:
  #   pool.close()
  #   pool.join()
    print('Processed %d files' % len(data_files))


if __name__ == "__main__":
  main()
