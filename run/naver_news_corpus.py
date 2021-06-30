#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os
import pickle as pk
from tqdm import tqdm

import sys
sys.path.append('/data/blank54/workspace/project/scci/')
from util import *
scci_path = SCCIPath()

from naver import ArticleParser
article_parser = ArticleParser()


def read_url_list(fname):
    fpath = os.path.join(scci_path.fdir_url_list, fname)
    with open(fpath, 'rb') as f:
        url_list = pk.load(f)
    return url_list

def save_article(article):
    fname_article = 'a-{}.pk'.format(article.id)
    fpath_article = os.path.join(scci_path.fdir_article, fname_article)
    makedir(fpath=fpath_article)
    with open(fpath_article, 'wb') as f:
        pk.dump(article, f)


def parse_article():
    with tqdm(total=len(os.listdir(scci_path.fdir_url_list))) as pbar:
        for fname_url_list in os.listdir(scci_path.fdir_url_list):
            query_list, _ = fname2query(fname_url_list)

            url_list = read_url_list(fname=fname_url_list)
            for url in url_list:
                article = article_parser.parse(url=url)
                article.extend_query(query_list)
                save_article(article)

            pbar.update(1)


if __name__ == '__main__':
    print('Parse articles:')
    parse_article()
    print('Done: {:,} articles in the corpus'.format(len(os.listdir(scci_path.fdir_article))))
    print('------------------------------------------------------------')