# coding:utf-8

import serial.tools.list_ports

plist = list(serial.tools.list_ports.comports())

if len(plist) <= 0:
    print("没有发现端口!")
else:
    print(plist)
    plist_0 = list(plist[0])
    print(plist_0)
    serialName = plist_0[0]
    print(serialName)
    serialFd = serial.Serial(serialName, 9600, timeout=60)
    print("可用端口名>>>", serialFd.name)