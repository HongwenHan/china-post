# -*- conding: utf-8 -*-

import mining_utils as util
import pymongo
from bs4 import BeautifulSoup
import time
import random


conn = pymongo.MongoClient('mongodb://localhost:27017/', connect=False)

db = conn.youbian  # 连接数据库名
youbian_db = db.youbian


base_url = 'http://www.yb21.cn'

proxys = util.getProxys()


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
    # city_urls = []
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


def getPostInfosAndUpdate(city_id, arr_name, index_dc, index_arr, soup):
    table_as = soup.find(cellpadding=2).find_all('a')
    posts = []
    for table_a in table_as:
        post = {}
        info_url = base_url + table_a['href']
        post_name = table_a.get_text()
        post['post_code'] = post_name
        info_content = util.getContentRequest(info_url)
        if not info_content:
            time.sleep(60)
            posts = []
            break
        time.sleep(random.randrange(2, 3))
        soup_info = BeautifulSoup(info_content[1], 'html.parser')
        td_infos = soup_info.find(class_='lh22').find_all('td')
        infos = []
        for info in td_infos:
            info_text = info.get_text().rstrip('\n')
            info_text = "".join(info_text.split())
            if not info_text or post_name in info_text:
                continue
            infos.append(info_text)
        post['infos'] = infos
        posts.append(post)
    if len(posts) > 0:
        youbian_db.update({'_id': city_id, 'district_county.dc_urls.name': arr_name}, {
            '$set': {'district_county.' + str(index_dc) + '.dc_urls.' + str(index_arr) + '.post': posts}})
    # return posts


def iterationCity():
    index_city = 0
    for city in youbian_db.find({}):
        district_countys = city['district_county']
        city_id = city['_id']
        index_dc = 0
        for dc in district_countys:
            if index_city == 18 or index_city == 20:
                continue
            arr_urls = dc['dc_urls']
            index_arr = 0
            for arr_url in arr_urls:
                href = arr_url['href']
                arr_name = arr_url['name']
                if 'post' in arr_url:
                    index_arr += 1
                    print(index_city, index_dc, index_arr, time.time())
                    continue
                arr_content = util.getContentRequest(href)
                if not arr_content:
                    time.sleep(60)
                    break
                soup = BeautifulSoup(arr_content[1], 'html.parser')
                getPostInfosAndUpdate(
                    city_id, arr_name, index_dc, index_arr, soup)
                index_arr += 1
                print(index_city, index_dc, index_arr, time.time())
            index_dc += 1
        index_city += 1


def SpiderYB():
    # list_content = util.getContentRequest(base_url)
    # getTotalCity(list_content)
    iterationCity()


if __name__ == '__main__':
    SpiderYB()
