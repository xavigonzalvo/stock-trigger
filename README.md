# Trading tools

[![Build Status](https://travis-ci.org/xavigonzalvo/stock-trigger.svg)](https://travis-ci.org/xavigonzalvo/stock-trigger)

Trading tools refer to utilities that can be used to process stock
symbols. Stocks in any market are charaterized by a symbol (ie. name)
and some historical data. The following tools take historical data and
builds a simple regression model to find interesting companies in the
market.

There are two parts in this repository. One the one hand, scripts to
run locally and process historical data of stock symbols. On the other
hand, an AppEngine frontend to run this functionality automatically.

## Build

Install python and protocol buffers (more information on protocol
buffers can be found here https://github.com/google/protobuf).

Build protocol buffers for this project:

    $ cd build
    $ ./update_protos.sh

## Local tools

### Get some historical data

* From a list of stocks:

        $ mkdir -p data/csv
        $ ./get_historical_data.py --filename config/symbols_little --output_path data/csv --num_threads=10

* A single symbol:

        $ mkdir -p data/csv
        $ ./get_historical_data.py --symbol GOOG --output_path data/csv --overwrite


### Generating data to get polynomial models

* Multiple symbols in parallel:

        $ mkdir data/res
        $ for f in `ls data/csv/*.csv`; do echo $f; done > /tmp/list
        $ ./process_symbols.py --filename /tmp/list --num_weeks 10 --output_path data/res/ --num_threads=10
   
* One symbol:

        $ mkdir data/res
        $ ./process_symbol_data.py --filename data/csv/CINE.L-2010-2015-week.csv --output_path data/res --num_weeks 8


### Filtering symbols

In order to filter information of a set of stock symbols, you can do
it locally too:

    $ mkdir data/filtered
    $ for f in data/res/*.res; do echo $f >> /tmp/res_list; done
    $ ./filter_symbols.py --filename /tmp/res_list --output_path data/filtered/ --filter filters/soft.ascii_proto

You can look at the mean percentage changes over the number of weeks
each symbol has been processed for:

    $  grep mean: data/filtered/*.res | sort -k 2

## AppEngine

An AppEngine frontend can be found in the `gae/` folder. First of all,
please install the python tools from
https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python.

You can start the server by doing the following:

    $ cd gae
    $ ./start_server.sh

Then you can visit http://localhost:8080 for testing locally.

You can have a look at a running instance of this AppEngine here:

http://deep-trading.appspot.com/

Note that this will only let you look at the previous reports.

TODO:

- Review data structure to minimize reads and writes.
- Have the list of symbols in the database to keep track of unknown symbols.
