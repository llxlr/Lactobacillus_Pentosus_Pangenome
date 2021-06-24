#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Find the items that occur in all rows of a table (i.e. rows in which all values are greater than 0) and save to output file.')
parser.add_argument('-i', '--input', help='Input file.')
parser.add_argument('-o', '--output', help='Output file.')
args = parser.parse_args()

d = pd.read_csv(args.input, sep='\t', index_col=0)
d = d.applymap(lambda x: 1 if x>0 else 0)
d.to_csv(args.output, sep='\t')