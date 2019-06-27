#!/usr/bin/env python3
"""
Author : kai
Date   : 2019-06-27
Purpose: Process input tsv data output txt file of all Interpro terms from tsv file


"""

import argparse
import sys
import csv
import os
import re

# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'positional', metavar='str', help='input tsv file')

    # parser.add_argument(
    #     '-a',
    #     '--arg',
    #     help='A named string argument',
    #     metavar='str',
    #     type=str,
    #     default='')
    #
    # parser.add_argument(
    #     '-i',
    #     '--int',
    #     help='A named integer argument',
    #     metavar='int',
    #     type=int,
    #     default=0)
    #
    # parser.add_argument(
    #     '-f', '--flag', help='A boolean flag', action='store_true')

    return parser.parse_args()


# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()
    # str_arg = args.arg
    # int_arg = args.int
    # flag_arg = args.flag
    infile = args.positional

    #doc = ''
    str_list = []
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', fieldnames=['a','b','c','d','e','f','g','h','i','j','k','l','m','n'])
        for row in reader:
            if row["l"] != None:
                #doc += (str(row["l"]) + " ")
                #print(doc)
                str_list.append(row["l"])

    doc = ' '.join(str_list)

    name = os.path.basename(infile)
    name = re.sub(".tsv", ".txt", name)
    path = 'interpro/' + name

    with open(path ,'w') as f:
        print(doc, file=f)


# --------------------------------------------------
if __name__ == '__main__':
    main()
