#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from argparse import RawTextHelpFormatter
import codecs
import sys


def extract(filename):
    import os
    import json
    import time

    if os.path.isfile(filename):
        f = codecs.open(filename, "r", "utf8")
        data = json.loads(f.read())
        f.close()

        sismos_peru = []
        for i in data['features']:
            if "Peru" in i['properties']['place']:
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['properties']['time']/1000))
                i['properties']['date'] = date
                sismos_peru.append(i)

        out = {}
        out['type'] = 'FeatureCollection'
        out['features'] = sismos_peru
        print json.dumps(out)



def main():
    description = u"""Este script extrae sismos para Peru usando datos tomados
    de http://earthquake.usgs.gov/."""

    parser = argparse.ArgumentParser(description=description,formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--filename', action='store',
            metavar='file.geojson',
            help=u'''archivo con datos en formato GeoJSON.''',
            required=True, dest='filename')

    args = parser.parse_args()
    filename = args.filename.strip()

    extract(filename)



if __name__ == "__main__":
    main()
