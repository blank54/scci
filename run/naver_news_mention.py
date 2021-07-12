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

from util import *
scci_path = SCCIPath()


def count_mentions(flist):
    mentions = defaultdict(int)    
    for fname in flist:
        fpath = os.path.join(scci_path.fdir_article, fname)
        with open(fpath, 'rb') as f:
            article = pk.load(f)

        for keyword in article.query:
            mentions[keyword] += 1
    return mentions

def view_mentions():
    flist = os.listdir(scci_path.fdir_article)
    mentions = count_mentions(flist)

    print('========================================')
    for key, value in sorted(mentions.items(), key=lambda x:x[1], reverse=True):
        print('  | {}: {:,}'.format(key, value))
    print('Total: {:,} articles'.format(len(flist)))
    print('========================================')


if __name__ == '__main__':
    view_mentions()