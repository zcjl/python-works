# coding:utf-8

import serial
import struct
import binascii
import datetime


class Ser(object):
    def __init__(self):
        # 打开端口
        self.ports = [
            serial.Serial(port='/dev/tty.usbserial-AC01NPYX', timeout=0.04),
            serial.Serial(port='/dev/tty.usbserial-AC01NPYX', timeout=0.04),
            serial.Serial(port='/dev/tty.usbserial-AC01NPYX', timeout=0.04),
            serial.Serial(port='/dev/tty.usbserial-AC01NPYX', timeout=0.04)]

    # 发送指令的完整流程
    def send_cmd(self, cmd):
        res = []
        for port in self.ports:

            # print str(datetime.datetime.now())
            port.write(cmd)
            # print str(datetime.datetime.now())
            response = port.readall()
            # print str(datetime.datetime.now())

            print len(response)
            print binascii.b2a_hex(response)

            result = struct.unpack(">h", response[3:5])[0]
            res.append(result)

        return res


# 所发十六进制字符串20 03 04 00 00 00 02 C2 BA
send_cmd = [0x20, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC2, 0xBA]
ser = Ser()
print str(datetime.datetime.now())
print ser.send_cmd(send_cmd)
print str(datetime.datetime.now())