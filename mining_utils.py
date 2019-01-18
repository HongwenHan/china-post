# -*- conding: utf-8 -*-

import requests  # 导入requests库
import random
import time
import urllib
from urllib import parse
from urllib import request

headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
           "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
           "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
           "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
           "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
           "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
           "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
           'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
           'Opera/9.25 (Windows NT 5.1; U; en)',
           'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
           'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
           'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
           "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
           "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
           ]


def getProxys():
    datas = []
    for x in range(10):
        r = requests.get(
            'https://h.wandouip.com/get/ip-list?pack=0&num=20&xy=1&type=2&lb=\r\n&mr=1&')
        r.encoding = 'utr-8'
        proxy_json = r.json()
        data = proxy_json['data']
        datas.append(data)

    proxy_list = []
    for data in datas:
        for ip_info in data:
            ip = ip_info['ip']
            port = ip_info['port']
            proxy_list.append(ip + ':' + str(port))

    return proxy_list


def openlink(self_hand, link):  # 重复请求
    maNum = 1
    while maNum <= 10:
        sleep_time = round(random.randint(5, 10) / 10, 2)
        print(sleep_time)
        time.sleep(sleep_time)
        try:
            req = urllib.request.Request(link, headers=self_hand)
            try:
                response = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                print('urllib.error.HTTPError except:', e)
                time.sleep(5)
                response = urllib.request.urlopen(req)
            text = ''
            try:
                text = response.read().decode('gbk')
            except UnicodeDecodeError as e:
                print('except:', e)
            maNum = maNum + 1
            return text
        except:
            if maNum < 10:
                maNum = maNum + 1
                continue
            else:
                print("Has tried %d times to access url %s, all failed!", maNum, link)
                break


def getContent(url, proxys):

    # 模拟浏览器访问，防止拦截
    proxy = random.choice(proxys)
    proxy_index = proxys.index(proxy)
    user_agent = random.choice(headers)
    send_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Connection": "keep-alive",
                    "Accept-Language": "Zh-CN, zh;q=0.8, en-gb;q=0.8, en;q=0.7",
                    "User-Agent": user_agent}
    print(proxy, user_agent)

    # 像目标url地址发送get请求，返回一个response对象
    # r = requests.get(url, headers=send_headers)
    # return r.text

    proxy_hand = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(proxy_hand)
    urllib.request.install_opener(opener)
    try:
        req = urllib.request.Request(url, headers=send_headers)
    except urllib.error.URLError as e:
        print('urllib.error.URLError except:', e)
        openlink(send_headers, url)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('urllib.error.HTTPError except:', e)

        proxys.pop(proxy_index)
        if len(proxys) == 0:
            proxys = getProxys()
            print(proxys)

        for i in range(10):
            time.sleep(5)
            try:
                response = urllib.request.urlopen(req)
                break
            except urllib.error.HTTPError as e:
                print('urllib.error.HTTPError except:', i, e)
    text = ''
    try:
        text = response.read().decode('gbk')
    except UnicodeDecodeError as e:
        print('UnicodeDecodeError except:', e)
    except ConnectionResetError as e:
        print('ConnectionResetError except:', e)
        while True:
            try:
                text = response.read().decode('gbk')
                break
            except ConnectionResetError as e:
                print('ConnectionResetError except:', e)
    return text


def getContentRequest(url):
    user_agent = random.choice(headers)
    send_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Connection": "keep-alive",
                    "Accept-Language": "Zh-CN, zh;q=0.8, en-gb;q=0.8, en;q=0.7",
                    "User-Agent": user_agent}
    r = requests.get(url, headers=send_headers)
    r.encoding = 'gbk'
    response_code = r.status_code
    if response_code == 403:
        print(response_code)
        time.sleep(random.randrange(5,10))
    return [response_code, r.text]


def getProxysXG():
    url = 'http://api3.xiguadaili.com/ip/?tid=557166374536560&filter=on&num=100&protocol=https&category=2&delay=1&area=北京'
    r = requests.get(url)
    r.encoding = 'utr-8'
    proxy_json = r.text
    proxys = proxy_json.split('\r\n')
    return proxys


def deleteProxy(ipProxys, proxy_index, error):
    ipProxys.pop(proxy_index)
    print(error, len(ipProxys))


def getContentRequestProxys(url, ipProxys):
    user_agent = random.choice(headers)
    send_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Connection": "keep-alive",
                    "Accept-Language": "Zh-CN, zh;q=0.8, en-gb;q=0.8, en;q=0.7",
                    "User-Agent": user_agent}

    proxy = random.choice(ipProxys)
    proxy_index = ipProxys.index(proxy)

    # proxyMeta = "http://" + proxy
    send_proxies = {
        "http": proxy,
        "https": proxy,
    }
    try:
        r = requests.get(url, headers=send_headers, proxies=send_proxies)
    except:
        deleteProxy(ipProxys, proxy_index, 'HTTPSConnectionPool')
        return None
    r.encoding = 'gbk'
    if r.status_code == 403:
        deleteProxy(ipProxys, proxy_index, 403)
    if len(ipProxys) == 0:
        ipProxys = getProxysXG()
        print(ipProxys)
    print(proxy)
    return r.text


if __name__ == '__main':
    print(getProxysXG())
