#coding=utf-8

import sys
import struct
import csv
import re
import json


p1 = re.compile(r"(.*) - (.*)")
re.compile(p1)


def read_rows(rows, fileName):
	
	f = open(fileName, "r")

	while True:
		line = f.readline()
		if line:
			print line
			m = re.match(p1, line)
			ts = m.group(1)
			data = m.group(2)

			row = [ts]

			data = data.replace("'", "\"")
			data = data.replace("True", "\"True\"")
			data = json.loads(data)
			row.extend(data.get("res"))
			row.extend(data.get("raw"))
			row.extend(data.get("offset"))
			row.extend(data.get("reference_unit"))
			print row

			rows.append(row)
		else:
			break

	f.close()
	return rows


def writeRows(rows, fileName):
	f = open(fileName, "wb")
	writer = csv.writer(f)
	for row in rows:
		writer.writerow(row)

logFiles = ["test.log.5", "test.log.4", "test.log.3", "test.log.2", "test.log.1", "test.log"]
rows = []
for logFile in logFiles:
	rows = read_rows(rows, logFile)

writeRows(rows, "merged_log.csv")
