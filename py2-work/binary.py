import sys
import struct
import csv

def readRows(fileName):
	rows = []
	f = open(fileName, "rb")
	while True:
		flag = f.read(3)
		if len(flag) < 3:
			break

		if flag == b'\x20\x03\x04':
			data = f.read(4)
			row = struct.unpack(">2h", data)[0]
			rows.append(row)

			flag = f.read(2)
			# if flag != b'\x2B\xBD':
			# 	break
	f.close()
	return rows


def writeRows(rows, fileName):
	f = open(fileName, "wb")
	writer = csv.writer(f)
	for row in rows:
		writer.writerow([row])


rows = readRows(sys.argv[1])

resultFile = "HEX_DATA.csv"
if len(sys.argv) > 2:
	resultFile = sys.argv[2]

writeRows(rows, resultFile)