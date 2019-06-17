#!/usr/bin/env python3
"""Tool to process information extracted from get_historical_data.

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

from multiprocessing import Lock

import flags
import symbol_data_generator

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_days", type=int, default=30,
                         help="Number of days to process. Starting from last")
flags.FLAGS.add_argument("--window", type=int, default=5,
                         help="Number of days to average over")
flags.FLAGS.add_argument("--iexcloud_token", required=True,
                         help="iexcloud token")
FLAGS = flags.Parse()


def main():
  runner = symbol_data_generator.Runner(
      Lock(), iexcloud_token=FLAGS.iexcloud_token)
  runner.Run(FLAGS.filename, FLAGS.num_days, FLAGS.window, FLAGS.output_path,
             make_graphs=True)


if __name__ == "__main__":
  main()
