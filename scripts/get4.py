#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Pool
import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd

options = Options()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"')

def get_func(args):
    gene_caller_id, gene_cluster_id, genome_name, bin_name, sequence = args
    browser = webdriver.Chrome(
            executable_path="D:/env/pyppeteer/local-chromium/588429/chrome-win32/chromedriver.exe",
            options=options
    )
    browser.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastx&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')
    browser.find_element_by_id('seq').send_keys(sequence)
    browser.find_element_by_id('blastButton1').click()
    try:
        table = WebDriverWait(browser, 120).until(ec.presence_of_element_located((By.ID, 'dscTable')))
        description = table.find_element_by_xpath('//*/tr[1]/td[2]/span/a[@class="deflnDesc"]').text
        sci_name = table.find_element_by_xpath('//*/tr[1]/td[3]/span/a[@class="sciName"]').text
        max_score = table.find_element_by_xpath('//*/td[@class="c6"]').text
        total_score = table.find_element_xpath('//*/td[@class="c7"]').text
        query_cover = table.find_element_xpath('//*/td[@class="c8"]').text
        e_val = table.find_element_by_xpath('//*/td[@class="c9"]').text
        per_ident = table.find_element_by_xpath('//*/td[@class="c10"]').text
        acc_len = table.find_element_by_xpath('//*/td[@class="c11"]').text
        accession = table.find_element_by_xpath('//*/td[@class="c12"]').text
        print([gene_caller_id, gene_cluster_id, genome_name, bin_name,
               description, sci_name, max_score, total_score, query_cover, e_val, per_ident, acc_len, accession])
        browser.close()
    except:
        pass
    finally:
        browser.quit()


if __name__ == '__main__':
    db_file = "D:/Projects/PyCharmProjects/a/seq/BGM48.db"
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        db = cur.execute("SELECT * FROM sequences ORDER BY gene_caller_id")
        sequences = pd.DataFrame(db.fetchall())
        cur.close()
        for i in sequences.iloc:
            data = i.values.tolist()
            get_func(data)
