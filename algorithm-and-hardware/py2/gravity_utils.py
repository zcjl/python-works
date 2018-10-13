# coding:utf-8

import serial
import struct
import binascii
import datetime
from enum import Enum


class GravityUtils:

	def __init__(self):
		# 打开端口
		self.ports = {
			"g_sensor_1": serial.Serial(port='/dev/tty.usbserial-FT2J03F3A', timeout=0.04),
			"g_sensor_2": serial.Serial(port='/dev/tty.usbserial-FT2J03F3B', timeout=0.04),
			"g_sensor_3": serial.Serial(port='/dev/tty.usbserial-FT2J03F3C', timeout=0.04),
			"g_sensor_4": serial.Serial(port='/dev/tty.usbserial-FT2J03F3D', timeout=0.04)
			# "g_sensor_1": serial.Serial(port='/dev/ttyUSB0', timeout=0.04),
			# "g_sensor_2": serial.Serial(port='/dev/ttyUSB1', timeout=0.04),
			# "g_sensor_3": serial.Serial(port='/dev/ttyUSB2', timeout=0.04),
			# "g_sensor_4": serial.Serial(port='/dev/ttyUSB3', timeout=0.04)
			# "g_sensor_1": serial.Serial(port='/dev/ttys1', timeout=0.04)
			# "g_sensor_2": serial.Serial(port='/dev/ttys2', timeout=0.04),
			# "g_sensor_3": serial.Serial(port='/dev/ttys2', timeout=0.04),
			# "g_sensor_4": serial.Serial(port='/dev/ttys3', timeout=0.04)
		}
		self.offset = 355568  # 原始重力值读数的位移差量 -> 20 33 33 30 34
		self.bias = 160000  # 原始重力值在10千克位上有一个跃迁差量（从20直接到31）
		self.format = "B"  # 按位读取原始重力值的16进制数据
		self.decimal = 10  # 并逐一转换为对应的10进制数据

	"""
	通过USB转串口，读取重力感应器重力值数据	
	"""
	def read_gravity(self):
		results = {}
		for name, port in self.ports.items():
			for i in range(3):
				response = port.read(8)
				print(binascii.b2a_hex(response))
				ok, gravity = self.convert_gravity(response)
				if not ok:
					if i < 2:
						print(gravity)
						continue
					else:
						return ApiResult().wrong(gravity, name)
				else:
					results[name] = gravity
					break
		return ApiResult().right(results)

	"""
	把串口读到的原始二进制数据，转换为实际的重力值数据
	数据样例为： 2B 20 33 33 34 39 0D 0A
	其中，第一位是标示位2B，第2-6位为重力数据，最后两位是校验位	0D 0A
	"""
	def convert_gravity(self, binary):
		if len(binary) != 8:
			return False, ApiResult.Code.LEN
		# if binary[0] != b'\x2B':
		# 	return False, ApiResult.Code.MARK
		# if binary[6:8] != b'\x0d\x0d':
		# 	return False, ApiResult.Code.CHECK

		# print(type(binary))
		raw = self.convert_binary(binary[1:6])

		result = raw - self.offset

		# 原始重力值在10千克位上有一个跃迁差量（从20直接到31）
		if result >= self.bias:
			result = result - self.bias

		return True, result

	"""
	把原始二进制数据，转换为对应的十进制数值
	数据样例为： 20 33 33 34 39
	从右到左依次为"个十百千万"，单位是克
	"""
	def convert_binary(self, binary):
		result = 0
		binary = str(binary, encoding="utf-8")
		for data in binary:
			result = result * self.decimal + struct.unpack(self.format, str.encode(data))[0]
		return result


# class CodeEnum(Enum):
# 	OK
# 	LEN
# 	MARK
# 	CHECK

class ApiResult:
	# Code = Enum('OK', 'LEN', 'MARK', 'CHECK')
	# Msg = Enum('', '重力传感器数据位不是8位', '重力传感器数据标示位错误', '重力传感器数据校验位错误')

	Code = Enum('Code', 'OK LEN MARK CHECK')
	Msg = {
		Code.LEN: '重力传感器数据位不是8位',
		Code.MARK: '重力传感器数据标示位错误',
		Code.CHECK: '重力传感器数据校验位错误'
	}
	# Msg = Enum('Msg', 'nil 重力传感器数据位不是8位 重力传感器数据标示位错误 重力传感器数据校验位错误')

	def __init__(self):
		self.success = True
		self.code = 0
		self.errorMsg = ""
		self.data = []

	def right(self, data):
		self.data = data
		return self

	def wrong(self, code, name):
		self.success = False
		self.code = code.value
		self.errorMsg = '重力传感器%s错误： %s' % (name, self.Msg[code])
		return self


util = GravityUtils()
# # print util.convert_binary(b'\x20\x20\x20\x20\x30')
print(str(datetime.datetime.now()))
print(util.read_gravity().__dict__)
print(str(datetime.datetime.now()))

# Code = Enum('Code', 'OK LEN MARK CHECK')
# Msg = Enum('Msg', 'nil 重力传感器数据位不是8位 重力传感器数据标示位错误 重力传感器数据校验位错误')
# print(list(Msg))
# print(Code.OK.value)
