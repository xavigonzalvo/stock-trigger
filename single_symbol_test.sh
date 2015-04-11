#!/bin/bash
#
# A test where one symbol is processed.

set -e

readonly csv_dir=`mktemp -d dir.XXXX`
readonly res_dir=`mktemp -d dir.XXXX`
readonly filelist=`mktemp -t list`

die() { echo "$@" 1>&2 ; exit 1; }

echo "Getting historical data"
./get_historical_data.py --symbol GOOG \
			 --output_path ${csv_dir} \
			 --overwrite

echo "Processing symbol data"
readonly year=`date +"%Y"`
./process_symbol_data.py --filename ${csv_dir}/GOOG-2010-${year}-week.csv \
			 --output_path ${res_dir} \
			 --num_weeks 8

echo "OK!"
