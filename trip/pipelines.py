# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import DButil

class ScenicPipeline(object):
    def process_item(self, item, spider):
        str = "INSERT INTO scenic(name, pos, satis,province,city,note," \
              "introduction,comment,transport) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s') "
        note="".join(item['note'])
        intro="".join(item['introduction'])
        trans="".join(item['transport'])
        sql = str % (item['name'], item['pos'], item['satis'], item['province'],
                     item['city'],  note, intro, item['comment'],
                     trans)
        DButil.execute(sql)
        return item
class AreaPipeline(object):
    def process_item(self, item, spider):
        print(item['name']+","+item['number'])
        sql = "INSERT INTO area(area, number) VALUES (" + "'" + item['name'] + "'" + ", " + "'" + item['number']+ "'" + ")"
        DButil.execute(sql)
        return item

class CityPipeline(object):
    def process_item(self, item, spider):
        print(item['name']+","+item['number']+item['area'])
        sql = "INSERT INTO city(city, number, area) VALUES (" + "'" + item['name'] + "'" + ", " + "'" + item['number']+ "'" + ", " + "'"+item['area']+ "'"+ ")"
        DButil.execute(sql)
        return item
    pass
