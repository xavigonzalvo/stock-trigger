#!/bin/bash

set -e
set -v

for f in $(ls *.proto);
do
    protoc --python_out=./ $f
done
