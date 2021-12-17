#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description    'a', {'class': 'deflnDesc'}
Scientific Name    'a', {'class': 'sciName'}
Max Score    'td', {'class': 'c6'}
Total Score    'td', {'class': 'c7'}
Query Cover    'td', {'class': 'c8'}
E value    'td', {'class': 'c9'}
Per. Ident    'td', {'class': 'c10'}
Acc. Len    'td', {'class': 'c11'}
Accession    'a', {'class': 'dflSeq'}
"""

import requests
from bs4 import BeautifulSoup


def main(request_id):
    with requests.get(f'https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID={request_id}') as response:
        soup = BeautifulSoup(response.text, 'lxml')
        if soup.find('section', {'id': 'noResInfo'}):
            print(False)
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
            print(description, sci_name, max_score, total_score, query_cover, e_val, per_ident, acc_len, accession)


if __name__ == '__main__':
    hasRes = 'NGMMFE5V013'
    noRes = 'NBMWZ2PS013'
    main(hasRes)
