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
from wordcloud import WordCloud
from collections import Counter, defaultdict

import matplotlib.pyplot as plt

from util import *
scci_path = SCCIPath()

from connlp.preprocess import Normalizer
normalizer = Normalizer()


def data_import():
    flist = os.listdir(scci_path.fdir_article)
    docs = []
    for fname in flist:
        fpath = os.path.join(scci_path.fdir_article, fname)
        with open(fpath, 'rb') as f:
            docs.append(pk.load(f))
    return docs

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

def tokenize_target_docs(fname_tokenizer, fname_stoplist, corp):
    tokenizer = load_tokenizer(fname=fname_tokenizer)

    docs = data_import()
    normalized = [normalizer.normalize(a.content.replace('co.kr', '')) for a in docs if corp in a.query]
    tokenized = [tokenizer.tokenize(doc) for doc in normalized]
    # print(tokenized)

    stoplist = load_stoplist(fname_stoplist)
    stopword_removed = [[w.strip() for w in doc if w not in stoplist] for doc in tokenized]
    return stopword_removed

def export_wordcloud(docs, fname):
    fpath = os.path.join(scci_path.fdir_wordcloud, fname)

    data = ' '.join(itertools.chain(*docs))
    wc = WordCloud(width=400, height=300, background_color='white', font_path='/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf')
    wc.generate(data)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')

    makedir(fpath)
    plt.savefig(fpath, dpi=300)


if __name__ == '__main__':
    fname_tokenizer = 'tokenizer_20210712.pk'
    fname_stoplist = 'stoplist_20210712.txt'
    corporations = ['현대건설', '포스코건설', '대우건설', '대림건설', '현대엔지니어링']
    
    print('========================================')
    print('WordCloud for top corporations')
    for corp in corporations:
        fname_wordcloud = '20210712_{}.png'.format(corp)
        docs = tokenize_target_docs(fname_tokenizer=fname_tokenizer, fname_stoplist=fname_stoplist, corp=corp)
        export_wordcloud(docs=docs, fname=fname_wordcloud)
        print('  | {} -> {}'.format(corp, fname_wordcloud))