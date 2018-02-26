#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: jairo
# @Date:   2018-02-02 15:40:47
# @Last Modified by:   Jairo Sanchez
# @Last Modified time: 2018-02-26 11:59:08

import pandas as pd
import os
import re
import argparse


class FilenameVariablesExtractor:
    """Defines a generic filename parser, to extract variables embedded in the
    filename and export them as DataFrame
    """
    def __init__(self, filename):
        pass

    def parse(self):
        """Main method for the derived classes to implement"""
        raise NotImplementedError()

    def get_groups(self):
        self._pattern = re.compile(self._REGEX)
        vars = self._pattern.match(self._fn).groups()
        if not vars:
            raise ValueError('No match in filename with provided regex')
        return vars


class SigmoidSim(FilenameVariablesExtractor):
    def __init__(self, filename):
        self._REGEX = ('([cdmxMANET]*)-.*seed\[(\d+)\]-\[(\d+)\]n-'
                       '\[([+-]?[0-9]*[.]?[0-9]+),([+-]?[0-9]*[.]?[0-9]+),'
                       '([+-]?[0-9]*[.]?[0-9]+),([+-]?[0-9]*[.]?[0-9]+)\].*')
        self._fn = filename

    def parse(self):
        df1 = pd.DataFrame()
        vars = self.get_groups()
        df1['scenario'] = vars[0]
        df1['seed'] = vars[1]
        df1['nodes'] = vars[2]
        df1['alpha'] = vars[3]
        df1['beta'] = vars[4]
        df1['delta'] = vars[5]
        df1['gamma'] = vars[6]

        return df1


class BasicSim(FilenameVariablesExtractor):
    def __init__(self, filename):
        self._REGEX = '([cdmxMANET]*)-.*seed\[(\d+)\]-\[(\d+)\]n.*'
        self._fn = filename

    def parse(self):
        df1 = pd.DataFrame()
        vars = self.get_groups()
        df1['scenario'] = vars[0]
        df1['seed'] = vars[1]
        df1['nodes'] = vars[2]
        return df1


class CRAWDADSim(FilenameVariablesExtractor):
    def __init__(self, filename):
        self._REGEX = '(.*Router)_\[(\d+)\]ttl_\[(\d+)\]s_seed\[(.*)\].*'
        self._fn = filename

    def parse(self):
        ser = pd.Series()
        vars = self.get_groups()
        ser['router'] = vars[0]
        ser['ttl'] = vars[1]
        ser['runtime'] = vars[2]
        ser['message_seed'] = vars[3]
        return ser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, required=True,
                        help='Directory that contains the reports')
    parser.add_argument('-o', '--output', type=str, required=False,
                        help='Destination file for CSV output')
    args = parser.parse_args()
    if os.path.isdir(args.dir):
        collector = pd.DataFrame()
        reports = os.listdir(args.dir)
        total = float(len(reports))
        processed = 0.0
        for file in reports:
            reportfile = os.path.join(args.dir, file)
            data_series = pd.read_table(reportfile, sep=':', squeeze=True)
            df1 = data_series.append(CRAWDADSim(file).parse())
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
