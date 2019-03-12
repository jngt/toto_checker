#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jngt
"""
from bs4 import BeautifulSoup
import pickle, os

def create_pred_list(data):
    """
    create prediction list from input
    data : request.form
    out : prediction list
    """
    pred_list = []
    for i in range(1, len(data)):
        pred = ''
        for s in ['1', '0', '2']:
            pred += s if s in data.getlist('in' + str(i)) else '_'
        pred_list.append(pred)
    return pred_list

def save_list(pred_list, flag, now):
    """
    save prediction by pickle
    """
    filepath = os.path.join('app', 'savedata', now + flag + '.txt')
    with open(filepath, 'wb') as f:
        pickle.dump(pred_list, f)

def load_list(flag, now):
    """
    load prediction by pickle
    """
    filepath = os.path.join('app', 'savedata', now + flag + '.txt')
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            pred_list = pickle.load(f)
    else:
        pred_list = []
    return pred_list
