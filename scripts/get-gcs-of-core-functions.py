#!/usr/bin/env python
# -*- coding: utf-8 -*-
def main(args):
    import pandas as pd
    data = pd.read_csv(args.enrichment_data, sep='\t', index_col=0)
    name_dict = pd.read_csv(args.name_dict, sep='\t', index_col=0, header=None)
    core_funcs = pd.read_csv(args.core_functions, sep='\t', index_col=0)
    gcs_of_core_functions = []
    for func in core_funcs.index:
        original_func_names = list(name_dict.loc[name_dict[1]==func].index)

        for ori_func in original_func_names:
            gcs_of_core_functions.extend(data.loc[ori_func.strip(),'gene_clusters_ids'].split(', '))

    with open(args.output_file, 'w') as f:
        for g in gcs_of_core_functions:
            f.write(g)
            f.write('\n')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='A very ad-hoc script to get the gene-cluster IDs associated with core functions.')
    parser.add_argument('--enrichment-data', metavar='FILE', type=str, help='Functional enrichment table created with anvi-get-enriched-functions-per-pan-group')
    parser.add_argument('--core-functions', metavar='FILE', type=str, help='List of core functinos created using get-core-functions.py')
    parser.add_argument('--name-dict', metavar='FILE', type=str, help='Functions name dictionary created with fix_functional_occurrence_table.py')
    parser.add_argument('--output-file', metavar='FILE', type=str, help='Output file')

    args = parser.parse_args()
    main(args)
