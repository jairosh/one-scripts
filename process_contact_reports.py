#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jairo Sánchez
# @Date:   2017-12-28 14:40:36
# @Last Modified by:   Jairo Sánchez
# @Last Modified time: 2018-01-15 13:35:54

import numpy as np
import pandas as pd
import argparse
import os
import fnmatch
import re
from scipy import stats
import matplotlib.pyplot as plt
from pandas.compat import StringIO
from itertools import izip_longest

FILE_REGEX = '^.*seed\[(\d+)\]-\[(\d+)\].*$'


def process_buffer_usage_stats(directory):
    global FILE_REGEX
    pattern = '*BufferOccupancyReport.txt'
    buffer_files = fnmatch.filter(os.listdir(directory), pattern)
    per_time = dict()
    time_column = pd.DataFrame()
    node_values = []
    for report in buffer_files:
        result = re.match(FILE_REGEX, report)
        nodes, seed = int(result.group(2)), int(result.group(1))
        if nodes not in node_values:
            node_values.append(nodes)

        full_report_path = os.path.join(directory, report)
        report_df = pd.read_csv(full_report_path, sep=' ',
                                names=['time', 'mean', 'variance'])

        if time_column.empty:
            time_column = report_df['time'].astype('int32')

        if nodes not in per_time:
            per_time[nodes] = pd.DataFrame()

        key = '{0}'.format(seed)
        per_time[nodes] = per_time[nodes].assign(**{key: report_df['mean']})

    bu_per_time = pd.DataFrame()
    bu_per_time = bu_per_time.assign(time=time_column)
    for n in node_values:
        mean = per_time[n].mean(axis=1)
        error = stats.sem(per_time[n], axis=1)
        col_name = '{0}'.format(n)
        err_name = '{0}-err'.format(n)
        bu_per_time = bu_per_time.assign(**{col_name: mean,
                                            err_name: error})

    bu_per_nodes = pd.DataFrame()
    mean = bu_per_time.mean()
    error = bu_per_time.sem()
    for n in node_values:
        col_name = '{0}'.format(n)
        entry = {'nodes': n,
                 'usage_avg': mean[col_name],
                 'usage_err': error[col_name]}
        bu_per_nodes = bu_per_nodes.append(entry, ignore_index=True)

    bu_per_nodes = bu_per_nodes.sort_values(by='nodes')
    # bu_per_nodes.plot.line(x='nodes', y='usage_avg', yerr='usage_err')
    # plt.show()
    return bu_per_time, bu_per_nodes


def read_snapshot_report(file_object, nlines, fillvalue):
    args = [iter(file_object)] * nlines
    return izip_longest(*args, fillvalue=fillvalue)


def load_saturation_stats(directory):
    csv_dataframe_path = os.path.join(directory, 'saturation_over_time.csv')
    sat_over_time = pd.read_csv(csv_dataframe_path)
    csv_dataframe_path = os.path.join(directory, 'saturation_over_nodes.csv')
    sat_over_nodes = pd.read_csv(csv_dataframe_path)
    return sat_over_time, sat_over_nodes


def process_saturation_stats(directory):
    global FILE_REGEX
    pattern = '*BFSaturationSnapshotReport.txt'
    report_files = fnmatch.filter(os.listdir(directory), pattern)
    node_values = []
    time_regex = re.compile('^\[(\d+)\]$')
    report_df = pd.DataFrame()
    i = 1

    csv_file_1 = os.path.join(directory, 'saturation_over_time.csv')
    csv_file_2 = os.path.join(directory, 'saturation_over_nodes.csv')
    if os.path.exists(csv_file_1) and os.path.exists(csv_file_2):
        return load_saturation_stats(directory)

    for report in report_files:
        print 'Processing file {0}/{1}'.format(i, len(report_files))
        i = i + 1
        result = re.match(FILE_REGEX, report)
        nodes, seed = int(result.group(2)), int(result.group(1))
        if nodes not in node_values:
            node_values.append(nodes)

        full_report_path = os.path.join(directory, report)
        with open(full_report_path, 'rb') as txt:
            df_text = ''
            time = 0
            for snapshot in read_snapshot_report(txt, nodes + 1, fillvalue=''):
                last_line = re.compile('^[a-z]*{0}'.format(nodes - 1))
                test1 = not time_regex.match(snapshot[0])
                test2 = not last_line.match(snapshot[nodes])
                if test1 or test2:
                    raise AssertionError('Wrong snapshot format')

                df_text = ''.join(snapshot)
                time = int(snapshot[0].replace('[', '').replace(']', ''))
                snapshot_df = pd.read_table(StringIO(df_text), sep=' ',
                                            names=['node', 'saturation'],
                                            skiprows=1)
                row = {'time': time, 'nodes': nodes, 'seed': seed,
                       'mean_saturation': snapshot_df.mean()['saturation']}
                report_df = report_df.append(row, ignore_index=True)

    sat_over_time = pd.DataFrame()
    sat_over_nodes = pd.DataFrame()
    for nodes in report_df.groupby(by='nodes'):
        mean = nodes[1].mean()['mean_saturation']
        se = nodes[1].sem()['mean_saturation']
        n = nodes[1].count()['mean_saturation']
        row = {'nodes': int(nodes[0]),
               'mean': mean,
               'error': se * stats.t.ppf((1.95) / 2., n - 1)}
        sat_over_nodes = sat_over_nodes.append(row, ignore_index=True)

    for snapshot in report_df.groupby('time'):
        row = dict()
        row['time'] = snapshot[0]
        for nodes in snapshot[1].groupby('nodes'):
            mean = nodes[1].mean()['mean_saturation']
            se = nodes[1].sem()['mean_saturation']
            n = nodes[1].count()['mean_saturation']
            h = se * stats.t.ppf((1.95) / 2., n - 1)
            row['{0}'.format(int(nodes[0]))] = mean
            row['{0}-err'.format(int(nodes[0]))] = h

        sat_over_time = sat_over_time.append(row, ignore_index=True)

    csv_dataframe_path = os.path.join(directory, 'saturation_over_time.csv')
    sat_over_time.to_csv(csv_dataframe_path)
    csv_dataframe_path = os.path.join(directory, 'saturation_over_nodes.csv')
    sat_over_nodes.to_csv(csv_dataframe_path)
    return sat_over_time, sat_over_nodes


