#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os
import sys
file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.sep.join(file_path.split(os.path.sep)[:-1])
sys.path.append(config_path)

import itertools
import pickle as pk
from tqdm import tqdm
from collections import Counter

from util import *
scci_path = SCCIPath()

from connlp.preprocess import Normalizer, KoreanTokenizer
normalizer = Normalizer()
tokenizer = KoreanTokenizer(pre_trained=True, analyzer='Hannanum')


def data_import():
    flist = os.listdir(scci_path.fdir_article)
    docs = []
    for fname in flist:
        fpath = os.path.join(scci_path.fdir_article, fname)
        with open(fpath, 'rb') as f:
            docs.append(pk.load(f))
    return docs

def tokenize_docs(docs):
    normalized = [normalizer.normalize(a.content) for a in docs]

    tokenized = []
    with tqdm(total=len(normalized)) as pbar:
        for doc in normalized:
            tokenized.append(tokenizer.extract_noun(doc))
            pbar.update(1)
    return tokenized

def load_stoplist(fname):
    fpath = os.path.join(scci_path.fdir_stoplist, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        stoplist = list(set([w.strip() for w in f.read().strip().split('\n')]))

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(stoplist))

    return stoplist

def count_words(docs, fname_tokenized, do_tokenize, fname_stoplist):
    print('========================================')
    print('Tokenize articles')
    fpath_tokenized = os.path.join(scci_path.fdir_tokenized, fname_tokenized)
    if do_tokenize:
        tokenized = tokenize_docs(docs)
        makedir(fpath_tokenized)
        with open(fpath_tokenized, 'wb') as f:
            pk.dump(tokenized, f)
    else:
        with open(fpath_tokenized, 'rb') as f:
            tokenized = pk.dump(f)

    print('========================================')
    print('Stopword removal')
    stoplist = load_stoplist(fname_stoplist)
    stopword_removed = []
    with tqdm(total=len(tokenized)) as pbar:
        for doc in tokenized:
            stopword_removed.append([w.strip() for w in doc if w not in stoplist])
            pbar.update(1)

    counter_before = Counter(itertools.chain(*tokenized))
    counter_after = Counter(itertools.chain(*stopword_removed))
    return counter_before, counter_after

def update_stoplist(counter_before, counter_after, topn):
    words_before = [w for w, c in sorted(counter_before.items(), key=lambda x:x[1], reverse=True)]
    words_after = [w for w, c in sorted(counter_after.items(), key=lambda x:x[1], reverse=True)]

    print('========================================')
    for idx, word in enumerate(words_before[:topn]):
        if word in words_after:
            print('  | [{:3,}] BEFORE: {} -> AFTER: {}({:,})'.format((idx+1), word, word, counter_after[word]))
        else:
            print('  | [{:3,}] BEFORE: {}({:,}) -> '.format((idx+1), word, counter_before[word]))
    print('========================================')

if __name__ == '__main__':
    ## Data import
    docs = data_import()
    
    ## Update stopword list
    fname_tokenized = 'tokenized_corpus_20210715.pk'
    fname_stoplist = 'stoplist_20210715.txt'
    do_tokenize = True
    counter_before, counter_after = count_words(docs=docs, fname_tokenized=fname_tokenized, do_tokenize=do_tokenize, fname_stoplist=fname_stoplist)

    topn = 300
    update_stoplist(counter_before=counter_before, counter_after=counter_after, topn=topn)