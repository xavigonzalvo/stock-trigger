import flags
import yahoo_finance_fetcher as yahoo

flags.FLAGS.add_argument("--verbose",
                         help="increase output verbosity",
                         action="store_true")
flags.FLAGS.add_argument("--output", required=True,
                         help="Output file")

FLAGS = flags.Parse()


def main():
    fetcher = yahoo.YahooFinanceFetcher()
    symbols = fetcher.GetAllSymbols()
    print '%d symbols' % len(symbols)
    with open(FLAGS.output, 'wt') as f:
        for symbol in symbols:
            f.write('%s\n' % symbol)


if __name__ == "__main__":    
    main()
