#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from multiprocessing import Pool
import sqlite3
import time
import glob
import os

from Bio import SeqIO
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

xps = {
    'Description': '//*/tr[1]/td[2]/span/a[@class="deflnDesc"]',
    'Scientific Name': '//*/tr[1]/td[3]/span/a[@class="sciName"]',
    # 'Common Name': '//*/tr[1]/td[4]/span/a[@class="cmnName"]',
    # 'Taxid': '//*/tr[1]/td[5]/span/a[@class="txid"]',
    'Max Score': '//*/tr[1]/td[6]',
    'Total Score': '//*/tr[1]/td[7]',
    'Query Cover': '//*/tr[1]/td[8]',
    'E value': '//*/tr[1]/td[9]',
    'Per.Ident': '//*/tr[1]/td[10]',
    'Acc.Len': '//*/tr[1]/td[11]',
    'Accession': '//*/tr[1]/td[12]/a[@class="dflSeq"]',
}


def db2csv(db_file, tablename, csv_file):
    """数据库数据转csv文件"""
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute(f"select * from {tablename}")
    data = cursor.fetchall()
    df = pd.DataFrame(data,
                      index=[0],
                      columns=['gene_cluster_id', 'gene_caller_id', 'Sequence', 'Description', 'Scientific Name',
                               'Max Score', 'Total Score', 'Query Cover', 'E value', 'Per Ident', 'Acc Len', 'Accession'])
    df.to_csv(csv_file, sep='\t', index=False)
    print('数据库转csv文件')
    cursor.close()
    db.close()


class Blast(object):
    def __init__(self, record):
        self.record = record

    @property
    def options(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"')
        return options

    def blast_browser(self):
        """基于selenium自动化调试，大部分情况不受限制"""
        print('开启浏览器进程')
        browser = webdriver.Chrome(
            executable_path="D:/env/pyppeteer/local-chromium/588429/chrome-win32/chromedriver.exe",
            options=self.options
        )
        browser.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastx&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')  # blastx
        # browser.find_element_by_id('seq').clear()
        browser.find_element_by_id('seq').send_keys(self.record.seq.upper())
        browser.find_element_by_xpath('//*[@id="blastButton1"]/input').click()
        try:
            table = WebDriverWait(browser, 120).until(ec.presence_of_element_located((By.ID, 'dscTable')))
            # browser.find_element_by_id('btndsConfig').click()
            # browser.find_element_by_xpath('//*[@id="dsConfig"]/li[3]/label').click()
            # browser.find_element_by_xpath('//*[@id="dsConfig"]/li[4]/label').click()
            data = {'Sequence': ''}
            for xp in xps:
                data[xp] = table.find_element_by_xpath(xps[xp]).text
            browser.save_screenshot('ncbi.png')
            browser.close()
            return data
        except Exception as e:
            del e
            print(f'Unknown: {self.record.id}')
            return None
        finally:
            browser.quit()   


def main(record, db_file, f_name):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute(f"select gene_caller_id from annotations")
    gene_cluster_id, gene_caller_id = map(lambda x: x[x.index(':')+1:], record.id.split(','))
    if gene_caller_id not in cursor.fetchall():
        blast = Blast(record)
        data = blast.blast_browser()
        if data:
            data['gene_caller_id'] = gene_caller_id
            data['gene_cluster_id'] = gene_cluster_id
            data['Sequence'] = f_name
            try:
                cursor.execute(f"INSERT INTO annotations values(?,?,?,?,?,?,?,?,?,?,?,?)", tuple(data.values()))
                db.commit()
                print(f'写入【Sequences producing significant alignments】：{data}')
            except Exception as e:
                print(e)
                db.rollback()
        else:
            print('没有匹配到信息')
    else:
        print('序列id已经存在数据库中 或者 没有匹配到信息')
    cursor.close()
    db.close()


if __name__ == "__main__":
    fs = [
        # './seq/BGM48/Core_Clusters.fasta',
        # './seq/BGM48/HC2_Absence.fasta',
        # './seq/DSM20314/Core_Clusters.fasta',
        # './seq/DSM20314/HC2_Absence.fasta',
        './seq/HC2/Core_Clusters.fasta',
        # './seq/HC2/HC_Unique.fasta',
        # './seq/SLC13/Core_Clusters.fasta',
        # './seq/SLC13/HC2_Absence.fasta',
        # './seq/ZFM222/Core_Clusters.fasta',
        # './seq/ZFM222/HC2_Absence.fasta',
        # './seq/ZFM94/Core_Clusters.fasta',
        # './seq/ZFM94/HC2_Absence.fasta',
    ]
    n = 2  # 进程数，根据机器配置改

    for f in fs:
        st = time.time()
        path = os.path.dirname(f)
        f_name = os.path.basename(f).replace('.fasta', '')
        db_file = os.path.join(path, f'annotations.db')

        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS annotations("
                       "gene_caller_id TEXT PRIMARY KEY,gene_cluster_id TEXT,Sequence TEXT,Description TEXT,"
                       "'Scientific Name' TEXT,'Max Score' TEXT,'Total Score' TEXT,'Query Cover' TEXT,"
                       "'E value' TEXT,'Per Ident' TEXT,'Acc Len' TEXT,'Accession' TEXT)")
        cursor.close()
        db.close()

        records = SeqIO.parse(f, 'fasta')
        print(f'读取序列文件')

        function = partial(main, db_file=db_file, f_name=f_name)
        with Pool(processes=n) as pool:
            pool.map(function, [record for record in records])
        et = time.time()
        print(f'运行总时间：{et-st:.6f}秒')

    # 数据库转csv
    # db2csv(db_file=db, tablename=table_name, csv_file='../annotation.csv')
