# coding:utf-8

import serial
import struct
import binascii
import datetime
import time

# 所发十六进制字符串010591F50000F104
cmd = [0x20, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC2, 0xBA]

class Ser(object):
    def __init__(self):
        # 打开端口
        self.ports = [serial.Serial(port='/dev/tty.usbserial-AC01NPYX', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.04)]

    # 发送指令的完整流程
    def send_cmd(self, cmd):
        res = []
        for port in self.ports:

            print str(datetime.datetime.now())
            port.write(cmd)
            print str(datetime.datetime.now())
            response = port.readall()
            print str(datetime.datetime.now())

            print len(response)
            print binascii.b2a_hex(response)

            result = struct.unpack(">h", response[3:5])[0]
            res.append(result)
            # print result

        # response = self.convert_hex(response)
        return res

    # 转成16进制的函数
    def convert_hex(self, string):
        res = []
        result = []
        for item in string:
            res.append(item)
        for i in res:
            result.append(hex(i))
        return result


ser = Ser()
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print ser.send_cmd(cmd)