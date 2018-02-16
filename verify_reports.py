#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Jairo Sánchez
# @Date:   2018-02-02 16:45:11
# @Last Modified by:   Jairo Sánchez
# @Last Modified time: 2018-02-09 16:45:31

import pandas as pd
import argparse
import os


SEEDS = [78802, 94176, 65221, 44180, 79009, 68831, 73906, 15598, 78051, 71182,
         15475, 45907, 5768, 28749, 24113, 80454, 59004, 54008, 70, 8439, 22,
         58405, 38517, 33282, 5481, 11778, 96617, 52770, 55182, 5327, 11131,
         61959, 44450, 4762, 20098, 61667, 15405, 98682, 82509, 65139, 4029,
         90521, 98820, 3136, 35402, 64524, 37578, 16966, 84181, 91016]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--csv', help='Input CSV file', type=str,
                        required=True)
    parser.add_argument('-d', '--dir', help='Simulation reports directory',
                        required=True, type=str)
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print('ERROR: Invalid directory')
        exit(1)

    if not os.path.isfile(args.csv):
        print('ERROR: Invalid file')

    data = pd.read_csv(args.csv)
    for index, experiment in data.iterrows():
        fname = ''
        if 'Scenario.name' in experiment:
            fname = experiment['Scenario.name']
            fname = fname.replace('%%Group.nrofHosts%%', str(experiment['Group.nrofHosts']))
            fname = fname.replace('%%BFGMPRouter.weightAlpha%%', str(experiment['BFGMPRouter.weightAlpha']))
            fname = fname.replace('%%BFGMPRouter.weightBeta%%', str(experiment['BFGMPRouter.weightBeta']))
            fname = fname.replace('%%BFGMPRouter.weightDelta%%', str(experiment['BFGMPRouter.weightDelta']))
            fname = fname.replace('%%BFGMPRouter.weightGamma%%', str(experiment['BFGMPRouter.weightGamma']))
            fname = fname + '_MessageStatsReport.txt'
            for seed in SEEDS:
                fullname = fname.replace('%%MovementModel.rngSeed%%', str(seed))
                filepath = os.path.join(args.dir, fullname)
                if not os.path.isfile(filepath):
                    print('MISSING SIM REPORT: {0}'.format(filepath))
                else:
                    print('FOUND: {0}'.format(filepath))
        else:
            print('ERROR: Template for file name not found!')
            exit(2)

if __name__ == '__main__':
    main()
