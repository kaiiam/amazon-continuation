#!/usr/bin/env python3
"""
Author : kai
Date   : 2019-06-25
Purpose: Test LDA using the script based on this https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/
Using the MGNIFY Interpro annotations from the Amazon Continuum Metagenomes study: https://www.ebi.ac.uk/metagenomics/studies/MGYS00000382

./test_lda.py --m_start 2 --m_limit 40 --m_step 5 --model_list_indx 4 --num_words 20 --num_topic 20

"""

import argparse
import sys
import re
import csv
import numpy as np
import pandas as pd
from pprint import pprint

# ingest data
import glob
import os

#Cleaning and Preprocessing
from nltk.corpus import stopwords
import nltk
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
import string

# Importing Gensim
import gensim
from gensim import corpora, models
from gensim.models import CoherenceModel

#Plotting
import matplotlib.pyplot as plt


# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

#Mallet
mallet_path = '/Users/kai/scripts/mallet-2.0.8/bin/mallet' # update this path

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
        '-s',
        '--m_start',
        help='number of topics to start iterating over',
        metavar='int',
        type=int,
        default=2)
    parser.add_argument(
        '-l',
        '--m_limit',
        help='number of topics to limit iterating over',
        metavar='int',
        type=int,
        default=3)
    parser.add_argument(
        '-p',
        '--m_step',
        help='step when iterating over number of topics',
        metavar='int',
        type=int,
        default=1)

    parser.add_argument(
        '-o',
        '--model_list_indx',
        help='index into model_list giving optimal number of topics',
        metavar='int',
        type=int,
        default=0)

    parser.add_argument(
        '-w',
        '--num_words',
        help='number of words to print per topic',
        metavar='int',
        type=int,
        default=10)
    parser.add_argument(
        '-t',
        '--num_topic',
        help='number of topics in model',
        metavar='int',
        type=int,
        default=10)

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
def compute_coherence_values(dictionary, corpus, texts, limit, start, step):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


