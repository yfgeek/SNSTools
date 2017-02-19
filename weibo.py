# -*- coding:utf-8 -*-
# Inspired by https://github.com/lzjun567/crawler_html2pdf/tree/master/heart
# Partial code by Ivan
import codecs
import csv
import re
import requests

cookies = {
    "_T_WM" : "ad60096c5acf1示例Cookie28f50d190365024aff4", 
    "SUB" : "_2A251rMWsDeRxGedO6V示例CookieVXbuvkrDV6PUJbkdBeLRjGkW0pDHzeewJsgAToIcymBD07FA-j4w..", 
    "SUHB" : "0FQd8示例Cookie9kDA5s", 
    "SCF" : "Am8FFSVq示例CookieR9XXi1hDnH6TyPHSBESCRC6JGC90f62Y3KVxxkcX6011HT0xYa8k.", 
    "SSOLoginState" : "148示例Cookie51644", 
    "M_WEIBOCN_PARAMS" : "luico示例Cookied%3D1076031765381094%26fid%3D1076031765381094%26uicode%3D10000011", 
    "H5_INDEX" : "0_friend", 
    "H5_INDEX_TITLE" : "%E5%A5%BD%E5%8F%8B%E5%9C%88%20"
}

def cleanring(content):
    pattern = "<a .*?/a>|<i .*?/i>|转发微博|//:|Repost|分享图片"
    content = re.sub(pattern, "", content)
    return content

def fetch_my_weibo(userid):
    api = "http://m.weibo.cn/index/my?format=cards&page=%s"
    for i in range(1, 102):
        response = requests.get(url=api+str(i), cookies=cookies)
        data = response.json()
        groups = data.get("cards") or []
        for group in groups:
            try:
                text = group.get("mblog").get("text")
                text = text.encode("utf-8")
                text = cleanring(text).strip()
                if text:
                    yield text
                    print text
            except:
                pass


def fetch_weibo_list(userid):
    #api = "http://m.weibo.cn/index/my?format=cards&page=%s"
    userid = userid + ""
    api = "http://m.weibo.cn/container/getIndex?uid="+ userid + "&featurecode=20000180&type=uid&value=" + userid + "&containerid=1076032260161101&page="
    for i in range(1, 102):
        response = requests.get(url=api+str(i), cookies=cookies)
        data = response.json()
        groups = data.get("cards") or []
        for group in groups:
            try:
                text = group.get("mblog").get("text")
                text = text.encode("utf-8")
                text = cleanring(text).strip()
                if text:
                    yield text
                    print text
            except:
                pass

def fetch_weibo_friend(userid):
    #api = "http://m.weibo.cn/index/my?format=cards&page=%s"
    userid = userid + ""
    api = "http://m.weibo.cn/container/getIndex?uid="+ userid + "&featurecode=20000180&type=uid&value=" + userid + "&containerid=1076032260161101&page="
    for i in range(1, 102):
        response = requests.get(url=api+str(i), cookies=cookies)
        data = response.json()
        groups = data.get("cards") or []
        for group in groups:
            try:
                id = group.get("mblog").get("id")
                id = id.encode("utf-8")
                cardcompoment = "http://m.weibo.cn/api/comments/show?id="+id+"&page=1"
                cresponse = requests.get(url=cardcompoment, cookies=cookies)
                commentdata = cresponse.json()
                commentgroup = commentdata.get("data") or []
                for c in commentgroup:
                    cuserid = c.get("user").get("id")
                    cusername = c.get("user").get("screen_name")
                    print cuserid
                    print cusername
            except:
                pass

def write_csv(texts,name):
    with codecs.open('./'+name+'.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=["text"])
        writer.writeheader()
        for text in texts:
            writer.writerow({"text": text})


def read_csv(name):
    with codecs.open('./'+name+'.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row['text']


if __name__ == '__main__':
    texts = fetch_weibo_friend("2260161101")
    #write_csv(texts,'ll')
