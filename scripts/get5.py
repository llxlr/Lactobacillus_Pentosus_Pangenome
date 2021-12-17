#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"')


def is_exist(driver, id: str) -> bool:
    """判断页面某元素是否存在"""
    try:
        driver.find_element_by_id(id)
        return True
    except:
        return False


def get_rid(sequence: str) -> str:
    """获取RID"""
    driver = webdriver.Chrome(
        executable_path="D:/env/pyppeteer/local-chromium/588429/chrome-win32/chromedriver.exe",
        options=options
    )
    try:
        driver.set_page_load_timeout(60)
        driver.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastx&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')
    except:
        driver.quit()
        return get_rid(sequence)

    try:
        driver.find_element_by_id('seq').send_keys(sequence)
        driver.find_element_by_id('blastButton1').click()
    except:
        driver.quit()
        return get_rid(sequence)

    for i in range(5):
        if is_exist(driver, 'statInfo'):
            try:
                rid = driver.find_element_by_xpath('//*[@id="statInfo"]/tbody/tr[1]/td[2]/b').text
                driver.quit()
                return rid
            except:
                time.sleep(1)
        else:
            continue
    driver.quit()
    return ''


def get_func(rid: str) -> List:
    """获取注释信息"""
    driver = webdriver.Chrome(
        executable_path="D:/env/pyppeteer/local-chromium/588429/chrome-win32/chromedriver.exe",
        options=options
    )

    try:
        driver.set_page_load_timeout(60)
        driver.get(f'https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID={rid}')
    except:
        driver.quit()
        return get_func(rid)

    for i in range(5):
        try:
            if is_exist(driver, 'statInfo'):
                time.sleep(10)
            if is_exist(driver, 'noResInfo'):
                driver.quit()
                return []
            if is_exist(driver, 'mainCont'):
                description = driver.find_element_by_xpath('//*/tr[1]/td[2]/span/a[@class="deflnDesc"]').text
                sci_name = driver.find_element_by_xpath('//*/tr[1]/td[3]/span/a[@class="sciName"]').text
                max_score = driver.find_element_by_xpath('//*/td[@class="c6"]').text
                total_score = driver.find_element_by_xpath('//*/td[@class="c7"]').text
                query_cover = driver.find_element_by_xpath('//*/td[@class="c8"]').text
                e_val = driver.find_element_by_xpath('//*/td[@class="c9"]').text
                per_ident = driver.find_element_by_xpath('//*/td[@class="c10"]').text
                acc_len = driver.find_element_by_xpath('//*/td[@class="c11 acclen"]').text
                accession = driver.find_element_by_xpath('//*/td[@class="c12 l lim"]').text
                driver.quit()
                return [description, sci_name, max_score, total_score, query_cover, e_val, per_ident, acc_len, accession]
        except:
            continue
    driver.quit()
    return []


if __name__ == '__main__':
    # db_file = "D:/Projects/PyCharmProjects/a/seq/BGM48.db"
    # conn = sqlite3.connect(db_file)
    # cur = conn.cursor()
    # db = cur.execute("SELECT * FROM sequences ORDER BY gene_caller_id")
    # sequences = pd.DataFrame(db.fetchall())
    # cur.close()
    # conn.close()
    # for i in sequences.iloc:
    #     gene_caller_id, gene_cluster_id, genome_name, bin_name, sequence = i.values.tolist()
    #     rid = get_rid(sequence)
    #     if rid:
    #         # print(rid)
    #         # print([gene_caller_id, gene_cluster_id, genome_name, bin_name, rid])
    #         function = get_func(rid)
    #         if function:
    #             data = [gene_caller_id, gene_cluster_id, genome_name, bin_name]
    #             data.extend(function)
    #             print(data)

    # BGM48
    # DSM20314
    df = pd.read_csv('DSM20314-rid.csv')
    for i in df.iloc:
        gene_caller_id, gene_cluster_id, genome_name, bin_name, rid = i.values.tolist()
        function = get_func(rid)
        if function:
            data = [str(gene_caller_id), gene_cluster_id, genome_name, bin_name]
            data.extend(function)
            print(','.join(data))
