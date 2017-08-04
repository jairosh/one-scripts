#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jairo Sanchez
# @Date:   2017-06-19 02:05:52
# @Last Modified by:   Jairo Sanchez
# @Last Modified time: 2017-06-24 00:00:41
import argparse
import os.path
import re
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import json
import numpy as np
from scipy.interpolate import griddata


class Node:
    """docstring for Node"""
    def __init__(self, jsonRepr):
        self.time = jsonRepr['time']
        self.id = str(jsonRepr['id'])
        self.myID = jsonRepr['router']['myID']
        self.x = jsonRepr['x']
        self.y = jsonRepr['y']
        self.m = jsonRepr['router']['m']
        self.k = jsonRepr['router']['k']
        self.c = jsonRepr['router']['c']
        self.Ft = jsonRepr['router']['Ft']

    def probabilityProductTo(self, destinationID):
        pr = 1.0
        for h in destinationID:
            pr *= self.Ft[h]
        return pr / (self.c**self.k)

    def __str__(self):
        return '{0} @ ({1}, {2}), hashes= {3}'.format(
            self.id, self.x, self.y, self.myID)


class Point:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return '{2}({0}, {1})'.format(self.x, self.y, self.name)


def create_frame(message_locations, dest_location, bfgDistrib, title, msg, outfile):
    plt.figure(figsize=(12.6, 9), dpi=150)
    plt.title(title)

    # Set the map layer
    plt.imshow(plt.imread(r'mapa_bw.png'),
               interpolation='nearest', alpha=0.9,
               extent=[0, 35000, 0, 25000])

    if len(bfgDistrib) > 0:
        # Plot BFG Gradient
        xi = bfgDistrib[0]
        yi = bfgDistrib[1]
        zi = bfgDistrib[2]
        plt.contourf(xi, yi, zi, 15, cmap=plt.cm.inferno,
                     vmax=1.0, vmin=0.0, alpha=0.5)
        plt.clim(0, 1)
        plt.colorbar()

    # Plot the message locations
    for node in message_locations:
        plt.plot([node.x], [node.y], marker='o', color='b',
                 markersize=7, markeredgewidth=2.5)

    # Plot the destination node location
    plt.plot([dest_location.x], [dest_location.y], marker='o',
             color='g', markersize=7, markeredgewidth=2)

    msg_legend = 'Message ({0})'.format(msg)
    dest_patch = mpatches.Patch(color='green', label=msg_legend)
    msg_patch = mpatches.Patch(color='blue', label='Message')
    plt.legend(handles=[dest_patch, msg_patch], loc=8, fontsize='small')

    plt.axes().set_aspect('equal', 'datalim')
    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)
    plt.gca().invert_yaxis()
    # plt.show()
    plt.savefig(outfile)
    plt.close()


def process_message_locations(msg_loc_report, msg):
    # for each "instant", save a list of points
    messages_at_time = dict()
    with open(msg_loc_report, 'rb') as infile:
        time = 0
        line_number = 0
        pattern = '.*{0}( |$).*'.format(msg)
        regex = re.compile(pattern)
        # print 'Pattern: {0}'.format(pattern)
        for line in infile.readlines():
                line_number += 1
                if '[' in line:
                    time = int(re.sub('[\[\]]', '', line))
                else:
                    if regex.match(line):
                        if re.match(r'\((.*?)\)', line):
                            p = re.match(r'\((.*?)\)', line)
                            coord = re.split(',', p.group(1))
                            point = Point(float(coord[0]), float(coord[1]),
                                          msg)
                            if time in messages_at_time:
                                messages_at_time[time].append(point)
                            else:
                                messages_at_time[time] = []
                                messages_at_time[time].append(point)
                        else:
                            print 'ERROR: unrecognizable line format'
    return messages_at_time


def process_destination_location(node_loc_report, node):
    # Store all values in this dictionary; key=TIME, value=Point
    node_loc = dict()
    with open(node_loc_report, 'rb') as inputreport:
        time = 0
        line_number = 0
        regex = '^{0} '.format(node)
        for line in inputreport:
            line_number += 1
            if '[' in line:
                time = int(re.sub('[\[\]]', '', line))
            else:
                if re.match(regex, line):
                    fields = re.split(' ', line)
                    point = Point(fields[1], fields[2], fields[0])
                    node_loc[time] = point

    return node_loc


