#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os
import sys
file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.sep.join(file_path.split(os.path.sep)[:-1])
sys.path.append(config_path)

from util import *
scci_path = SCCIPath()

import time
import itertools
import numpy as np
import pickle as pk
from collections import defaultdict
from datetime import datetime, timedelta

from urllib import request
from urllib.parse import quote
from bs4 import BeautifulSoup


class Status:
    def url_list_cnt(self):
        url_list = []
        for fname in os.listdir(scci_path.fdir_url_list):
            fpath_url_list = os.path.join(scci_path.fdir_url_list, fname)
            with open(fpath_url_list, 'rb') as f:
                url_list.extend(pk.load(f))

        url_list = list(set(url_list))

        print('========================================')
        print('  | Total # of urls: {:,}'.format(len(url_list)))
        print('========================================')


class Article:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', '')
        self.id = kwargs.get('id', '')
        self.query = []

        self.title = kwargs.get('title', '')
        self.date = kwargs.get('date', '')
        self.category = kwargs.get('category', '')
        self.content = kwargs.get('content', '')

        self.content_normalized = kwargs.get('content_normalized', '')

    def extend_query(self, query_list):
        queries = self.query
        queries.extend(query_list)
        self.query = list(set(queries))


class QueryParser:
    def build_query_list(self, items):
        _splitted_queries = [queries.split('\n') for queries in items]
        _queries_combs = list(itertools.product(*_splitted_queries))
        query_list = ['+'.join(e) for e in _queries_combs]
        return query_list

    def build_date_list(self, date_start, date_end):
        date_start = datetime.strptime(date_start, '%Y%m%d')
        date_end = datetime.strptime(date_end, '%Y%m%d')
        delta = date_end - date_start

        date_list = []
        for i in range(delta.days+1):
            day = date_start + timedelta(days=i)
            date_list.append(datetime.strftime(day, '%Y%m%d'))
        return date_list

    def load_corporation_names(self, fname):
        fpath_corporation_names = os.path.join(scci_path.fdir_query, fname)
        with open(fpath_corporation_names, 'r', encoding='utf-8') as f:
            data = f.read().strip()

        same_corp = {}
        for line in data.split('\n'):
            try:
                original, synonyms = line.split('  ')
                for synonym in synonyms.split(' '):
                    same_corp[synonym] = original
            except ValueError:
                original = line.strip()

            same_corp[original] = original

        return same_corp


class NewsQuery:
    def __init__(self, query):
        self.query = query

    def __call__(self):
        return quote(self.query.encode('utf-8'))

    def __str__(self):
        return '{}'.format(self.query)

    def __len__(self):
        return len(self.query.split('+'))


class NewsDate:
    def __init__(self, date):
        self.date = date
        self.formatted = self.__convert_date()

    def __call__(self):
        return self.formatted

    def __str__(self):
        return '{}'.format(self.__call__())

    def __convert_date(self):
        try:
            return datetime.strptime(self.date, '%Y%m%d').strftime('%Y.%m.%d')
        except:
            return ''


class NewsCrawler:
    time_lag = np.random.normal(loc=1, scale=0.1)
    headers = {'User-Agent': '''
        [Windows64,Win64][Chrome,58.0.3029.110][KOS] 
        Mozilla/5.0 Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
        Chrome/58.0.3029.110 Safari/537.36
        '''}


class ListScraper(NewsCrawler):
    def __init__(self):
        self.url_base = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=3&ds={}&de={}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from{}to{},a:all&start={}'

    def get_url_list(self, query, date):
        query = NewsQuery(query)
        date = NewsDate(date)

        url_list = []
        start_idx = 1
        while True:
            url_list_page = self.url_base.format(query(), date(), date(), date.date, date.date, start_idx)
            req = request.Request(url=url_list_page, headers=self.headers)
            html = request.urlopen(req).read()
            soup = BeautifulSoup(html, 'lxml')
            time.sleep(self.time_lag)

            url_list.extend([s.get('href') for s in soup.find_all('a', class_='info') if '네이버뉴스' in s])
            start_idx += 10

            if soup.find('div', class_='not_found02'):
                break
            else:
                continue

        return list(set(url_list))


class ArticleParser(NewsCrawler):
    def __init__(self):
        pass

    def parse(self, url):
        req = request.Request(url=url, headers=self.headers)
        html = request.urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml')
        time.sleep(self.time_lag)

        id = str(url.split('=')[-1])
        title = soup.find_all('h3', {'id': 'articleTitle'})[0].get_text().strip()
        date = soup.find_all('span', {'class': 't11'})[0].get_text().split()[0].replace('.', '').strip()
        content = soup.find_all('div', {'id': 'articleBodyContents'})[0].get_text().strip()

        try:
            category = soup.find_all('em', {'class': 'guide_categorization_item'})[0].get_text().strip()
        except IndexError:
            category = None

        article = Article(url=url, id=id, title=title, date=date, category=category, content=content)
        return article