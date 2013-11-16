"""Filters a list of symbols in parallel."""

from multiprocessing import Pool
import os
import shutil

import filter_pb2
import flags
import util
import week_result_pb2

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--filter", required=True,
                         help="Path to the filter definition as a text proto")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_threads", required=False, type=int, default=10,
                         help="Number of threads")
FLAGS = flags.Parse()


def FilterWorker(data_filter, filename, output_path):
    data = week_result_pb2.WeekResult()
    util.ReadTextProto(filename, data)
    
    if (data.market_cap < data_filter.min_market_cap or
        data.market_cap > data_filter.max_market_cap):
        return
    if data.mean - data.std < 0 and not data_filter.negative_gradient_variation:
        return  # mean variation can go negative
    if data.mean < data_filter.min_mean:
        return  # if increases less than X% in average
    for poly in data.poly:
        if poly.order == 1:
            for coef in poly.coef:
                if coef < data_filter.min_linear_gradient:
                    return
                break
        if poly.order == 2:
            if poly.convex != data_filter.convex:
                return

    # At this point, we have a good symbol.
    basename = util.Basename(filename)
    shutil.copyfile(filename, os.path.join(output_path, basename + '.res'))
    png_file = os.path.join(os.path.dirname(filename), basename + '.png')
    shutil.copyfile(png_file, os.path.join(output_path, basename + '.png'))


def main():
    data_filter = filter_pb2.Filter()
    util.ReadTextProto(FLAGS.filter, data_filter)
    print data_filter

    data_files = util.SafeReadLines(FLAGS.filename)
    print 'Processing %d files' % len(data_files)
    pool = Pool(processes=FLAGS.num_threads)
    for data_file in data_files:
        pool.apply_async(FilterWorker, [data_filter, data_file,
                                        FLAGS.output_path])
    pool.close()
    pool.join()


if __name__ == "__main__":    
    main()