def process_gradient(reportFile, destination, time):
    nodes = []
    # Search for time in file
    regex = re.compile('\[(\d+)\]')
    readingTime = False
    dstFound = False
    with open(reportFile, 'rb') as inputF:
        for line in inputF:
            if regex.match(line):
                ftime = int(regex.match(line).group(1))
                continue

            # Found the given time, then read all subsequent lines
            if ftime == time:
                readingTime = True
            # Check if we already reached the section of interest in the file
            elif not readingTime:
                continue  # Skip the line
            else:
                break  # We reached the next time section in the file

            # Each line is a JSON object
            jNode = json.loads(line)
            theNode = Node(jNode)
            # print '{0}=={1}'.format(theNode.id, destination)
            if theNode.id == destination:
                dstFound = True
                dstNode = theNode

            nodes.append(theNode)

    if not dstFound:
        print 'ERROR: Destination node not found in {0}'.format(reportFile)
        exit(4)

    X, Y, Z = np.array([]), np.array([]), np.array([])
    for node in nodes:
        X = np.append(X, node.x)
        Y = np.append(Y, node.y)
        Z = np.append(Z, node.probabilityProductTo(dstNode.myID))

    # Create x-y points to be used in heatmap (scenario specific)
    xi = np.linspace(0, 34999, 1000)
    yi = np.linspace(0, 24999, 1000)

    # Z is a matrix of x-y values
    zi = griddata((X, Y), Z, (xi[None, :], yi[:, None]), method='linear',
                  fill_value=0)

    return (xi, yi, zi)


def get_destination_node(reportFile, message):
    with open(reportFile, 'rb') as inputfile:
        for line in inputfile:
            fields = re.split(' ', line)
            if message in fields[1]:
                return fields[4]
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scenario',
                        type=str,
                        help='Scenario name, without the report suffixes',
                        required=True)
    parser.add_argument('-m', '--message',
                        help='ID of the message to plot',
                        type=lambda s: unicode(s, 'utf8'),
                        required=True)
    parser.add_argument('-t', '--step',
                        help='Time between snapshots in the input file',
                        type=int)
    parser.add_argument('-g', '--gradient',
                        required=False, action='store_true')
    args = parser.parse_args()

    reports = dict()
    reports['msg_loc'] = '{0}_MessageLocationReport.txt'.format(args.scenario)
    reports['nod_loc'] = '{0}_LocationSnapshotReport.txt'.format(args.scenario)
    reports['msgs'] = '{0}_CreatedMessagesReport.txt'.format(args.scenario)
    if args.gradient:
        suffix = '_BloomFilterSnapshotReport0000.txt'
        reports['bfg'] = '{0}{1}'.format(args.scenario, suffix)

    for f in reports.iterkeys():
        if not os.path.isfile(reports[f]):
            print 'ERROR: File does not exist! {0}'.format(reports[f])
            exit(1)

    dest_node = get_destination_node(reports['msgs'], args.message)
    if dest_node is '':
        print 'ERROR: The specified message was not found in the sim report'
        exit(2)

    copies = process_message_locations(reports['msg_loc'], args.message)
    dest_locs = process_destination_location(reports['nod_loc'], dest_node)

    # Get the time for the last register in messages
    times = list(copies.keys())
    times.sort()
    max_time = times[-1]
    print 'Message exist from {0} to {1}'.format(times[0], times[-1])
    index = 0
    for i in range(args.step, max_time + 1, args.step):
        filename = '{1}/{0:0>8}.png'.format(index, args.scenario)
        index += 1
        print '\rProgress {0:.2f}%'.format((float(i) / float(max_time)) * 100.0),
        # Check if the gradient of the probabilistic space should be plotted
        probSp = ()
        if args.gradient:
            probSp = process_gradient(reports['bfg'], dest_node, i)

        if i in dest_locs:
            if i in copies:
                title = 't={0} s, Active copies: {1}'.format(i, len(copies[i]))
                # Have all data to plot
                create_frame(copies[i], dest_locs[i], probSp, title, args.message, filename)
            else:
                title = 't={0} s, Active copies: 0'.format(i)
                # The destination node already in sim but no messages
                create_frame([], dest_locs[i], probSp, title, args.message, filename)
        else:
            # There's at least one message, but destiantion doesn't exist
            print 'ERROR: The destination node had no coords. at time {0}'.\
                  format(i)
            exit(3)


if __name__ == '__main__':
    main()
