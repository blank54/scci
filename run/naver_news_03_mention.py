#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os
import sys
file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.sep.join(file_path.split(os.path.sep)[:-1])
sys.path.append(config_path)

import pickle as pk
from collections import defaultdict

from naver import QueryParser
query_parser = QueryParser()

from util import *
scci_path = SCCIPath()


def count_mentions(flist):
    fname_corporation_names = 'corporation_names.txt'
    same_corp = query_parser.load_corporation_names(fname=fname_corporation_names)

    mentions = defaultdict(list)    
    for fname_article in flist:
        fpath_article = os.path.join(scci_path.fdir_article, fname_article)
        with open(fpath_article, 'rb') as f:
            article = pk.load(f)

        for keyword in article.query:
            try:
                corp_name = same_corp[keyword]
                mentions[corp_name].append(article.id)
            except:
                continue

    return {corp_name: len(set(article_id_list)) for corp_name, article_id_list in mentions.items()}

def view_mentions():
    flist = os.listdir(scci_path.fdir_article)
    mentions = count_mentions(flist)

    print('========================================')
    for idx, (key, value) in enumerate(sorted(mentions.items(), key=lambda x:x[1], reverse=True)):
        print('  | [{:2,}] {}: {:,} ({:.02f}%)'.format((idx+1), key, value, (value/len(flist)*100)))
    print('Total: {:,} articles'.format(len(flist)))
    print('========================================')


if __name__ == '__main__':
    view_mentions()