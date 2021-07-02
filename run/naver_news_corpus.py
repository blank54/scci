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

def check_exist(url):
    id = url.split('=')[-1]
    fname_article = 'a-{}.pk'.format(id)
    fpath_article = os.path.join(scci_path.fdir_article, fname_article)
    return os.path.isfile(fpath_article)

def parse_article():
    print('Parse articles:')

    cnt = 0
    duplicates = []
    errors = []
    with tqdm(total=len(os.listdir(scci_path.fdir_url_list))) as pbar:
        for fname_url_list in os.listdir(scci_path.fdir_url_list):
            query_list, _ = fname2query(fname_url_list)

            url_list = read_url_list(fname=fname_url_list)
            for url in url_list:
                pbar.update(1)
                cnt += len(url_list)

                if check_exist(url):
                    duplicates.append(url)
                    continue
                else:
                    try:
                        article = article_parser.parse(url=url)
                        article.extend_query(query_list)
                        save_article(article)
                    except:
                        errors.append(url)

    print('========================================')
    print('  |Initial   : {:,} urls'.format(cnt))
    print('  |Done      : {:,} articles'.format(len(os.listdir(scci_path.fdir_article))))
    print('  |Duplicated: {:,}'.format(len(duplicates)))
    print('  |Error     : {:,}'.format(len(errors)))
    print('========================================')

    if errors:
        print('Errors:')
        for url in errors:
            print(url)
        print('========================================')


if __name__ == '__main__':
    parse_article()