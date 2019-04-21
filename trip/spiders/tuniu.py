# -*- coding: utf-8 -*-
import scrapy
from scrapy import spiders, Request
from scrapy import Selector, spiders
import json
from trip.items import TripItem

class TuniuSpider(scrapy.Spider):
    name = 'tuniu'
    #allowed_domains = ['tuniu.com']
    start_urls = ['http://menpiao.tuniu.com/cat_0_0_0_0_0_0_1_1_1.html']
    print("进行到：0")
    #api = 'http://trips.tuniu.com/travels/index/ajax-list?sortType=1&page={page}&limit=10'

    def parse(self, response):
        sel = Selector(response)
        item = TripItem()
        #item_list=[]
        for i in range(1,11):
            if sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/h3/a/text()') is None:
                break
            item['name'] = sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/h3/a/text()').extract()[0]
            if sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/p[1]/strong/text()') is None:
                item['satis'] ='无'
            else:item['satis'] =sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/p[1]/strong/text()').extract()[0]
            item['pos'] = sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/p[2]/text()').extract()[0]
            item['nextPage'] = sel.xpath('//*[@id="niuren_list"]/div[4]/div/a[10]@herf').extract()[0]
            yield item

        nextPage=sel.xpath('//*[@id="niuren_list"]/div[4]/div/a[last()-1]/@href').extract()[0]
        print("下一页的url:"+nextPage)
        yield Request(url=nextPage,callback=self.parse)

