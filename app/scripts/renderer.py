#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jngt
"""
from bs4 import BeautifulSoup
import requests

def create_home(now):
    """
    link to each active toto page
    now : how many times
    out : html
    """
    toto_type = ['toto', 'minitotoA', 'minitotoB']
    big_type = ['BIG', 'HyakuenBig', 'BIG1000', 'miniBIG']
    big_name = ['BIG', '100円BIG', 'BIG1000', 'miniBIG']
    # toto
    r = requests.get('https://store.toto-dream.com/dcs/subos/screen/pi01/spin000/PGSPIN00001DisptotoLotInfo.form?holdCntId=' + now)
    soup = BeautifulSoup(r.text, "html.parser")
    index = []
    for tt in range(len(toto_type)):
        if soup.find('a', href="#{}".format(toto_type[tt])):
            index.append(tt)
    # BIG
    r = requests.get('https://store.toto-dream.com/dcs/subos/screen/pi02/spin004/PGSPIN00401DispBIGLotInfo.form?holdCntId=' + now)
    soup = BeautifulSoup(r.text, "html.parser")
    for bt in range(len(big_type)):
        if soup.find('a', href="#{}".format(big_type[bt])):
            index.append(len(toto_type) + bt)

    soup = BeautifulSoup('<div></div>', "html.parser")
    kuji_type = toto_type + big_type
    kuji_name = toto_type + big_name
    for i in index:
        link_tag = soup.new_tag('a', href="/{}?id={}".format(kuji_type[i], now))
        link_tag.string = kuji_name[i]
        soup.div.append(link_tag)
    return soup.prettify()

def create_input_form(thtml, flag, now):
    """
    create input form for your prediction
    thtml : table as html
    flag : type of toto
    now : how many times
    out : html
    """
    soup = BeautifulSoup(thtml, "html.parser")
    rows = soup.find_all("tr")
    for i in range(1, len(rows)):
        tds = rows[i].find_all("td")
        pre = tds[5].string
        tds[5].string = ''
        for s in ['1', '0', '2']:
            if s in pre:
                input_tag = soup.new_tag('input', type='checkbox', value=s, checked=True)
            else:
                input_tag = soup.new_tag('input', type='checkbox', value=s)
            input_tag['name'] = 'in' + str(i)
            input_tag.string = s
            tds[5].append(input_tag)

    btag = soup.new_tag('button')
    btag.string = 'SAVE'
    btag['name'] = 'post_value'
    btag['onclick'] = "location.href='/{}?id={}'".format(flag, now)
    btag['value'] = 'SAVE'
    soup.table.wrap(soup.new_tag('form', action= '/{}?id={}'.format(flag, now), method='post'))
    soup.form.append(btag)
    return soup.prettify()

def create_view_form(thtml, flag, n_match, now):
    """
    create view page after save
    flag : type of toto
    n_match : '{}/{}'
    now : how many times
    out : html
    """
    soup = BeautifulSoup(thtml, "html.parser")
    n_match_tag = soup.new_tag('div')
    n_match_tag.string = n_match
    soup.append(n_match_tag)
    btag = soup.new_tag('button')
    btag.string = 'INPUT'
    btag['name'] = 'post_value'
    btag['onclick'] = "location.href='/{}?id={}'".format(flag, now)
    btag['value'] = 'INPUT'
    soup.append(btag)
    soup.button.wrap(soup.new_tag('form', action= '/{}?id={}'.format(flag, now), method='post'))
    return soup.prettify()

def create_button(flag, btype):
    soup = BeautifulSoup('<button></button>', "html.parser")
    soup.button.string = btype
    soup.button['name'] = 'post_value'
    soup.button['onclick'] = "location.href='/{}'".format(flag)
    soup.button['value'] = btype
    soup.button.wrap(soup.new_tag('form', action= '/' + flag, method='post'))
    return soup.prettify()

def table_changer(thtml):
    soup = BeautifulSoup(thtml, "html.parser")
    rows = soup.find_all("tr")
    for i in range(1, len(rows)):
        tds = rows[i].find_all("td")
        input_tag = soup.new_tag('input', type='text', name='in'+str(i), value=tds[5].text)
        tds[5].string.replace_with(input_tag)
    return soup.prettify()

'''
    <a href="/toto">toto</a>
    <a href="/minitotoA">minitotoA</a>
    <a href="/minitotoB">minitotoB</a>
    <a href="/big">BIG</a>
    <a href="/100yenbig">100円BIG</a>
    <a href="/big1000">BIG1000</a>
    <a href="/minibig">miniBIG</a>
'''
