"""Filters a list of symbols in parallel."""

from google.protobuf import text_format
from multiprocessing import Pool
import os
import shutil

import flags
import util
import week_result_pb2

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_threads", required=False, type=int, default=10,
                         help="Number of threads")
FLAGS = flags.Parse()


def FilterWorker(filename, output_path):
    data = week_result_pb2.WeekResult()
    with open(filename, 'r') as f:
        text_format.Merge(f.read(), data)
    if data.market_cap < 30 or data.market_cap > 350:
        return
    for poly in data.poly:
        if poly.order == 1:
            for coef in poly.coef:
                if coef < 1.0:
                    return
                break
        if poly.order == 2:
            if not poly.convex:
                return
    # At this point, we have a good symbol.
    basename = util.Basename(filename)
    shutil.copyfile(filename, os.path.join(output_path, basename + '.res'))
    png_file = os.path.join(os.path.dirname(filename), basename + '.png')
    shutil.copyfile(png_file, os.path.join(output_path, basename + '.png'))


def main():
    data_files = util.SafeReadLines(FLAGS.filename)
    print 'Processing %d files' % len(data_files)
    pool = Pool(processes=FLAGS.num_threads)
    for data_file in data_files:
        pool.apply_async(FilterWorker, [data_file, FLAGS.output_path])
    pool.close()
    pool.join()


if __name__ == "__main__":    
    main()
