Trading tools
=============

Install
-------

Update protocol buffers (more information on protocol buffers can be
found here https://github.com/google/protobuf).

  ```
  $ cd build
  $ ./update_protos.sh
  ```

Get some historical data
------------------------ 

a) A list of symbols:

   python get_historical_data.py --filename config/symbols --output_path data/csv --num_threads=10

b) A single symbol:

   python get_historical_data.py --symbol GOOG --output_path data/csv --overwrite


Generating data to get polynomial models
----------------------------------------

a) Multiple symbols in parallel:

   for f in `ls data/*.csv`; do echo $f; done > /tmp/list
   python process_symbols.py --filename /tmp/list --num_weeks 10 --output_path data/res/ --num_threads=10
   
b) One symbol:

   python process_symbol_data.py --filename data/CAM.L-2010-2013-week.csv --output_path data/res --num_weeks 8



Filtering symbols
-----------------

for f in data/res/*.res; do echo $f >> /tmp/res_list; done
python filter_symbols.py --filename /tmp/res_list --output_path data/filtered/ --filter filters/soft.ascii_proto

grep mean: data_days/filtered_medium/*.res | sort -k 2
