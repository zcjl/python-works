# coding:utf-8

import serial
import time
import binascii


class GravityUtils:

    def __init__(self):
        # 打开端口
        self.port = serial.Serial(port='/dev/ttyUSB0', timeout=0.03)
        self.send_cmd = b'\xE5\x96\x02\x03\x02\xA0\x00\x01\x85\xA3\x1B'

    def read_gravity(self):
        self.port.write(self.send_cmd)
        response = self.port.readall()
        print(len(response))
        print(binascii.b2a_hex(response))


begin = time.time()
print(GravityUtils().read_gravity())
end = time.time()
print('调用耗时：%f\n\n' % (end - begin))
