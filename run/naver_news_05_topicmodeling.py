#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os
import sys
file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.sep.join(file_path.split(os.path.sep)[:-1])
sys.path.append(config_path)

import pickle as pk
import pyLDAvis
import pyLDAvis.gensim

from util import *
scci_path = SCCIPath()

from connlp.analysis import TopicModel
from connlp.preprocess import Normalizer

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

def data_preparation(docs):
    normalizer = Normalizer()

    fname_tokenizer = 'tokenizer_20210712.pk'
    tokenizer = load_tokenizer(fname=fname_tokenizer)
    
    docs_for_lda = {}
    for article in docs:
        normalized = normalizer.normalize(article.content)
        tokenized = tokenizer.tokenize(normalized)
        docs_for_lda[article.id] = tokenized

    return docs_for_lda

def lda_model_development(docs, lda_parameters, num_topics):
    docs_for_lda = data_preparation(docs=docs)

    lda_model = TopicModel(docs=docs_for_lda, num_topics=num_topics)
    lda_model.learn(parameters=lda_parameters)
    lda_model.assign()
    return lda_model

def get_lda_model(fname, do_train):
    fpath_lda_model = os.path.join(scci_path.fdir_lda, fname)

    if do_train:
        global docs, lda_parameters, num_topics

        lda_model = lda_model_development(docs=docs, lda_parameters=lda_parameters, num_topics=num_topics)
        makedir(fpath=fpath_lda_model)
        with open(fpath_lda_model, 'wb') as f:
            pk.dump(lda_model, f)
    else:
        with open(fpath_lda_model, 'rb') as f:
            lda_model = pk.load(f)

    return lda_model


if __name__ == '__main__':
    ## LDA Parameters
    num_topics = 10
    lda_parameters = {
        'iterations': 100,
        'alpha': 0.7,
        'eta': 0.05,
    }
    fname_lda_model = 'lda_model_20210714_N-{}_E-{}.pk'.format(num_topics, lda_parameters['iterations'])

    ## Model Development
    docs = data_import()
    lda_model = get_lda_model(fname=fname_lda_model, do_train=False)

    ## Evaluation
    print(lda_model.coherence)

    ## Visualization
    vis = pyLDAvis.gensim.prepare(lda_model.model, lda_model.docs_for_lda, lda_model.id2word)
    pyLDAvis.save_html(vis, 'pyldavis_test.html')