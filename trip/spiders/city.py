# -*- coding: utf-8 -*-
# //*[@id="niuren_list"]/div[1]/div/div[3]/dl/dd/ul/li[2]/a
import scrapy
from scrapy import spiders, Request
from scrapy import Selector, spiders
import json
from trip.items import CityItem
class CitySpider(scrapy.Spider):
    name = 'city'

    custom_settings = {
        'ITEM_PIPELINES': {
            'trip.pipelines.CityPipeline': 100,
        }
    }

    start_urls = ['http://menpiao.tuniu.com/cat_0_0_0_0_0_0_1_1_1.html']
    def parse(self, response):
        sel = Selector(response)
        for i in range(2,41):
            if  sel.xpath('//*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li['+i.__str__()+']/a') is None:
                break
            str = sel.xpath('//*[@id="niuren_list"]/div[1]/div/div[2]/dl/dd/ul/li['
                            +i.__str__()+']/a/@href').extract()[0]
            link='http://menpiao.tuniu.com'+str
            yield Request(link, callback=self.parse_author)
    def parse_author(self, response):
        sel = Selector(response)
        item = CityItem()
        for i in range(2,100):
            if sel.xpath('//*[@id="niuren_list"]/div[1]/div/div[3]/dl/dd/ul/li['+i.__str__()+']/a/text()') == None:
                print('--------------------------结束----------------------------------')
                break
            item['name']=sel.xpath('//*[@id="niuren_list"]/div[1]/div/div[3]/dl/dd/ul/li['
                                   +i.__str__()+']/a/text()').extract()[0]
            str=sel.xpath('//*[@id="niuren_list"]/div[1]/div/div[3]/dl/dd/ul/li['
                                   +i.__str__()+']/a/@href').extract()[0]
            print(str.split('_')[2])
            item['number']=str.split('_')[2]
            print(str.split('_')[1])
            item['area']=str.split('_')[1]
            yield item


