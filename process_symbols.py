#!/usr/bin/env python
"""Process data of a list of symbols in parallel.

  for f in `ls data/csv/*.csv`; do echo $f; done > /tmp/list
  <bin> --filename /tmp/list --num_weeks 10 --output_path data/res/ \
        --num_threads=10
"""

from multiprocessing import Pool, Manager

import flags
import util
import signal
import symbol_data_generator
import time

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_weeks", type=int, default=-1,
                         help="Number of weeks. Starting from last")
flags.FLAGS.add_argument("--num_threads", required=False, type=int, default=10,
                         help="Number of threads")
flags.FLAGS.add_argument("--make_graphs", default=False,
                         help="Generate graph of each symbol",
                         action="store_true")
FLAGS = flags.Parse()


def InitWorker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def ProcessorWorker(runner, filename, num_weeks, output_path, make_graphs):
    runner.Run(filename, num_weeks, output_path, make_graphs)


def main():
    data_files = util.SafeReadLines(FLAGS.filename)
    print 'Processing %d files' % len(data_files)
    pool = Pool(FLAGS.num_threads, InitWorker)
    manager = Manager()
    lock = manager.Lock()
    runner = symbol_data_generator.Runner(lock)
    for data_file in data_files:
        pool.apply_async(ProcessorWorker, [runner, data_file, FLAGS.num_weeks,
                                           FLAGS.output_path, FLAGS.make_graphs])

    try:
        wait_seconds = len(data_files) / FLAGS.num_threads / 2
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
        print 'Processed %d files' % len(data_files)


if __name__ == "__main__":    
    main()
