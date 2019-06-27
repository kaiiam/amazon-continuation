#!/bin/bash

for x in data/*.tsv; do ./process_data.py $x ; done
