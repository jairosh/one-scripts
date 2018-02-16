#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: jairo
# @Date:   2018-02-02 15:40:47
# @Last Modified by:   Jairo Sánchez
# @Last Modified time: 2018-02-09 17:03:01

import pandas as pd
import os
import re
import argparse


# REGEX = '([cdmxMANET]*)-.*seed\[(\d+)\]-\[(\d+)\]n-\[([+-]?[0-9]*[.]?[0-9]+),([+-]?[0-9]*[.]?[0-9]+),([+-]?[0-9]*[.]?[0-9]+),([+-]?[0-9]*[.]?[0-9]+)\].*'
REGEX = '([cdmxMANET]*)-.*seed\[(\d+)\]-\[(\d+)\]n.*'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, required=True,
                        help='Directory that contains the reports')
    parser.add_argument('-o', '--output', type=str, required=False,
                        help='Destination file for CSV output')
    args = parser.parse_args()
    if os.path.isdir(args.dir):
        collector = pd.DataFrame()
        pattern = re.compile(REGEX)
        reports = os.listdir(args.dir)
        total = float(len(reports))
        processed = 0.0
        for file in reports:
            reportfile = os.path.join(args.dir, file)
            df = pd.read_table(reportfile, sep=':')
            df1 = df.T
            vars = pattern.match(file).groups()
            df1['scenario'] = vars[0]
            df1['seed'] = vars[1]
            df1['nodes'] = vars[2]
            #df1['alpha'] = vars[3]
            #df1['beta'] = vars[4]
            #df1['delta'] = vars[5]
            #df1['gamma'] = vars[6]
            collector = collector.append(df1, ignore_index=True)
            processed += 1.0
            print('\r{0:04}% '.format(processed * 100.0 / total), end=' ')

        if args.output:
            collector.to_csv(args.output, index=False)
        print('Done')
    else:
        print('ERROR: Invalid directory')
        exit(2)


if __name__ == '__main__':
    main()
