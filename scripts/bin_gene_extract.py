#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
python bin_gene_extract.py -s GENOMES.db -p PAN.db -n HC2 -o C:/seq/
"""
import argparse
import os
import sqlite3

import pandas as pd


def extract_sequence(genome_storage_db, pan_db, save_path, name):
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    with sqlite3.connect(genome_storage_db) as conn:
        cur = conn.cursor()
        # 所有序列
        sql = f"SELECT gene_caller_id,dna_sequence FROM gene_info WHERE genome_name == '{name}'"
        data = cur.execute(sql)
        total_gene = pd.DataFrame(data.fetchall(), columns=['gene_caller_id', 'dna_sequence'])
        cur.close()

    with sqlite3.connect(pan_db) as conn:
        cur = conn.cursor()
        # 基因组为name中，总基因簇对应的序列（一对多）
        sql = f"SELECT gene_cluster_id,gene_caller_id FROM gene_clusters WHERE genome_name == '{name}'"
        data = cur.execute(sql)
        df = pd.DataFrame(data.fetchall(), columns=['gene_cluster_id', 'gene_caller_id'])

        # 分箱对应的有效基因簇
        sql = "SELECT bin_name FROM collections_of_splits"
        bins = cur.execute(sql)
        bin_dict, gene_num = {}, {}
        for bin_name in sorted({*bins.fetchall()}):
            bin_name = bin_name[0]
            sql = f"SELECT split FROM collections_of_splits WHERE bin_name == '{bin_name}'"
            data = cur.execute(sql)

            seqs, m, n = [], 0, 0
            for gene_cluster_id in pd.DataFrame(data.fetchall())[0]:
                val = df.loc[(df['gene_cluster_id'] == gene_cluster_id)]['gene_caller_id'].values.tolist()
                if val:
                    seq = ''.join(map(lambda gene_caller_id: ''.join([
                        f">gene_cluster_id:{gene_cluster_id},gene_caller_id:{gene_caller_id}\n",
                        f"{total_gene.loc[gene_caller_id, ['dna_sequence']]['dna_sequence']}\n"
                    ]), val))
                    # print(f'{bin_name} {len(val)}\n{seq}')
                    seqs.append(seq)
                    m += len(val)
                    gene_num[bin_name] = m
                else:
                    # print(f'{bin_name} {gene_cluster_id} {len(val)}')
                    pass
                n += 1
                bin_dict[bin_name] = n

            if seqs:
                with open(os.path.join(save_path, f'{bin_name}.fasta'), 'w', encoding='utf-8') as f:
                    f.write(''.join(seqs))
                    print(f'Save {bin_name}.fasta')

        print(f'gene_clusters: {bin_dict}')
        print(f'gene_numbers: {gene_num}')
        with open(os.path.join(save_path, 'data.json'), 'w', encoding='utf-8') as f:
            f.write(str(gene_num))

        cur.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bin_gene_extract',
                                     description="""the tool of extracting genes from gene clusters.
                                     such as `python bin_gene_extract.py -s GENOMES.db -p PAN.db -n HC2 -o C:/seq/`""")
    parser.add_argument('-s', '--storage', help='genome storage database file path.', required=True, type=str)
    parser.add_argument('-p', '--pan', help='pangenome database file path.', required=True, type=str)
    parser.add_argument('-n', '--name', help='genome name.', required=True, type=str)
    parser.add_argument('-o', '--save', help='gene sequences save path.', required=True, type=str)
    args = parser.parse_args()
    extract_sequence(genome_storage_db=args.storage, pan_db=args.pan, save_path=args.save, name=args.name)
