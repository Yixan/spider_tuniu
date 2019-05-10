# //*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li[2]/
# //*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li[40]/a
# //*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li[2]/a
# //*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li[2]/a

# -*- coding: utf-8 -*-
import scrapy
from scrapy import spiders, Request
from scrapy import Selector, spiders
import json
from trip.items import AreaItem
class AreaSpider(scrapy.Spider):
    name = 'area'
    start_urls = ['http://menpiao.tuniu.com/cat_0_0_0_0_0_0_1_1_1.html']
    def parse(self, response):
        sel = Selector(response)
        item = AreaItem()
        #item_list=[]
        for i in range(2,41):
            if  sel.xpath('//*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li['+i.__str__()+']/a') is None:
                break
            item['name'] = sel.xpath('//*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li['
                                     +i.__str__()+']/a/text()').extract()[0]
            str = sel.xpath('//*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li['
                            +i.__str__()+']/a/@href').extract()[0]
            item['number']=str.split('_')[1]
            yield item

        # nextPage=sel.xpath('//*[@id="niuren_list"]/div[4]/div/a[last()-1]/@href').extract()[0]
        # print("下一页的url:"+nextPage)
        # yield Request(url=nextPage,callback=self.parse)