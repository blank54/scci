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

from naver import QueryParser
query_parser = QueryParser()

from util import *
scci_path = SCCIPath()

from run.naver_news_01_crawling import parse_query


def query_history():
    history = defaultdict(list)

    for fname in sorted(os.listdir(scci_path.fdir_query)):
        if not fname.startswith('query_'):
            continue

        collected_date = fname.replace('.txt', '').split('_')[1]
        fpath = os.path.join(scci_path.fdir_query, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            query_file = f.read().split('\n\n')
            date_list, query_list = parse_query(query_file)

        history['collected_date'].append(collected_date)
        history['date_start'].append(date_list[0])
        history['date_end'].append(date_list[-1])
        history['num_query'].append(len(query_list))
        history['query'].append(', '.join(query_list))

    history_df = pd.DataFrame(history)

    print('==================================================')
    print('Query History')
    print('  | {:>13} {:>10} {:>10} {:>12} {:>15}'.format('CollectedDate', 'DateStart', 'DateEnd', 'NumOfQuery', 'Query'))
    for i in range(len(history_df)):
        collected_date = history_df.iloc[i]['collected_date']
        date_start = history_df.iloc[i]['date_start']
        date_end = history_df.iloc[i]['date_end']
        num_query = history_df.iloc[i]['num_query']
        query = history_df.iloc[i]['query']
        print('  | {:>13} {:>10} {:>10} {:>12} {:>12}, ...'.format(collected_date, date_start, date_end, num_query, query[:10]))


def corporation_names():
    fname_corporation_names = 'corporation_names.txt'
    same_corp = query_parser.load_corporation_names(fname=fname_corporation_names)

    corporation_names = defaultdict(list)
    for corp in same_corp:
        corporation_names[same_corp[corp]].append(corp)

    print('==================================================')
    print('Considered the following names as the same corporation')
    for original, synonyms in corporation_names.items():
        print('  | {} -> {}'.format(original, ', '.join(synonyms)))



def naver_news_status():
    flist = os.listdir(scci_path.fdir_article)

    print('==================================================')
    print('Naver News Status')
    print('  | Total: {:,}'.format(len(flist)))


if __name__ == '__main__':
    query_history()
    corporation_names()
    naver_news_status()