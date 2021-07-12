#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os


class SCCIPath:
    root = '/data/blank54/workspace/project/scci/'

    fdir_data = os.path.join(root, 'data/')
    fdir_corpus = os.path.join(root, 'corpus/')
    fdir_model = os.path.join(root, 'model/')
    fdir_result = os.path.join(root, 'result/')

    fdir_query = os.path.join(fdir_data, 'naver_news/query/')
    fdir_url_list = os.path.join(fdir_data, 'naver_news/url_list/')
    fdir_article = os.path.join(fdir_corpus, 'naver_news/')

    fdir_tokenizer = os.path.join(fdir_model, 'tokenizer/')
    fdir_stoplist = os.path.join(fdir_model, 'stoplist/')

    fdir_wordcloud = os.path.join(fdir_result, 'wordcloud/')


def makedir(fpath):
    '''
    A method to make directory for the given file path.

    Attributes
    ----------
    fpath : str
        | A file path.
    '''

    if fpath.endswith('/'):
        os.makedirs(fpath, exist_ok=True)
    else:
        os.makedirs('/'.join(fpath.split('/')[:-1]), exist_ok=True)


def fname2query(fname):
    Q, D = fname.replace('.pk', '').split('_')
    query_list = Q.split('-')[1].split('+')
    date = D.split('-')[1]
    return query_list, date