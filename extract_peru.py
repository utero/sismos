#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from argparse import RawTextHelpFormatter
import codecs
import sys


def extract(filename, date_start, date_end):
    import os
    import json
    import time
    from datetime import datetime

    date_start = datetime.strptime(date_start, "%Y-%m-%d")
    date_end = datetime.strptime(date_end, "%Y-%m-%d")

    if os.path.isfile(filename):
        f = codecs.open(filename, "r", "utf8")
        data = json.loads(f.read())
        f.close()

        sismos_peru = []
        for i in data['features']:
            if "Peru" in i['properties']['place']:
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['properties']['time']/1000))
                date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                if date_start <= date_obj and date_end >= date_obj:
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
    parser.add_argument('-s', '--start', action='store',
            metavar='date start',
            help=u'''fecha de inicio YYYY-MM-DD''',
            required=True, dest='date_start')
    parser.add_argument('-e', '--end', action='store',
            metavar='date end',
            help=u'''fecha final YYYY-MM-DD''',
            required=True, dest='date_end')

    args = parser.parse_args()
    filename = args.filename.strip()

    date_start = args.date_start.strip()
    date_end = args.date_end.strip()

    extract(filename, date_start, date_end)



if __name__ == "__main__":
    main()
