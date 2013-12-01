"""Process data of a list of symbols in parallel.
"""

from multiprocessing import Pool, Manager

import flags
import util
import symbol_data_generator

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


def ProcessorWorker(runner, filename, num_weeks, output_path, make_graphs):
    runner.Run(filename, num_weeks, output_path, make_graphs)


def main():
    data_files = util.SafeReadLines(FLAGS.filename)
    print 'Processing %d files' % len(data_files)
    pool = Pool(processes=FLAGS.num_threads)
    manager = Manager()
    lock = manager.Lock()
    runner = symbol_data_generator.Runner(lock)
    for data_file in data_files:
        pool.apply_async(ProcessorWorker, [runner, data_file, FLAGS.num_weeks,
                                           FLAGS.output_path, FLAGS.make_graphs])
    pool.close()
    pool.join()


if __name__ == "__main__":    
    main()
