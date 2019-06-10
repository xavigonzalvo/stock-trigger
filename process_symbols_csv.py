"""Reads and processes a file of symbols.

The file is downloaded from:

https://www.nasdaq.com/screening/company-list.aspx
"""

import pandas
import csv
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('input_csv', '', 'Input csv with symbols.')
flags.DEFINE_string('output', '', 'Output path to save the symbols.')


def market_cap_fn(x):
  str = x.replace("M", "").replace("$", "").replace("B", "").replace("\"", "")
  return float(str)


def main(argv):
  df = pandas.read_csv(FLAGS.input_csv,
                       quoting=csv.QUOTE_ALL,
                       quotechar='"',
                       engine='python',
                       converters={'MarketCap': market_cap_fn},
                       header=0,
                       names=["Symbol","Name","LastSale","MarketCap","IPOyear","Sector","industry","Summary Quote", ""]
                      )
  good = df["MarketCap"] < 300

  print("Number of symbols:", len(df[good]))
  with open(FLAGS.output, "wt") as f:
    for symbol in df[good]['Symbol']:
      f.write(symbol + "\n")


if __name__ == '__main__':
  app.run(main)
