# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re


class TripPipeline(object):
    def process_item(self, item, spider):
        with open("my_out.txt", 'a', encoding="utf-8") as fp:
            try:
                fp.write(item['name'] + '\t' + item['satis'] + '\t' + item['pos'] + '\n')

            except UnicodeEncodeError as err:  # 使用as将异常对象，并将其赋值给一个标识符
                print('File Error:' + str(err))  # ‘+’用于字符串直接的连接

            finally:
                pass
        return item
