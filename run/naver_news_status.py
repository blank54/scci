#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os
import sys
file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.sep.join(file_path.split(os.path.sep)[:-1])
sys.path.append(config_path)

import pandas as pd
from collections import defaultdict

from util import *
scci_path = SCCIPath()

from run.naver_news_crawling import parse_query


def query_history():
    history = defaultdict(list)

    for fname in os.listdir(scci_path.fdir_query):
        fpath = os.path.join(scci_path.fdir_query, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            query_file = f.read().split('\n\n')
            date_list, query_list = parse_query(query_file)

        history['date_start'].append(date_list[0])
        history['date_end'].append(date_list[-1])
        history['num_query'].append(len(query_list))
        history['query'].append(', '.join(query_list))

    return pd.DataFrame(history)


def naver_news_status():
    flist = os.listdir(scci_path.fdir_article)

    print('==================================================')
    print('Naver News Status')
    print('  | Total: {:,}'.format(len(flist)))


if __name__ == '__main__':
    history = query_history()
    print(history)

    naver_news_status()