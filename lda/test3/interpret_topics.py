#!/usr/bin/env python3
"""
Author : kai
Date   : 2019-06-26
Purpose: Rock the Casbah
"""

import argparse
import sys
import re
import csv

# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # parser.add_argument(
    #     'positional', metavar='str', help='A positional argument')

    parser.add_argument(
        '-a',
        '--arg',
        help='A named string argument',
        metavar='str',
        type=str,
        default='')

    parser.add_argument(
        '-i',
        '--int',
        help='A named integer argument',
        metavar='int',
        type=int,
        default=0)

    parser.add_argument(
        '-f', '--flag', help='A boolean flag', action='store_true')

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
    str_arg = args.arg
    int_arg = args.int
    flag_arg = args.flag
    #pos_arg = args.positional

    #read and open the annotations file
    intpro_dict = {}
    with open('InterPro_entry_list.tsv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            intpro_dict[row['ENTRY_AC']] = row['ENTRY_NAME']

    with open('model_topics.txt', 'r') as file:
        model_topics = file.read().replace('\n', '')

    model_topics = re.sub("'", "", model_topics)
    model_topics = re.sub("\[", "", model_topics)
    model_topics = re.sub("\]", "", model_topics)

    mtl = model_topics.split('), ')

    with open('output_topics.tsv' ,'w') as f:
        print('Topic\tModel_coefficient\tInterpro_ID\tInterPro_ENTRY_NAME', file=f)
        for list in mtl:
            topic = list[1]
            split_list = list.split()
            id_re = re.compile('IPR\d{3}')
            c_words = []
            for w in split_list:
                match = id_re.search(w)
                if match:
                    c_words.append(w)
            c_words = [re.sub('"', '', i) for i in c_words]
            for w in c_words:
                re.sub('\)', '', w)
                coef, intpro = w.split('*')
                intpro = intpro[:9]

                if intpro in intpro_dict.keys():
                    label = intpro_dict[intpro]
                else:
                    label = ''

                print('{}\t{}\t{}\t{}'.format(topic,coef,intpro,label), file=f)


# --------------------------------------------------
if __name__ == '__main__':
    main()
