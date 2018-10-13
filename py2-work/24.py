import sys
import pandas as pd
import csv

def add(a, b):
	return a + b

def minus(a, b):
	return abs(a - b)

def times(a, b):
	return a * b

def divided(a, b):
	if checkDivision(a, b) == False:
		return False
	if a > b:
		return a / b
	else:
		return b / a

def checkDivision(a, b):
	return a != 0 and b != 0 and (a % b == 0 or b % a == 0)

operations = [add, minus, times, divided]

def calculation(arr):
	if len(arr) == 1:
		return arr[0] == 24
	for i in range(len(arr) - 1):
		for j in range(i + 1, len(arr)):
			for f in operations:
				newarr = getNewArray(arr, i, j, f)
				if calculation(newarr):
					print getattr(f, "__name__") + str([int(arr[i]), int(arr[j])]) + "=" + str(newarr[i]) + ", and get" + str(newarr)
					return True
	return False

def getNewArray(arr, i, j, f):
	if arr[i] == False or arr[j] == False:
		return [False]
	newarr = arr[:]
	newarr[i] = f(int(arr[i]), int(arr[j]))
	del newarr[j]
	return newarr

# print calculation(sys.argv[1:])

arr = []
for i in xrange(1,14):
	for j in xrange(1,14):
		for k in xrange(1,14):
			for l in xrange(1,14):
				row = [i, j, k, l]
				result = calculation(row)
				row.append(result)
				arr.append(row)
print str(arr[5])



with open("test_data.csv","w") as csvfile: 
    writer = csv.writer(csvfile)

    
    writer.writerow(["a","b","c","d","tag"])
    
    writer.writerows(arr)
