#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Bio.SeqUtils import GC
from Bio import SeqIO
import os
import re

path = '../sequence/origin/'

for file in os.listdir(path):
    strain = os.path.basename(file).replace('.fna', '')
    print(f'Strain: {strain}')
    seq = ''
    for record in SeqIO.parse(path+file, 'fasta'):
        seq += str(record.seq)
        result = re.search(r'plasmid (.*?),', record.description)
        plasmid = f"\tPlasmid: {re.sub(r'plasmid |,', '', result.group())}" if result else ''
        print(f"GB: {record.id}\tSize: {len(str(record.seq))} bp\tGC: {GC(str(record.seq))} %{plasmid}")
    print(f'Total Size: {len(seq)} bp')
    print(f'Total GC: {GC(seq)} %')
    print('\n')
