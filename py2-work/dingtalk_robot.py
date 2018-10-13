#coding=utf-8

from fake_useragent import UserAgent
import requests
import json

ua=UserAgent()
headers = {
	"User-Agent":ua.random,
	"Content-Type":"application/json"
}

# url = "https://oapi.dingtalk.com/robot/send?access_token=9248356d34c0a911abecf5fccfc2ad171a0cd96f24ca95d2e8129afa7a2e3e47"
url = "https://oapi.dingtalk.com/robot/send?access_token=d7b69f9d202715a10edd49985180b3c73c4f4792f4930b79f5585e1c3c936024"

msg = json.dumps(
{
	"msgtype": "text", 
	"text": {
		"content": "大家好，我是魔柜守护者小柜子，随时替大家值守在一线，请多指教,  @18913191123"
	}, 
	"at": {
		"atMobiles": ["18913191123"], "isAtAll": "false"
	}
}
)

resp = requests.post(url, data=msg, headers=headers)
print resp.text


msg = json.dumps(
{
	"msgtype": "link", 
	"link": {
		"title": "奇点云官网",
		"text": "这里是奇点云官网的文字介绍",
		"picUrl": "",
		"messageUrl": "https://www.startdt.com/"
	}
}
)

# resp = requests.post(url, data=msg, headers=headers)
# print resp.text


msg = json.dumps(
{
	"msgtype": "markdown", 
	"markdown": {
		"title": "杭州天气",
		"text": "#### 杭州天气  \n > 9度，@13750849886 西北风1级，空气良89，相对温度73%\n\n > ![screenshot](http://i01.lw.aliimg.com/media/lALPBbCc1ZhJGIvNAkzNBLA_1200_588.png)\n  > ###### 10点20分发布 [天气](http://www.thinkpage.cn/) "
	}, 
	"at": {
		"atMobiles": ["13750849886"],
		"isAtAll": "false"
	}
}
)

# resp = requests.post(url, data=msg, headers=headers)
# print resp.text