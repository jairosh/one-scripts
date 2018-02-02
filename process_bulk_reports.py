#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: jairo
# @Date:   2018-02-02 15:40:47
# @Last Modified by:   jairo
# @Last Modified time: 2018-02-02 15:55:58

import pandas as pd
import os
import re
import argparse


REGEX = '.*seed\[(\d+)\]-\[(\d+)\]n-\[([+-]?[0-9]*[.]?[0-9]+),([+-]?[0-9]*[.]?[0-9]+),([+-]?[0-9]*[.]?[0-9]+),([+-]?[0-9]*[.]?[0-9]+)\].*'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, required=True,
                        help='Directory that contains the reports')
    args = parser.parse_args()
    if os.path.isdir(args.dir):
        collector = pd.DataFrame()
        pattern = re.compile(REGEX)
        for file in os.listdir(args.dir):
            reportfile = os.path.join(args.dir, file)
            df = pd.read_table(reportfile, sep=':')
            df1 = df.T
            vars = pattern.match(file).groups()
            print(vars)
            df1['seed'] = vars[0]
            df1['nodes'] = vars[1]
            df1['alpha'] = vars[2]
            df1['beta'] = vars[3]
            df1['delta'] = vars[4]
            df1['gamma'] = vars[5]
            collector = collector.append(df1, ignore_index=True)

        print(collector)


if __name__ == '__main__':
    main()
