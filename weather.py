#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib2, re

class HtmlParser(HTMLParser):

	def __init__(self):
		self.data = ''
		self.readingdata = 0
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		if tag == 'td':
			self.readingdata = 1

	def handle_data(self, chars):
		if self.readingdata:
			self.data += '\n' + chars

	def handle_endtag(self, tag):
		if tag == 'td':
			self.readingdata = 0

	def cleanse(self):
		self.data = re.sub('\s+', ' ', self.data)

	def getdata(self):
		self.cleanse()
		return self.data

class Weather(object):

	def halfDay(self, data):
		data[1] = data[2]
		data[2] = data[4]
		return data[:3] + ['\n']

	def wholeDay(self, data):
		data[1] = data[2] + ' --> ' + data[8]
		data[2] = data[10] + ' --> ' + data[4]
		return data[:3] + ['\n']

	def forecast(self):
		# this url is a place where you want to know the weather forecast
		url = "http://www.weather.com.cn/html/weather/101210101.shtml"
		req = urllib2.Request(url)
		conn = urllib2.urlopen(req)

		htmlParser = HtmlParser()
		htmlParser.feed(conn.read())
		weather = htmlParser.getdata().split()

		forecast = []
		# 用‘日‘来分割
		tag	= [weather.index(i) for i in weather if '\xe6\x97\xa5' in i]
		for i in range(7):
			if i == 6:
				data = weather[tag[i]:]
			else:
				data = weather[tag[i]:tag[i+1]]

			if len(data) < 8:
				forecast += self.halfDay(data)
			else:
				forecast += self.wholeDay(data)

		return '\n'.join(forecast).decode("UTF-8").encode("GBK")
