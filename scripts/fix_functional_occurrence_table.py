#!/usr/bin/env python
# -*- coding: utf-8 -*-
def main(args):
    import pandas as pd
    import re

    input_file = args.input_file
    output_file = args.output_file
    data = pd.read_csv(input_file, sep='\t', index_col=False)

    # deal with the header of the first column
    name_column = list(data.columns)[0]
    new_name_column = 'name'
    data.rename(columns={name_column:new_name_column}, inplace=True )
    name_column = new_name_column

    # change every non alpha numberic sequence to a single '_'
    new_functions_names = data[name_column].map(lambda x: re.sub('[^0-9a-zA-Z]+', '_', x))
    if args.name_dict_output:
        # create a dictionary between old and new names so we can use it later if we need to
        name_dict = dict(zip(list(data[name_column]), list(new_functions_names)))
        pd.DataFrame.from_dict(name_dict, orient='index').to_csv(args.name_dict_output, sep='\t', header=False)
    data[name_column] = new_functions_names

    # Save only the max value between redundant columns
    new_data = data.groupby(name_column).max()

    new_data.sort_values(by=name_column, axis=0, inplace=True)
    new_data.to_csv(output_file, sep='\t')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fix duplicate functions in ad hoc functional pangenome')
    parser.add_argument('--input-file', metavar='FILE', type=str, help='functional occurrence table created with anvi-get-enriched-functions-per-pan-group and --functional-occurrence-table-output option')
    parser.add_argument('--output-file', metavar='FILE', type=str, help='Output file for the functional occurrence table with new function names.')
    parser.add_argument('--name-dict-output', metavar='FILE', type=str, help='A file to store a dictionary to translate between the original and simplified names.', default='')

    args = parser.parse_args()
    main(args)
