#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os
import itertools
import pickle as pk
from tqdm import tqdm

import sys
sys.path.append('/data/blank54/workspace/project/scci/')
from util import *
scci_path = SCCIPath()

from naver import QueryParser, ListScraper, Status
query_parser = QueryParser()
list_scraper = ListScraper()
status = Status()


def parse_query(query_file):
    date_start, date_end = query_file[0].split('\n')
    date_list = query_parser.build_date_list(date_start, date_end)
    query_list = query_parser.build_query_list(query_file[1:])
    return date_list, query_list

def save_url_list(query, date, url_list):
    fname_url_list = 'Q-{}_D-{}.pk'.format(query, date)
    fpath_url_list = os.path.join(scci_path.fdir_url_list, fname_url_list)
    makedir(fpath=fpath_url_list)
    with open(fpath_url_list, 'wb') as f:
        pk.dump(url_list, f)

def scrape_url_list(fname_query_list):
    fpath_query = os.path.join(scci_path.fdir_query, fname_query_list)
    with open(fpath_query, 'r', encoding='utf-8') as f:
        query_file = f.read().split('\n\n')
        date_list, query_list = parse_query(query_file)
    
    for date in sorted(date_list, reverse=False):
        cnt = 0

        print('Start: {}'.format(date))
        with tqdm(total=len(query_list)) as pbar:
            for query in query_list:
                url_list = list_scraper.get_url_list(query=query, date=date)
                save_url_list(query, date, url_list)
                cnt += len(url_list)
                pbar.update(1)

        print('Done : {} ({:,} articles)'.format(date, cnt))
        print('------------------------------------------------------------')


if __name__ == '__main__':
    fname_query_list = 'query_20210701.txt'
    scrape_url_list(fname_query_list)
    status.url_list_cnt()