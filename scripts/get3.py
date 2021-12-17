#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: v0.0.1
@author: James Yang
@email: i@xhlr.top
@blog: https://white-album.top
@software: PyCharm
@project: a
@file: get3.py
@description: 
@license: MIT License
@time: 2021/9/30 21:43
"""
from functools import partial
from multiprocessing import Pool
import os
import sqlite3
import time

from Bio import SeqIO
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"
options = Options()
options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument(f'--user-agent="{headers}"')


def init_db(db_file):
    sql1 = "CREATE TABLE IF NOT EXISTS annotations(gene_caller_id INT PRIMARY KEY," \
           "gene_cluster_id CHARACTER,'Genome name' CHARACTER,'Bin' CHARACTER," \
           "Description TEXT,'Scientific Name' TEXT,'Max Score' TEXT,'Total Score' TEXT," \
           "'Query Cover' TEXT,'E value' TEXT,'Per Ident' TEXT,'Acc Len' TEXT,'Accession' TEXT)"
    sql2 = "CREATE TABLE IF NOT EXISTS submits(gene_caller_id INT PRIMARY KEY,gene_cluster_id CHARACTER," \
           "'Genome name' CHARACTER,'Bin' CHARACTER,Timestamp TIMESTAMP,'Request ID' CHARACTER)"
    sql3 = "CREATE TABLE IF NOT EXISTS fails(gene_caller_id INT PRIMARY KEY,gene_cluster_id CHARACTER," \
           "'Genome name' CHARACTER,'Bin' CHARACTER)"
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    for sql in (sql1, sql2, sql3):
        cursor.execute(sql)
    cursor.close()
    db.close()


def get_rid(record, genome_name, bin_name, db_file):
    gene_cluster_id, gene_caller_id = map(lambda x: x[x.index(':') + 1:], record.id.split(','))
    gene_caller_id = int(gene_caller_id)
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute('select gene_caller_id from annotations')
    if (gene_caller_id,) not in cursor.fetchall():
        print('打开浏览器')
        browser = webdriver.Chrome(
            executable_path="D:/env/pyppeteer/local-chromium/588429/chrome-win32/chromedriver.exe",
            options=options
        )
        browser.set_page_load_timeout(60)
        browser.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastx&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')
        print('键入基因序列')
        print(gene_cluster_id, gene_caller_id)
        browser.find_element_by_id('seq').send_keys(record.seq.upper())
        browser.find_element_by_xpath('//*[@id="blastButton1"]/input').click()
        print('正在刷新页面')
        if browser.find_element_by_id('statInfo'):
            request_id = browser.find_element_by_xpath('//*[@id="statInfo"]/tbody/tr[1]/td[2]/b').text
            if browser.find_element_by_xpath('//*[@id="statInfo"]/tbody/tr[3]/td[1]').text != 'Submitted at':
                time.sleep(3)
            timestamp = browser.find_element_by_xpath('//*[@id="statInfo"]/tbody/tr[3]/td[2]').text
            data = [gene_caller_id, gene_cluster_id, genome_name, bin_name, timestamp, request_id]
            print(data)
            cursor.execute("INSERT INTO submits values(?,?,?,?,?,?)", tuple(data))
            db.commit()
            print('已存入RID')
        else:
            print('没有获得状态表')
        browser.close()
    cursor.close()
    db.close()


def get_func(genome_name, bin_name, db_file):
    db1 = sqlite3.connect(db_file)
    cursor1 = db1.cursor()
    cursor1.execute('select gene_caller_id,gene_cluster_id,"Request ID" from submits')
    for gene_caller_id, gene_cluster_id, request_id in cursor1.fetchall():
        # browser = webdriver.Chrome(
        #     executable_path="D:/env/pyppeteer/local-chromium/588429/chrome-win32/chromedriver.exe",
        #     options=options
        # )
        # browser.set_page_load_timeout(60)
        # browser.get(f'https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID={request_id}')
        # text = browser.page_source
        res = requests.get(f'https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID={request_id}')
        text = res.text

        db2 = sqlite3.connect(db_file)
        cursor2 = db2.cursor()
        cursor2.execute("select gene_caller_id from annotations")
        if (gene_caller_id,) not in cursor2.fetchall():
            soup = BeautifulSoup(text, 'lxml')
            if soup.find('section', {'id': 'noResInfo'}):
                print('没有获得注释信息！')
                db3 = sqlite3.connect(db_file)
                cursor3 = db2.cursor()
                cursor3.execute("INSERT INTO fails values(?,?,?,?)", tuple([
                    gene_caller_id, gene_cluster_id, genome_name, bin_name
                ]))
                db3.commit()
            else:
                description = soup.find('a', {'class': 'deflnDesc'}).text
                sci_name = soup.find('a', {'class': 'sciName'}).text
                max_score = soup.find('td', {'class': 'c6'}).text
                total_score = soup.find('td', {'class': 'c7'}).text
                query_cover = soup.find('td', {'class': 'c8'}).text
                e_val = soup.find('td', {'class': 'c9'}).text
                per_ident = soup.find('td', {'class': 'c10'}).text
                acc_len = soup.find('td', {'class': 'c11'}).text
                accession = soup.find('a', {'class': 'dflSeq'}).text
                data = [
                    gene_caller_id, gene_cluster_id, genome_name, bin_name,
                    description, sci_name, max_score, total_score, query_cover, e_val, per_ident, acc_len, accession
                ]
                print(data)
                print('保存注释信息~')
                cursor2.execute("INSERT INTO annotations values(?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
                db2.commit()
        cursor2.close()
        db2.close()
        # browser.close()
    cursor1.close()
    db1.close()


if __name__ == '__main__':
    fs = [
        './seq/BGM48/Core_Clusters.fasta',
        './seq/BGM48/HC2_Absence.fasta',
        # './seq/DSM20314/Core_Clusters.fasta',
        # './seq/DSM20314/HC2_Absence.fasta',
        # './seq/HC2/Core_Clusters.fasta',
        # './seq/HC2/HC_Unique.fasta',
        # './seq/SLC13/Core_Clusters.fasta',
        # './seq/SLC13/HC2_Absence.fasta',
        # './seq/ZFM222/Core_Clusters.fasta',
        # './seq/ZFM222/HC2_Absence.fasta',
        # './seq/ZFM94/Core_Clusters.fasta',
        # './seq/ZFM94/HC2_Absence.fasta',
    ]
    db_file = 'annotations.db'
    n = 10

    # 初始化数据库
    # init_db(db_file=db_file)

    # 遍历序列文件
    for f in fs:
        genome_name = os.path.dirname(f).split('/')[-1]
        bin_name = os.path.basename(f).replace('.fasta', '')

        # for record in SeqIO.parse(f, 'fasta'):
            # get_rid(record, genome_name=genome_name, bin_name=bin_name, db_file=db_file)

        # function = partial(get_rid, genome_name=genome_name, bin_name=bin_name, db_file=db_file)
        # with Pool(processes=n) as pool:
        #     pool.map(function, [record for record in SeqIO.parse(f, 'fasta')])

        get_func(genome_name=genome_name, bin_name=bin_name, db_file=db_file)
