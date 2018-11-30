# -*- coding: utf-8 -*-
import scrapy
from Tengxun.items import TengxunItem

class TengxunSpider(scrapy.Spider):
	name = 'tengxun'
	allowed_domains = ['hr.tencent.com']

	# 定义1一个基准的url，方便后期拼接290个url
	url = "https://hr.tencent.com/position.php?&start="
	start = 0	
	start_urls = [url + str(start)]


	# parse函数是第一次从start_urls中初始URL发情求
	# 得到响应后必须要调用的函数，但是别的请求可以不走这个函数，可以自定义回调函数．
	def parse(self, response):
		for i in range(0, 2891, 10):
			# scrapy.Request()
			# 把290页的url给调度器入队列，然后出队列给下载器
			yield scrapy.Request(self.url + str(i), callback = self.parseHtml)
	
	
	def parseHtml(self, response):
		# 每个职位的节点对象列表
		baseList = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')
		for base in baseList:
			item = TengxunItem()
			item["zhName"] = base.xpath('./td[1]/a/text()').extract()[0]
			item["zhLink"] = base.xpath('./td[1]/a/@href').extract()[0]
			resType = base.xpath('./td[2]/text()').extract()
			if resType:
				item["zhType"] = resType[0]
			else:
				item["zhType"] = "无"
			item["zhNum"] = base.xpath('./td[3]/text()').extract()[0]
			item["zhAddress"] = base.xpath('./td[4]/text()').extract()[0]
			item["zhTime"] = base.xpath('./td[5]/text()').extract()[0]
			
			yield item
