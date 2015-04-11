#!/bin/bash
#
# A tool that extracts multiple symbols.

set -e

readonly csv_dir=`mktemp -d dir.XXXX`
readonly res_dir=`mktemp -d dir.XXXX`
readonly filtered_dir=`mktemp -d dir.XXXX`
readonly filelist=`mktemp list.XXXX`
readonly res_list=`mktemp list.XXXX`

die() { echo "$@" 1>&2 ; exit 1; }

echo "Getting historical data"
./get_historical_data.py --filename config/symbols_test2 \
			 --output_path ${csv_dir} \
			 --num_threads=10

echo "Processing symbols data"
for f in `ls ${csv_dir}/*.csv`; do echo $f; done > ${filelist}
./process_symbols.py --filename ${filelist} \
		     --num_weeks 10 \
		     --output_path ${res_dir} \
		     --num_threads=10

echo "Filter symbols in ${filtered_dir}"
for f in ${res_dir}/*.res; do echo $f >> ${res_list}; done
./filter_symbols.py --filename ${res_list} \
		    --output_path ${filtered_dir} \
		    --filter filters/soft.ascii_proto

echo "OK!"
