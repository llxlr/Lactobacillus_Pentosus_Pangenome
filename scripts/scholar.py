#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
thesis analysis
"""
from bs4 import BeautifulSoup
import requests
import sqlite3
import os
import re

# main_url = 'https://www.x-mol.com/paper/search/q?option='
main_url = 'https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0,5'
# as_sdt=0,5  # 0,5不包含专利2007包含专利，默认不包含专利
# as_vis=0  # 0包含引用1不包含引用，默认包含引用
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/90.0.4430.93'}
proxies = {'http': '127.0.0.1:8889', 'https': '127.0.0.1:8889'}


def get_soup(url):
    response = requests.get(url, headers=headers, proxies=proxies)
    status_code = response.status_code
    # print(status_code)
    if status_code == 200:
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'lxml')
    elif status_code == 429:
        print('访问受限，请降低爬取频率或者更换访问IP！')
        return None
    else:
        return None


def get_num(url, keywords: str):
    soup = get_soup(f'{url}&q={keywords}')
    if soup:
        result = [tag.text for tag in soup.select('div.gs_ab_mdw')][-1]
        result = re.search(r' ([0-9,]+) ', result)
        if result:
            n = int(re.sub(r' |,', '', result.group()))
            if 10 < n < 1000:
                n1, n2 = str(n/10).split('.')
                n = int(n1) + 1 if n2 != '0' else int(n1)
                return list(range(0, n * 10, 10))
            elif n <= 10:
                return [0]
            else:
                return list(range(0, 1000, 10))
        else:
            return None
    else:
        return None


def get_data(url: str, keywords: str, file: str, tablename: str, num=0):
    soup = get_soup(f'{url}&start={num}&q={keywords}')
    items = soup.find_all('div', {'class': 'gs_ri'})

    for item in items:
        t1 = item.select_one('h3>a')
        title, url = t1.text, t1['href']
        t2 = re.split(r'…\xa0- |\xa0- |…- | - ', item.select_one('div.gs_a').text)
        author = t2[0]
        if len(t2) == 3:
            t3 = re.split(r', ', t2[1])
            if len(t3) == 2:
                journal, year = t3
            else:
                journal = year = t3[0]
        else:
            journal = year = 'None'
        abstract = item.select_one('div.gs_rs').text

        db = sqlite3.connect(file)
        cursor = db.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename}("
                       "id INT PRIMARY KEY,"
                       "title TEXT,author TEXT,'year' TEXT,"
                       "journal TEXT,abstract TEXT,url TEXT)")
        cursor.execute(f"SELECT id FROM {tablename}")
        id = len(cursor.fetchall()) + 1
        print(keywords, id)
        try:
            cursor.execute(f"INSERT INTO {tablename} VALUES(?,?,?,?,?,?,?)",
                           (id, title, author, year, journal, abstract, url))
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            cursor.close()
            db.close()


if __name__ == '__main__':
    keywords_list = [
        'CP022130',  # 8
        'CP022131',  # 3

        'CP016491',  # 6
        'CP016492',  # 无
        'CP016493',  # 无
        'CP016494',  # 无
        'CP016495',  # 无
        'CP016496',  # 无

        'CP032654',  # 2
        'CP032655',  # 2
        'CP032656',  # 2
        'CP032657',  # 2
        'CP032658',  # 2
        'CP032659',  # 2
        'CP032660',  # 3
        'CP032661',  # 3
        'CP032662',  # 3

        'CP032757',  # 3
        'CP032758',  # 2

        'lactiplantibacillus pentosus SLC13',  # 1
        'lactiplantibacillus pentosus BGM48',  # 1
        'lactiplantibacillus pentosus ZFM222',  # 1
        'lactiplantibacillus pentosus ZFM94',  # 1
        'lactiplantibacillus pentosus DSM 20314'  # 1
    ]
    for keywords in keywords_list:
        table_name = keywords.replace('.', '_').replace(' ', '_')
        nums = get_num(url=main_url, keywords=keywords)
        if nums:
            for num in nums:
                get_data(url=main_url, keywords=keywords,
                         file=os.path.join(
                            os.path.dirname(__file__),
                            'thesis/raw-thesis.db'
                         ),
                         tablename=table_name,
                         num=num)
        else:
            print(f'{keywords}无搜索结果！')
