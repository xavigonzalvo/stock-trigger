import yahoo_finance_fetcher
import flags

flags.FLAGS.add_argument("--verbose",
                         help="increase output verbosity",
                         action="store_true")
FLAGS = flags.Parse()


def main():
    print FLAGS.verbose


if __name__ == "__main__":    
    main()
