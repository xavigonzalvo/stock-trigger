#!/bin/bash

set -e
set -v

for f in $(ls ../protos/*.proto);
do
    protoc --proto_path=../protos --python_out=../protos $f
done
