#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Jairo Sanchez
# @Date:   2018-08-14 15:35:08
# @Last Modified by:   Jairo Sanchez
# @Last Modified time: 2018-08-14 17:39:24
import argparse
import os
import svgwrite
from geomet import wkt


def load_wkt(filepath):
    """Loads the content of a file into a GeoJSON object

    Args:
        filepath (str): The path to the file

    Returns:
        dict: A dictionary with the representation of the file
    """
    geojson = []
    with open(filepath, 'r') as input_file:
        for line in input_file.readlines():
            try:
                wkt_contents = wkt.loads(line)
                geojson.append(wkt_contents)
            except ValueError as value:
                print('Unrecognized geometry: {}'.format(value))
    return geojson


def main():
    """Main method

    Raises:
        FileNotFoundError: Description
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wkt', help='WKT file to render', type=str)
    parser.add_argument('-o', '--out', help='SVG File to write', type=str)
    args = parser.parse_args()

    output_file = 'default.svg'
    if args.out:
        if os.path.exists(args.out):
            print('ERROR: Output file already exists.')
            exit(1)
        output_file = args.out

    if os.path.exists(args.wkt):
        geojson = load_wkt(args.wkt)
        dwg = svgwrite.Drawing(filename=output_file)
        for shape in geojson:
            if shape['type'] == 'LineString':
                print('LINE')
    else:
        raise FileNotFoundError('WKT File doesn\'t exists')


if __name__ == '__main__':
    main()
