import requests
import re
import json
from collections import OrderedDict
import pymysql
#import pymongo
from multiprocessing import Pool
from config import *
from urllib.parse import urlencode
from requests.exceptions import RequestException
import pymysql
db = pymysql.connect(host='62.234.52.40', port=3306, user='douban',
                         password='CYfY9HPbz0d5SWmO', db='crawl')
cursor = db.cursor()
sql='alter table remark AUTO_INCREMENT=1;'
cursor.execute(sql)
db.commit()
# 获取到某个城市的总的旅游线路的某一页的HTML页面
def get_oneHTML_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

#使用正则表达式解析出 某个城市的总的旅游线路的某一页的HTML页面里面的所有链接、标题、评论数
def prase_one_page(html):
    pattren= re.compile('<li>.*?theinfo">.*?href="(.*?)".*?>.*?title="(.*?)">.*?<em>(.*?)</em>.*?comment-satNum">.*?<i>(.*?)</i>.*?person-num"><i>(.*?)</i>.*?person-comment"><i>(.*?)</i>.*?</a>.*?</li>', re.S)
    items=re.findall(pattren, html)
    #print(items)
    for item in items:
        yield {
            'linked':item[0],
            'title':item[1],
            'price':item[2],
            'satisfaction':item[3],
            'totalnumber':item[4],
            'commentnumber':item[5]
        }


# 做测试用
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()
# 使用mongodb时需要加载一个配置文件，内容如下
# GROUP_START=1
# GROUP_END=3
# MONGO_URL = 'localhost'
# MONGO_DB = 'tuniu'
# MONGU_TABLE = 'remark'
#
# def save_to_mongodb(result):
#     if db[MONGU_TABLE].insert(result):
#         print('存储到mongodb成功', result)
# 根据请求参数得到评论页的url，然后根据url得到评论页面的内容
def get_remark_page(productId,productType,page):
    data={
        'productId': productId,
        'productType': productType,
        'page':page
    }
    url='http://www.tuniu.com/papi/product/remarkList?'+urlencode(data)
    if (productId == '20545063'):
        print(url)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求评论页出错')
        return None

# 把每条评论的详情写到result.txt这个文件中
# def write_to_file(dict):


# 使用正则表达式解析出每条评论的id，评论内容，评论者的昵称
def prase_remark(html):
    pattern=re.compile('{"id":(.*?),"adultNum".*?"productName":"(.*?)","specSvalue".*?"remarkTime":"(.*?)","remarkChannelName":"(.*?)","compGrade".*?"productCategoryName":"(.*?)","extendTime".*?"compTextContent":{"gradeLevel":0,"dataId":2,"dataIvalue":0,"dataSvalue":"(.*?)","notes".*?"nickname":"(.*?)".*?"}}', re.S)
    items = re.findall(pattern,html)
    #print(items)
    for itemold in items:
        tup = ('','')
        item = itemold+tup
        dict=OrderedDict()
        dict={ "remarkid":item[0],
            "productName":item[1],
            "remarkTime":item[2],
            "remarkChannelName":item[3],
            "productCategoryName":item[4],
            "remark":item[5],
            "nickname":item[6],
            "polarity":item[7],
            "level":item[8]}
        sql = "INSERT INTO remark(remarkid, product,time,remarkChannelName,roductCategoryName,nickname，remark)" \
              " VALUES('%s','%s','%s','%s','%s','%s','%s')"%(item[0],item[1],
                item[2],item[3],item[4],item[6],item[5])
        cursor.execute(sql)
        db.commit()
        print('执行完毕')
        yield{
            'remarkid':item[0],
            'productName':item[1],
            'remarkTime':item[2],
            'remarkChannelName':item[3],
            'productCategoryName':item[4],
            'remark':item[5],
            'nickname':item[6],
            'polarity':item[7],
            'level':item[8]
        }


def get_remark(prams):
    lists=[]
    # print(page)
    productId = prams[0]
    #print(productId)
    groups = prams[1:]
    for group in groups:
        html = get_remark_page(productId, 1, group)
        # print(html)
        dict=prase_remark(html)
        for item in prase_remark(html):
            lists.append(item)
        print(lists)
    print(lists)
    # write_to_file(dict)

    #save_to_mysql(lists)
    return lists

def getproduct_id(html):
    product_ids = []
    for item in prase_one_page(html):
        url1 = item.get('title')
        url2 = item.get('linked')
        print(url2, 'test', url1)
        newurl = url2 + 'test' + url1
        # print(html2)
        pattern02 = re.compile('tour/(.*?)test')
        items = re.findall(pattern02, newurl)
        product_ids.extend(items)
    return product_ids
# def save_to_mysql(lists):
#     db = pymysql.connect(host="localhost", user="root", password="123456", db="tuniu", charset="utf8mb4")
#     cursor = db.cursor()
#     for i in lists:
#         sql = "INSERT INTO remark(remarkid,productName,remarkTime,remarkChannelName,productCategoryName,remark,nickname,polarity,level) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (i["remarkid"], i["productName"], i["remarkTime"], i["remarkChannelName"], i["productCategoryName"], i["remark"],i["nickname"],i["polarity"],i["level"])
#         # print(sql)
#         try:
#             cursor.execute(sql)
#             db.commit()
#             # print(i["productName"] + " is success")
#         except:
#             print("$&")
#             db.rollback()
#     db.close()

def main():
    # db = pymysql.connect(host="localhost", user="root", password="123456", db="tuniu", charset="utf8mb4")
    # cursor = db.cursor()
    # cursor.execute("DROP TABLE IF EXISTS remark")
    # createTab = """CREATE TABLE remark(
    #                         id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #                         remarkid VARCHAR(100) NOT NULL,
    #                         productName VARCHAR(500) NOT NULL,
    #                         remarkTime VARCHAR(100) NOT NULL,
    #                         remarkChannelName VARCHAR(250) NOT NULL,
    #                         productCategoryName VARCHAR(500) NOT NULL,
    #                         remark VARCHAR(2000) NOT NULL,
    #                         nickname VARCHAR(100),
    #                         polarity VARCHAR(200),
    #                         level VARCHAR(200)
    #                     )"""
    # cursor.execute(createTab)
    # db.close()
    prams = []
    # citys = ['g906', 'g3300','g414','g700']
    citys = ['g906']
    for city in citys:
        for i in range(1,2):
            #获取到某个城市的旅游线路的某一页的地址
            url = 'http://www.tuniu.com/'+str(city)+'/tours-nj-0/list-h0-i-j0_0/' + str(i) + '/'
            print(url)
            html=get_oneHTML_page(url)
            for productId in getproduct_id(html):
                #print(productId)
                groups = [x for x in range(GROUP_START, GROUP_END + 1)]
                pram =[]
                pram.append(productId)
                groups = map(str, groups)
                pram.extend(groups)
                prams.append(pram)
    pool = Pool()
    pool.map(get_remark, prams)

if __name__ == '__main__':
    main()