# --------------------------------------------------
def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    #contents = pd.Series(texts)
    #sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()
    str_arg = args.arg
    flag_arg = args.flag
    #pos_arg = args.positional
    num_topic = args.num_topic
    num_words = args.num_words
    m_start = args.m_start
    m_limit = args.m_limit
    m_step = args.m_step
    model_list_indx = args.model_list_indx


    # #read in csv
    # #read and open the annotations file
    # doc1 = ''
    # with open("data/SRR1182511_MERGED_FASTQ_InterPro.tsv") as csvfile:
    #     reader = csv.DictReader(csvfile, delimiter='\t', fieldnames=['a','b','c','d','e','f','g','h','i','j','k','l','m','n'])
    #     for row in reader:
    #         if row["l"] != None:
    #             doc1 += (str(row["l"]) + " ")
    #
    #
    # doc2 = ''
    # with open("data/SRR1182512_MERGED_FASTQ_InterPro.tsv") as csvfile:
    #     reader = csv.DictReader(csvfile, delimiter='\t', fieldnames=['a','b','c','d','e','f','g','h','i','j','k','l','m','n'])
    #     for row in reader:
    #         if row["l"] != None:
    #             doc2 += (str(row["l"]) + " ")
    #
    # # # compile documents
    # # doc_complete = [doc1, doc2, doc3, doc4, doc5]
    # doc_complete = [doc1, doc2]


    # compile documents
    doc_complete = []

    # #Read in all *.tsv files in /data
    # pwd = os.getcwd()
    # path = pwd + '/data'
    # for filename in glob.glob(os.path.join(path, '*.tsv')):
    #     #doc = ''
    #     str_list = []
    #     with open(filename) as csvfile:
    #         reader = csv.DictReader(csvfile, delimiter='\t', fieldnames=['a','b','c','d','e','f','g','h','i','j','k','l','m','n'])
    #         for row in reader:
    #             if row["l"] != None:
    #                 str_list.append(row["l"])
    #
    #     doc = ' '.join(str_list)
    #     doc_complete.append(doc)


    # Read in all *.tsv files in /interpro
    pwd = os.getcwd()
    #path = pwd + '/temp'
    path = pwd + '/interpro'
    for filename in glob.glob(os.path.join(path, '*.txt')):
        #str_list = []
        with open(filename, 'r') as file:
            doc = file.read()#.replace('\n', '')

        doc_complete.append(doc)

    ## For GENES files
    doc_clean = [doc.split() for doc in doc_complete]

    id2word = corpora.Dictionary(doc_clean)

    #id2word.filter_extremes(no_below=15) #, keep_n=100000 , no_above=0.5
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    corpus = [id2word.doc2bow(doc) for doc in doc_clean]


    # Compute LDA using mallet
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topic, id2word=id2word)

    # Show Topics
    pprint(ldamallet.show_topics(formatted=False))

    model_topics = ldamallet.show_topics(formatted=False)
    model_topics_out = open('model_topics.txt','w')
    pprint(ldamallet.print_topics(num_words=num_words), model_topics_out)


    # Compute Coherence Score
    coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=doc_clean, dictionary=id2word, coherence='c_v')
    coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    print('\nCoherence Score: ', coherence_ldamallet)




    # ## find the optimal number of topics for LDA
    # model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=doc_clean, start=m_start, limit=m_limit, step=m_step)
    #
    # # Show graph
    # limit=m_limit; start=m_start; step=m_step;
    # x = range(start, limit, step)
    # plt.plot(x, coherence_values)
    # plt.xlabel("Num Topics")
    # plt.ylabel("Coherence score")
    # plt.legend(("coherence_values"), loc='best')
    # #plt.show()
    # plt.savefig('coherence_values.png')
    #

    # with open('topic_numbers_and_coherence_values.txt' ,'w') as f:
    #     for m, cv in zip(x, coherence_values):
    #         print("Num Topics =", m, " has Coherence Value of", round(cv, 4), file=f )
    #

    with open('topic_numbers_and_coherence_values.txt' ,'a') as f:
        print('Num Topics ={} has Coherence Value of {}'.format(num_topic, coherence_ldamallet), file=f)


    # optimal_model = model_list[model_list_indx]
    # model_topics = optimal_model.show_topics(formatted=False)
    # model_topics_out = open('model_topics.txt','w')
    # pprint(optimal_model.print_topics(num_words=num_words), model_topics_out)
    #
    # #Finding the dominant topic in each sentence
    # df_topic_sents_keywords = format_topics_sentences(ldamodel=optimal_model, corpus=corpus, texts=doc_clean)
    #
    # # Format
    # df_dominant_topic = df_topic_sents_keywords.reset_index()
    # df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords'] #, 'Text'
    #
    # # Show
    # #pprint(df_dominant_topic.head(10))
    # df_dominant_topic.to_csv('dominant_topics.tsv', sep='\t', encoding='utf-8')
    #
    #
    # ## Find the most representative document for each topic
    # # Group top 5 sentences under each topic
    # sent_topics_sorteddf_mallet = pd.DataFrame()
    #
    # sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')
    #
    # for i, grp in sent_topics_outdf_grpd:
    #     sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet,
    #                                              grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)], axis=0)
    #
    # # Reset Index
    # sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)
    #
    # # Format
    # sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords"] #, "Text"
    #
    # # Show
    # #pprint(sent_topics_sorteddf_mallet.head()) # not really different from df_dominant_topic
    # sent_topics_sorteddf_mallet.to_csv('sent_topics_sorted_df_mallet.tsv', sep='\t', encoding='utf-8')
    #
    # # Topic distribution across documents
    # # Number of Documents for Each Topic
    # topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts()
    #
    # # Percentage of Documents for Each Topic
    # topic_contribution = round(topic_counts/topic_counts.sum(), 4)
    #
    # # Topic Number and Keywords
    # topic_num_keywords = df_topic_sents_keywords[['Dominant_Topic', 'Topic_Keywords']]
    #
    # # Concatenate Column wise
    # df_dominant_topics = pd.concat([topic_num_keywords, topic_counts, topic_contribution], axis=1)
    #
    # # Change Column names
    # df_dominant_topics.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents']
    #
    # # Show
    # #pprint(df_dominant_topics)
    # df_dominant_topics.to_csv('documents_per_topic.tsv', sep='\t', encoding='utf-8')



# --------------------------------------------------
if __name__ == '__main__':
    main()