def plot_over_time(dataframe, series, ylabel, outfile):
    ax = dataframe.plot.line(x='time', y=[str(x) for x in series],
                             grid=True, sort_columns=True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Time (s)')
    plt.savefig(outfile)


def plot_over_nodes(df, series, ylabel, outfile, yaxis='mean', err='error'):
    ax = df.plot.line(x='nodes', y=yaxis, yerr=err,
                      grid=True, sort_columns=True, marker='o')
    ax.set_ylabel(ylabel)
    ax.legend(['Saturation'])
    ax.set_xlabel('Nodes')
    plt.savefig(outfile)


def process_contacts_stats(directory):
    global FILE_REGEX
    pattern = '*FullContactReport.txt'
    report_files = fnmatch.filter(os.listdir(directory), pattern)
    report_df = pd.DataFrame()
    node_values = []
    for report in report_files:
        result = re.match(FILE_REGEX, report)
        nodes, seed = int(result.group(2)), int(result.group(1))
        if nodes not in node_values:
            node_values.append(nodes)

        full_report_path = os.path.join(directory, report)
        with open(full_report_path, 'rb') as txt:
            df = pd.read_table(txt, sep=' ', index_col=False,
                               names=['nodeA', 'nodeB', 'duration'])
            node_col = np.array([nodes] * df.shape[0])
            seed_col = np.array([seed] * df.shape[0])
            df = df.assign(**{'nodes': node_col, 'seed': seed_col})
            report_df = report_df.append(df)

    legends = []
    series = report_df.groupby('nodes').duration
    for s in series:
        ax = s[1].round(1).sort_values().value_counts().sort_index().plot()
        ax.set_xlim(left=0, right=500)
        ax.set_xlabel('Contact duration (s)')
        ax.set_ylabel('Quantity')
        legends.append('n={0}'.format(s[0]))
    ax.legend(legends)

    plt.savefig('/home/jairo/contact_distribution.pdf')
    csv_dataframe_path = os.path.join(directory, 'contacts.csv')
    report_df.to_csv(csv_dataframe_path)
    return report_df, 0


def process_connectivity_ONE_reports(directory):
    global FILE_REGEX
    pattern = '*ConnectivityONEReport.txt'
    report_files = fnmatch.filter(os.listdir(directory), pattern)
    node_values = []
    report_df = pd.DataFrame()

    csv_file = os.path.join(directory, 'contacts_from_connectivity.csv')
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)

    for report in report_files:
        name_data = re.match(FILE_REGEX, report)
        nodes, seed = int(name_data.group(2)), int(name_data.group(1))
        if nodes not in node_values:
            node_values.append(nodes)

        full_report_path = os.path.join(directory, report)
        conndf = pd.read_table(full_report_path, sep=' ',
                               names=['time', 'c', 'nodeA', 'nodeB', 'event'])
        for pair_of_nodes in conndf.groupby(by=['nodeA', 'nodeB']):
            conn_up = []
            if pair_of_nodes[1].shape[0] % 2 != 0:
                print "WARN: Odd number of connection events {0}".format(
                    pair_of_nodes[0])
            first_row = True
            for row in pair_of_nodes[1].itertuples():
                if first_row:
                    if row.event != 'up':
                        raise AssertionError('Conn. didn\'t start with UP')
                        exit(1)
                    first_row = False
                if row.event == 'up':
                    conn_up = row
                elif row.event == 'down':
                    if row.time < conn_up.time:
                        raise AssertionError('Up time mismatch with Down time')
                        exit(1)
                    new_row = {'node a': pair_of_nodes[0][0],
                               'node b': pair_of_nodes[0][1],
                               'conn_start': conn_up.time,
                               'conn_end': row.time,
                               'nodes': nodes,
                               'seed': seed}
                    report_df = report_df.append(new_row, ignore_index=True)
                    conn_up = None

    csv_path = os.path.join(directory, 'contacts_from_connectivity.csv')
    report_df.to_csv(csv_path)
    print report_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory',
                        type=str,
                        help='Report directory', required=True)
    parser.add_argument('-o', '--output',
                        type=str, required=False,
                        help='Output type')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print 'ERROR: {0} is not a directory'.format(args.directory)
        exit(1)

    nodes = [200, 250, 500, 750, 1000]
    # sat_t, sat_n = process_saturation_stats(args.directory)
    # plot_over_time(sat_t, nodes, 'Saturation (%)',
    #                '/home/jairo/saturation_vs_time.pdf')
    # plot_over_nodes(sat_n, nodes, 'Saturation (%)',
    #                '/home/jairo/saturation_vs_nodes.pdf')

    # bu_t, bu_n = process_buffer_usage_stats(args.directory)
    # plot_over_time(bu_t, nodes, 'Buffer Usage (%)',
    #               '/home/jairo/buffer_usage_vs_time.pdf')
    # plot_over_nodes(bu_n, nodes, 'Buffer Usage (%)',
    #                '/home/jairo/buffer_usage_vs_nodes.pdf',
    #                yaxis='usage_avg', err='usage_err')

    # contact_t, contact_n = process_contacts_stats(args.directory)
    process_connectivity_ONE_reports(args.directory)


if __name__ == '__main__':
    main()
