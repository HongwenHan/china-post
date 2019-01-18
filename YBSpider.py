# -*- conding: utf-8 -*-

import mining_utils as util
import pymongo
from bs4 import BeautifulSoup
import time


conn = pymongo.MongoClient('mongodb://localhost:27017/', connect=False)

db = conn.youbian  # 连接数据库名
youbian_db = db.youbian


base_url = 'http://www.yb21.cn'


def getDCUrls(dc_content):
    soup = BeautifulSoup(dc_content[1], 'html.parser')
    table_as = soup.find(cellspacing=10).find_all('a')
    arrs = []
    for table_a in table_as:
        arr = {}
        arr_href = base_url + table_a['href']
        arr_name = table_a.get_text()
        arr['name'] = arr_name
        arr['href'] = arr_href
        arrs.append(arr)
    return arrs


def getTotalCity(content):
    print('get all city urls start ')
    soup = BeautifulSoup(content[1], 'html.parser')
    citys = soup.find_all(class_='citysearch')
    city_urls = []
    n = 0
    for city in citys:
        city_name = city.h1.get_text()
        city_post = {}
        city_post['city_name'] = city_name
        city_post['district_county'] = []
        district_countys = city.ul.find_all('a')
        for dc in district_countys:
            district_county = {}
            district_county['dc_name'] = dc.get_text()
            dc_url = base_url + dc['href']
            district_county['dc_url'] = dc_url
            dc_content = util.getContentRequest(dc_url)
            time.sleep(1)
            district_county['dc_urls'] = getDCUrls(dc_content)
            city_post['district_county'].append(district_county)
        youbian_db.insert(city_post)
        # city_urls.append(city_post)
        n += 1
        print(n)
    print('get all city urls end ')
    # return city_urls


def iterationCity():
    for city in youbian_db.find({}):
        district_countys = city['district_county']
        for dc in district_countys:
            arr_urls = dc['dc_urls']
            for arr_url in arr_urls:
                href = arr_url['href']
                arr_content = util.getContentRequest(href)
                soup = BeautifulSoup(arr_content[1], 'html.parser')
                time.sleep(1)



def SpiderYB():
    # list_content = util.getContentRequest(base_url)
    # getTotalCity(list_content)
    iterationCity()


if __name__ == '__main__':
    SpiderYB()
