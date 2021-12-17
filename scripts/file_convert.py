#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3

from Bio import SeqIO
import pandas


def txt2csv(txt_file, csv_file, ):
    if os.path.exists(csv_file):
        os.remove(csv_file)
    with open(csv_file, 'a') as f1:
        f1.write('gene_caller_id,gene_cluster_id,Genome name,Bin,Timestamp,Request ID\n')
        with open(txt_file, 'r', encoding='utf-8') as f2:
            for i in f2.readlines():
                if '[' and ']' in i:
                    string = i.replace(", '", ",").replace("'", "").replace('[', '').replace(']', '')
                    print(string.replace('\n', ''))
                    f1.write(string)


def csv2db(csv_file, db_file, table_name):
    with sqlite3.connect(db_file) as conn:
        df = pandas.read_csv(csv_file)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print('ok')


def fasta2db():
    pass


# txt2csv(txt_file='a.txt', csv_file='ZFM94-Core_Clusters.csv')
# csv2db(csv_file='DSM20314-Core_Clusters-0-1017.csv', db_file='annotations.db', table_name='submits')

fs = [
    './seq/BGM48/Core_Clusters.fasta',
    './seq/BGM48/HC2_Absence.fasta',
    './seq/DSM20314/Core_Clusters.fasta',
    './seq/DSM20314/HC2_Absence.fasta',
    './seq/HC2/Core_Clusters.fasta',
    './seq/HC2/HC_Unique.fasta',
    './seq/SLC13/Core_Clusters.fasta',
    './seq/SLC13/HC2_Absence.fasta',
    './seq/ZFM222/Core_Clusters.fasta',
    './seq/ZFM222/HC2_Absence.fasta',
    './seq/ZFM94/Core_Clusters.fasta',
    './seq/ZFM94/HC2_Absence.fasta',
]

for f in fs:
    genome_name = os.path.dirname(f).split('/')[-1]
    bin_name = os.path.basename(f).replace('.fasta', '').replace('_', ' ')

    db = sqlite3.connect(f'./seq/{genome_name}.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS sequences(gene_caller_id INT PRIMARY KEY,gene_cluster_id CHARACTER,"
                   "'Genome name' CHARACTER,'Bin' CHARACTER,Sequence TEXT)")
    cursor.close()
    db.close()
    for record in SeqIO.parse(f, 'fasta'):
        gene_cluster_id, gene_caller_id = map(lambda x: x[x.index(':') + 1:], record.id.split(','))
        db = sqlite3.connect(f'./seq/{genome_name}.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO sequences values(?,?,?,?,?)",
                       tuple([int(gene_caller_id), gene_cluster_id, genome_name, str(bin_name), str(record.seq.upper())]))
        db.commit()
        cursor.close()
        db.close()
    print('ok')
