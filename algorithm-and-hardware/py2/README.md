## binary_converter.py
* 将串口调试读取的二进制数据，转换为对应的重量读数，数据写入csv的代码
* 源数据格式示例为20 03 04 13 85 00 00 DE 5C
* 其中前三位为标示位，4、5、6、7为数据位，8、9为校验位

## check_status.py
* 检查魔柜算法状态的监控脚本代码
* 每隔2秒检查一次状态，连续10次error则通过钉钉机器人发出告警
* 依赖requests包

## dingtalk_robot.py
* 钉钉机器人测试代码
* 依赖requests、fake_useragent包

## dump_log.py
* 检查重力服务读数并记录日志的代码
* 每隔5秒调用重力服务数据，并通过滚动日志写入文件（test.log）
* 依赖requests、logging包

## merge_log.py
* 顺序合并上述脚本生成的日志文件，并写入csv供后续分析的代码

## list_ports.py
* 查找并显示系统可用串口端口（comports）的代码
* 依赖serial、pyserial包

## gravity_server.py
* 基于串口转USB读取重力感应器数据，并转换成json提供服务的代码
* 依赖serial、pyserial包