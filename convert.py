#!/usr/bin/python

import csv

data = []

with open('log', 'rb') as csvfile:
    logreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in logreader:
        data.append((row[0], float(row[1]) / 3600000))

with open('data.csv', 'wb') as csvfile:
    logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in data:
        logwriter.writerow(row)