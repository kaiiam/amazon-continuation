#!/bin/bash

# read input file ($1) line by line and wget the line
while IFS= read -r line; do
    wget $line
done < "$1"

# unzip all gz files in directory
for x in *.tsv.gz; do gunzip $x ; done
