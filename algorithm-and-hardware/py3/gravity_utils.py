# coding:utf-8

import serial
import time
import binascii
from enum import Enum


class GravityUtils:
    Code = Enum('Code', 'MARK CHECK')

    def __init__(self):
        # 打开端口
        self.ports = {
            # "g_sensor_1": serial.Serial(port='/dev/tty.usbserial-FT2J03F3A', timeout=0.04),
            # "g_sensor_2": serial.Serial(port='/dev/tty.usbserial-FT2J03F3B', timeout=0.04),
            # "g_sensor_3": serial.Serial(port='/dev/tty.usbserial-FT2J03F3C', timeout=0.04),
            # "g_sensor_4": serial.Serial(port='/dev/tty.usbserial-FT2J03F3D', timeout=0.04)
            # "g_sensor_1": serial.Serial(port='/dev/ttyUSB1', timeout=0.03),
            # "g_sensor_2": serial.Serial(port='/dev/ttyUSB3', timeout=0.03),
            # "g_sensor_3": serial.Serial(port='/dev/ttyUSB0', timeout=0.03),
            # "g_sensor_4": serial.Serial(port='/dev/ttyUSB2', timeout=0.03)
        }
        self.offset = 100  # 原始重力值读数的位移差量 -> 20 33 33 30 34

    """
    通过USB转串口，读取重力感应器重力值数据	
    """
    def read_gravity(self):
        results = {}
        for name, port in self.ports.items():
            while True:
                port.flush()
                response = port.read(8)
                print('read data from %s, result is %s' % (name, binascii.b2a_hex(response)))
                if len(response) == 0 or response[:1] != b'\x2B':
                    continue
                if len(response) < 8:
                    response = bytearray(response)
                    response.extend(port.read(8))

                ok, gravity = self.convert_gravity(response)
                if not ok:
                    print(gravity)
                    continue
                else:
                    results[name] = gravity
                    break
        return {"success": True, "data": results}

    """
    把串口读到的原始二进制数据，转换为实际的重力值数据
    数据样例为： 2B 20 33 33 34 39 0D 0A
    其中，第一位是标示位2B，第2-6位为重力数据，最后两位是校验位	0D 0A (回车换行符)
    """
    def convert_gravity(self, binary):
        if binary[:1] != b'\x2B':
            return False, self.Code.MARK
        if binary[6:8] != b'\x0D\x0A':
            return False, self.Code.CHECK

        raw = self.convert_binary(binary[1:6])
        result = raw - self.offset

        return True, result


    """
    把原始二进制数据，转换为对应的十进制数值
    数据样例为： 20 33 33 34 39
    从右到左依次为"个十百千万"，单位是克
    """
    def convert_binary(self, binary):
        result = ''
        for data in binary:
            result = result + chr(data)
        return int(result)


begin = time.time()
print(GravityUtils().read_gravity())
end = time.time()
print('调用耗时：%f\n\n' % (end - begin))
