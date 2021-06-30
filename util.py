#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os


class SCCIPath:
    root = '/data/blank54/workspace/project/scci/'

    fdir_data = os.path.join(root, 'data/')

    fdir_query = os.path.join(fdir_data, 'naver_news/query/')
    fdir_url_list = os.path.join(fdir_data, 'naver_news/url_list/')


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