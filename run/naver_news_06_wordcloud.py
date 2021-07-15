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
from wordcloud import WordCloud
from collections import Counter, defaultdict

import matplotlib.pyplot as plt

from util import *
scci_path = SCCIPath()

from connlp.preprocess import Normalizer, KoreanTokenizer
normalizer = Normalizer()
tokenizer = KoreanTokenizer(pre_trained=True, analyzer='Hannanum')


def data_import(corp):
    flist = os.listdir(scci_path.fdir_article)
    docs = []
    for fname in flist:
        fpath = os.path.join(scci_path.fdir_article, fname)
        with open(fpath, 'rb') as f:
            docs.append(pk.load(f))
    return [a for a in docs if corp in a.query]

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

def preprocess_docs(do_tokenize, fname_stoplist, corp):
    print('========================================')
    print('Tokenize articles')
    docs = data_import(corp=corp)

    fname_tokenized = 'tokenized_corpus_20210715_{}.pk'.format(corp)
    fpath_tokenized = os.path.join(scci_path.fdir_tokenized, fname_tokenized)
    if do_tokenize:
        tokenized = tokenize_docs(docs=docs)
        makedir(fpath_tokenized)
        with open(fpath_tokenized, 'wb') as f:
            pk.dump(tokenized, f)
    else:
        with open(fpath_tokenized, 'rb') as f:
            tokenized = pk.dump(f)

    stoplist = load_stoplist(fname=fname_stoplist)
    stopword_removed = [[w.strip() for w in doc if w not in stoplist] for doc in tokenized]
    return stopword_removed

def export_wordcloud(docs, fname):
    stoplist_apartment = load_stoplist(fname='stoplist_apartment.txt')

    data = ' '.join(itertools.chain(*docs))
    wc = WordCloud(width=400, height=300, background_color='white', font_path='/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf', stopwords=stoplist_apartment)
    wc.generate(data)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')

    fpath = os.path.join(scci_path.fdir_wordcloud, fname)
    makedir(fpath)
    plt.savefig(fpath, dpi=300, bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    do_tokenize = True
    fname_stoplist = 'stoplist_20210715.txt'
    corporations = ['현대건설', '포스코건설', '지에스건설', '대우건설', '대림건설', '에스케이건설']
    
    print('========================================')
    print('WordCloud for top corporations')
    for corp in corporations:
        fname_wordcloud = '20210715_{}.png'.format(corp)
        preprocessed = preprocess_docs(do_tokenize=do_tokenize, fname_stoplist=fname_stoplist, corp=corp)
        export_wordcloud(docs=preprocessed, fname=fname_wordcloud)
        print('  | {} -> {}'.format(corp, fname_wordcloud))