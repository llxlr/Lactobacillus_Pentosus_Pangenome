#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

seq1 = 'ATCG'
seq2 = 'ATGGAATTAGACGCTCAAATGCAATCATGGCTTCATGGCGTCAAAGATTTAATTCCTAACACGTCCGTAAAATCAGCAATGACAGCTGCTGAAGCGCAAGCATACGCAGAAGTGTTACGTAAAAATACACCACGATCCGACAATGATGATAGCGAGTATGGTCATTTACAAGACAACATTGCGATTCAAAACAGTGATGTAGACGGCATTGTTAATGGTAATACGCTAGCTGGTTTTGGCAAGAAAGCGTATATTGCTGGATTCTTGAATGATGGGACCGTAAAGATGGCGGCAACTCATTTTGTTGACGATTCTAGACGAGAATCTCAGGAAGCGGCCTTTAAAGCCGGTATGGCAGTTTACAAAGCTAAAACGGGTGGTGAATAG'

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                     'like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"')

print('打开浏览器')
browser = webdriver.Chrome(
    executable_path="D:/env/pyppeteer/local-chromium/588429/chrome-win32/chromedriver.exe",
    options=options
)
browser.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastx&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')  # blastx
# browser.find_element_by_id('seq').clear()
print('键入基因序列')
browser.find_element_by_id('seq').send_keys(seq2)
browser.find_element_by_xpath('//*[@id="blastButton1"]/input').click()
print('正在刷新页面')
if browser.find_element_by_id('statInfo'):
    request_id = browser.find_element_by_xpath('//*[@id="statInfo"]/tbody/tr[1]/td[2]/b').text
    if browser.find_element_by_xpath('//*[@id="statInfo"]/tbody/tr[3]/td[1]').text != 'Submitted at':
        time.sleep(1)
    timestamp = browser.find_element_by_xpath('//*[@id="statInfo"]/tbody/tr[3]/td[2]').text
    print(request_id, timestamp)
else:
    print('没有获得状态表')
browser.close()
