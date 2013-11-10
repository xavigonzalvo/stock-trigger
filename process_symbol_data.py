"""Tool to process information extracted from get_historical_data."""

from multiprocessing import Lock

import flags
import symbol_data_generator

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_weeks", type=int, default=-1,
                         help="Number of weeks to process. Starting from last")
FLAGS = flags.Parse()


def main():
    runner = symbol_data_generator.Runner(Lock())
    runner.Run(FLAGS.filename, FLAGS.num_weeks, FLAGS.output_path)

if __name__ == "__main__":    
    main()
