import flags

flags.FLAGS.add_argument("--verbose",
                         help="increase output verbosity",
                         action="store_true")
flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_weeks", type=int, default=-1,
                         help="Number of weeks. Starting from last")
FLAGS = flags.Parse()


def main():
    print FLAGS.verbose


if __name__ == "__main__":    
    main()
