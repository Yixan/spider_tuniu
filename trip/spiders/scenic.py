# -*- coding: utf-8 -*-
import scrapy
from scrapy import spiders, Request
from scrapy import Selector, spiders
import json
from trip.items import ScenicItem
from scrapy_splash import SplashRequest
import copy

class ScenicSpider(scrapy.Spider):
    name = 'scenic'
    myItem=None
    rank=1
    custom_settings = {
        'ITEM_PIPELINES': {
            'trip.pipelines.ScenicPipeline': 100,
        }
    }
    start_urls = ['http://menpiao.tuniu.com/cat_0_0_0_0_0_0_1_1_144.html']
    #allowed_domains = ['tuniu.com']


    print("进行到：0")
    #api = 'http://trips.tuniu.com/travels/index/ajax-list?sortType=1&page={page}&limit=10'

    def parse(self, response):
        sel = Selector(response)

        #item_list=[]
        for i in range(1,11):
            print('------------------------------i='+i.__str__()+'--------------------------------------------')
            if sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/h3/a/text()') is None:
                break
            item = ScenicItem()
            item['name'] = sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/h3/a/text()')\
                .extract_first()
            if sel.xpath(
                    '//*[@id="niuren_list"]/div[3]/div/ul/li[' + i.__str__() + ']/p[1]/strong/text()')\
                    .extract_first() is None:
                item['satis'] = '无'
            else:
                item['satis'] =sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/p[1]/strong/text()').extract()[0]
            if sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/p[2]/text()').extract_first() == None:
                item['pos']='无'
            else:
                item['pos'] = sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/p[2]/text()')\
            .extract_first()
            if sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/h3/span[1]/a[2]/text()').extract()== None:
                item['province'] = sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['
                                             +i.__str__()+']/h3/span[1]/a/text()').extract()[0]
                item['city']='无'
            else:
                item['province']=sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['
                                           +i.__str__()+']/h3/span[1]/a[1]/text()').extract_first()
                item['city'] = sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['
                                         ''+i.__str__()+']/h3/span[1]/a[2]/text()').extract_first()
            if sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['
                                                              +i.__str__()+']/h3/a/@href').extract() == None:
                item['link']='无'
            else:
                item['link']='http://menpiao.tuniu.com'+sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['
                                                              +i.__str__()+']/h3/a/@href').extract()[0]
            print(item['link'])
            item['seriald']=sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['
                                                              +i.__str__()+']/h3/a').extract()[0].split("_")[1]
            if sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['+i.__str__()+']/p[1]/span/strong') \
                    .extract_first() is None:
                item['comment'] =0
            else:
                item['comment']=sel.xpath('//*[@id="niuren_list"]/div[3]/div/ul/li['

                                          +i.__str__()+']/p[1]/span/strong') .extract_first()


            # yield item
            yield SplashRequest(url=item['link'],meta={'item': item}, args={'wait': '0.5'},callback=self.parse_all)
        nextPage=sel.xpath('//*[@id="niuren_list"]/div[4]/div/a[last()-1]/@href').extract()[0]
        print("下一页的url:"+'http://menpiao.tuniu.com/'+nextPage)
        yield Request(url='http://menpiao.tuniu.com/'+nextPage,callback=self.parse)

    def parse_all(self,response):
        # print('------------------------------i=' + response + '--------------------------------------------')
        item = response.meta['item']
        sel = Selector(response)
        item['note']=sel.xpath('/html/body/div[2]/div/section/div/div[2]/div[2]').extract()
        item['introduction']=sel.xpath('/html/body/div[2]/div/div[2]/div[3]').extract()
        item['transport']=sel.xpath('/html/body/div[2]/div/div[2]/div[4]').extract()
        print(item['name']+'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('------------------------------------------------结束---------------------------------------------------------------------------')
        yield  item



# /html/body/div[2]/div/div[2]/div[2]/div[2]#
# /html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]
# /html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]
# /html/body/div[2]/div/section/div/div[2]/div[1]/h3/p