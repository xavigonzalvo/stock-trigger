"""Process data of a list of symbols in parallel.
"""

from multiprocessing import Pool

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
FLAGS = flags.Parse()


def ProcessorWorker(filename, num_weeks, output_path):
    symbol_data_generator.Run(filename, num_weeks, output_path)


def main():
    data_files = util.SafeReadLines(FLAGS.filename)
    print 'Processing %d files' % len(data_files)
    pool = Pool(processes=FLAGS.num_threads)
    for data_file in data_files:
        pool.apply_async(ProcessorWorker, [data_file, FLAGS.num_weeks,
                                           FLAGS.output_path])
    pool.close()
    pool.join()


if __name__ == "__main__":    
    main()