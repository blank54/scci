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
from collections import Counter

from util import *
scci_path = SCCIPath()

from connlp.preprocess import Normalizer, KoreanTokenizer
normalizer = Normalizer()


def data_import():
    flist = os.listdir(scci_path.fdir_article)
    docs = []
    for fname in flist:
        fpath = os.path.join(scci_path.fdir_article, fname)
        with open(fpath, 'rb') as f:
            docs.append(pk.load(f))
    return docs

def normalize_docs(docs):
    return [normalizer.normalize(a.content) for a in docs]

def train_tokenizer(docs, fname):
    normalized = normalize_docs(docs)

    tokenizer = KoreanTokenizer(min_frequency=0)
    tokenizer.train(text=normalized)

    fpath = os.path.join(scci_path.fdir_tokenizer, fname)
    makedir(fpath=fpath)
    with open(fpath, 'wb') as f:
        pk.dump(tokenizer, f)

def load_tokenizer(fname):
    fpath = os.path.join(scci_path.fdir_tokenizer, fname)
    with open(fpath, 'rb') as f:
        tokenizer = pk.load(f)
    return tokenizer

def load_stoplist(fname):
    fpath = os.path.join(scci_path.fdir_stoplist, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        stoplist = list(set([w.strip() for w in f.read().strip().split('\n')]))

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(stoplist))

    return stoplist

def count_words(docs, fname_tokenizer, fname_stoplist):
    normalized = normalize_docs(docs)

    tokenizer = load_tokenizer(fname=fname_tokenizer)
    tokenized = [tokenizer.tokenize(doc) for doc in normalized]

    stoplist = load_stoplist(fname_stoplist)
    stopword_removed = [[w.strip() for w in doc if w not in stoplist] for doc in tokenized]

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
    
    ## Train tokenizer
    fname_tokenizer = 'tokenizer_20210712.pk'
    train_tokenizer(docs=docs, fname=fname_tokenizer)

    ## Update stopword list
    fname_stoplist = 'stoplist_20210712.txt'
    counter_before, counter_after = count_words(docs=docs, fname_tokenizer=fname_tokenizer, fname_stoplist=fname_stoplist)

    topn = 300
    update_stoplist(counter_before=counter_before, counter_after=counter_after, topn=topn)