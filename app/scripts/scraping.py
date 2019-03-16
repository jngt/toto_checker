#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jngt
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re, zenhan, json

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys

def get_toto_info(flag, now):
    """
    * get toto info from toto web site
    flag : type of toto
    now : how many times
    out : game info pandas
    """
    toto_type = ['toto', 'minitotoA', 'minitotoB']
    big_type = ['BIG', 'HyakuenBig', 'BIG1000', 'miniBIG']
    with open("app/json/team.json", 'r') as f:
        team_name = json.load(f)
    home_team = []
    away_team = []
    if flag in toto_type:
        n_game = {'toto' : 13, 'minitoto': 5}
        url = 'http://sport-kuji.toto-dream.com/dci/I/IPA/IPA01.do?op=disptotoLotInfo&holdCntId=' + now
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find_all('tr')
        for nr in range(len(rows)):
            tds = rows[nr].find_all('td')
            if tds:
                text = tds[0].get_text().replace(' ', '').replace('\n', '').replace('\r', '')
                segment = re.findall(r'[a-zA-Z]+', text)
                if ''.join(segment) == flag:
                    for i in range(nr+6, nr+6+n_game[segment[0]]):
                        tds = rows[i].find_all('td')
                        home = zenhan.z2h(tds[4].get_text())
                        away = zenhan.z2h(tds[6].get_text())
                        home_team.append(team_name[home] if home in team_name.keys() else home)
                        away_team.append(team_name[away] if away in team_name.keys() else away)
                    break
    elif flag in big_type:
        bignum = {'BIG':'09', 'HyakuenBig':'13', 'BIG1000':'11', 'miniBIG':'10'}
        url = 'http://sport-kuji.toto-dream.com/dci/I/IPA/IPA02.do?op=dispBIGLotAssignGameDetail&popupDispDiv=0&holdCntId=' + now + '&bigLotInfoCommodityId=&commodityId='
        r = requests.get(url + bignum[flag])
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find_all('tr')
        for i in range(5, len(rows)):
            tds = rows[i].find_all('td')
            home = zenhan.z2h(tds[4].get_text())
            away = zenhan.z2h(tds[6].get_text())
            home_team.append(team_name[home] if home in team_name.keys() else home)
            away_team.append(team_name[away] if away in team_name.keys() else away)

    data = {'home' : home_team, 'away' : away_team}
    df = pd.DataFrame(data)
    return df

def get_match_info(toto):
    """
    * get match info from yahoo web site
    toto : game info pandas
    """
    rows = []
    url = 'https://soccer.yahoo.co.jp/jleague/league/'
    r = requests.get(url + 'j1')
    soup = BeautifulSoup(r.text, "html.parser")
    rows += soup.tbody.find_all("tr")
    r = requests.get(url + 'j2')
    soup = BeautifulSoup(r.text, "html.parser")
    rows += soup.tbody.find_all("tr")
    r = requests.get(url + 'j3')
    soup = BeautifulSoup(r.text, "html.parser")
    rows += soup.tbody.find_all("tr")
    r = requests.get(url + 'yn')
    soup = BeautifulSoup(r.text, "html.parser")
    for tbody in soup.find_all("tbody"):
        rows += tbody.find_all("tr")

    score = []
    status = []
    for t in range(len(toto)):
        for row in rows:
            atag = row.find_all("a")
            home = atag[1].get_text()
            if home == toto['home'][t]:
                if atag[4].get_text() == toto['away'][t]:
                    score.append(row.find("td", class_="score").find('a').get_text())
                    status.append(row.find('small', class_="status").get_text())
                    break
    toto["score"] = score
    toto["status"] = status
    result = []
    for t in range(len(toto)):
        if toto["score"][t][0].isnumeric():
            score_h = int(toto["score"][t][0])
            score_a = int(toto["score"][t][-1])
            if score_h > score_a:
                result.append('1')
            elif score_h < score_a:
                result.append('2')
            else:
                result.append('0')
        else:
            result.append('-')
    toto["result"] = result
    return toto

def get_scr_data(flag, now):
    """
    * get scraping result
    """
    toto = get_toto_info(flag, now)
    toto = get_match_info(toto)
    return toto

def cat_pred(toto, pred_list):
    """
    * cat your prediction
    toto : game info pandas
    pred_list : your prediction list
    """
    match_dict = {True : 'O', False : 'X'}
    if not pred_list:
        pred_list = ['_0_' for i in range(len(toto))]
    toto['prediction'] = pred_list
    match = []
    for i in range(len(toto)):
        match.append(toto["result"][i] in toto["prediction"][i].replace('_', ''))
    toto["match"] = match
    n_match = str(toto["match"].sum()) + '/' + str(len(toto["match"]))
    toto["match"] = toto["match"].map(match_dict)
    toto = toto.loc[:, ['home', 'score', 'away', 'status', 'result', 'prediction', 'match']]
    return toto, n_match

if __name__ == '__main__':
    toto, now = get_src_data('miniBIG')
    thtml = toto.to_html(classes='table', index=False)

    '''
    # 今の回を取ってくる
    if False:
        options = ChromeOptions()
        options.add_argument('--headless')
        driver = Chrome(options=options)
        url_index = 'https://www.toto-dream.com/toto/index.html'
        driver.get(url_index)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.tbody.find_all('a')
        next = rows[0].get_text()[1:-1]
        now = str(int(next) - 1)
        driver.close()
        driver.quit()
    elif False:
        now = '1075'
    '''
