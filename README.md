Trading tools
=============

Build
-----

Install python and protocol buffers (more information on protocol
buffers can be found here https://github.com/google/protobuf).

Build protocol buffers for this project:

    $ cd build
    $ ./update_protos.sh

Get some historical data
------------------------ 

* From a list of stocks:

        $ mkdir -p data/csv
        $ ./get_historical_data.py --filename config/symbols_little --output_path data/csv --num_threads=10

* A single symbol:

        $ ./get_historical_data.py --symbol GOOG --output_path data/csv --overwrite


Generating data to get polynomial models
----------------------------------------

a) Multiple symbols in parallel:

   for f in `ls data/*.csv`; do echo $f; done > /tmp/list
   python process_symbols.py --filename /tmp/list --num_weeks 10 --output_path data/res/ --num_threads=10
   
b) One symbol:

   python process_symbol_data.py --filename data/CAM.L-2010-2013-week.csv --output_path data/res --num_weeks 8



Filtering symbols
-----------------

In order to filter information of a set of stock symbols, you can do
it locally too:

    $ for f in data/res/*.res; do echo $f >> /tmp/res_list; done
    $ python filter_symbols.py --filename /tmp/res_list --output_path data/filtered/ --filter filters/soft.ascii_proto

You can see the mean:

    $ grep mean: data_days/filtered_medium/*.res | sort -k 2
