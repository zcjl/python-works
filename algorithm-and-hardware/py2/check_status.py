#coding=utf-8

import time
import json
import requests
import threading


counter = 0
def countErrors():
	global counter
	counter += 1

def resetCounter():
	global counter
	counter = 0


def check():
	if True:
		threading.Timer(2, check).start()

	url = "http://192.168.70.200:8301/status"
	while True:
	    try:
	        resp = requests.get(url, timeout=5)
	        if not resp.status_code == requests.codes.ok:
	        	return

	        resp = resp.json()
	        break
	    except:
	        pass

	print json.dumps(resp, ensure_ascii=False)
	succ = resp["success"]
	if not succ:
		reportError(resp)
		return

	statusList = resp["status_list"]
	for layer in statusList:
		status = layer["status"]
		if "error" in status:
			reportError(resp)
			return

	resetCounter()


REPORT_INTERVAL = 10
def reportError(resp):
	countErrors()
	if counter >= REPORT_INTERVAL:
		sendToDingtalk(resp)
		resetCounter()


def sendToDingtalk(resp):

	headers = {
		"Content-Type":"application/json"
	}
	# robotUrl = "https://oapi.dingtalk.com/robot/send?access_token=d7b69f9d202715a10edd49985180b3c73c4f4792f4930b79f5585e1c3c936024"
	robotUrl = "https://oapi.dingtalk.com/robot/send?access_token=9248356d34c0a911abecf5fccfc2ad171a0cd96f24ca95d2e8129afa7a2e3e47"

	msg = json.dumps(
	{
		"msgtype": "text", 
		"text": {
			"content": '%s，魔柜已经持续%d次状态错误，错误信息如下\n%s\n' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), counter, resp)
		}, 
		"at": {
			"atMobiles": [],
			"isAtAll": "true"
		}
	}
	)

	resp = requests.post(robotUrl, data=msg, headers=headers)
	print resp.text

check()