#!/usr/bin/env python
"""Filters a list of symbols in parallel.

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

from multiprocessing import Pool
import os
import shutil

import filter_utils
import flags
import util
import protos.filter_pb2 as filter_pb2
import protos.week_result_pb2 as week_result_pb2

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--filter", required=True,
                         help="Path to the filter definition as a text proto")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_threads", required=False, type=int, default=10,
                         help="Number of threads")
FLAGS = flags.Parse()


def FilterWorker(filter_serialized, filename, output_path):
    data_filter = filter_pb2.Filter()
    data_filter.ParseFromString(filter_serialized)

    data = week_result_pb2.WeekResult()
    util.ReadTextProto(filename, data)
    
    if filter_utils.Filter(data, data_filter):
        return

    # At this point, we have a good symbol.
    basename = util.Basename(filename)
    shutil.copyfile(filename, os.path.join(output_path, basename + '.res'))
    png_file = os.path.join(os.path.dirname(filename), basename + '.png')
    shutil.copyfile(png_file, os.path.join(output_path, basename + '.png'))


def main():
    data_filter = filter_pb2.Filter()
    util.ReadTextProto(FLAGS.filter, data_filter)
    filter_serialized = data_filter.SerializeToString()
    print data_filter

    data_files = util.SafeReadLines(FLAGS.filename)
    print 'Processing %d files' % len(data_files)
    pool = Pool(processes=FLAGS.num_threads)
    for data_file in data_files:
        pool.apply_async(FilterWorker, [filter_serialized, data_file,
                                        FLAGS.output_path])
    pool.close()
    pool.join()


if __name__ == "__main__":    
    main()
