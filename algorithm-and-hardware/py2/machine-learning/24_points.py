import csv


def add(a, b):
	return a + b


def minus(a, b):
	return abs(a - b)


def times(a, b):
	return a * b


def divided(a, b):
	if not check_division(a, b):
		return False
	if a > b:
		return a / b
	else:
		return b / a


def check_division(a, b):
	return a != 0 and b != 0 and (a % b == 0 or b % a == 0)


operations = [add, minus, times, divided]


def calculation(arr):
	if len(arr) == 1:
		return arr[0] == 24
	for i in range(len(arr) - 1):
		for j in range(i + 1, len(arr)):
			for operator in operations:
				newarr = get_new_array(arr, i, j, operator)
				if calculation(newarr):
					print getattr(operator, "__name__") + str([int(arr[i]), int(arr[j])]) \
						+ "=" + str(newarr[i]) + ", and get" + str(newarr)
					return True
	return False


def get_new_array(arr, i, j, operator):
	if not arr[i] or not arr[j]:
		return [False]
	newarr = arr[:]
	newarr[i] = operator(int(arr[i]), int(arr[j]))
	del newarr[j]
	return newarr


# import sys
# print calculation(sys.argv[1:])


def generate_data():
	rows = []
	for i in xrange(1, 14):
		for j in xrange(1,14):
			for k in xrange(1,14):
				for l in xrange(1,14):
					row = [i, j, k, l]
					result = calculation(row)
					row.append(result)
					rows.append(row)
	return rows


with open("test_data.csv", "w") as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow(["a", "b", "c", "d", "tag"])
	writer.writerows(generate_data())
