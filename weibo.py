# -*- coding:utf-8 -*-
# Inspired by https://github.com/lzjun567/crawler_html2pdf/tree/master/heart
# Partial code by https://github.com/yfgeek
import codecs
import csv
import re
import requests
import time

cookies = {
    "_T_WM" : "5f2c5ff65ad87f3示例COOKIE0227531a73ae204", 
    "SUB" : "_2A251rcMgDeRxGedO6示例COOKIE6PUJbkdBeLUvxkW0X_1x2mYG5chfbtaPbWobp7b4W_A..", 
    "SUHB" : "0XDT示例COOKIEiGL9jQGes", 
    "SCF" : "AjzTxE示例COOKIEU_Zttv11Rc2nIzSYkqyvJF5bmSRja7FlXO72MUmNb6H6pzNJEfCJNw3w.", 
    "SSOLoginState" : "1487516528", 
    "M_WEIBOCN_PARAMS" : "uicode=10000189", 
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
        time.sleep(3)
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

def fetch_weibo_friend(userid,cid):
    #api = "http://m.weibo.cn/index/my?format=cards&page=%s"
    userid = userid + ""
    api = "http://m.weibo.cn/container/getIndex?uid="+ userid + "&featurecode=20000180&type=uid&value=" + userid + "&containerid="+cid+"&page="
    for i in range(1, 102):
        time.sleep(3)
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
                    cusercontent = c.get("text")
                    write_comments_csv(cuserid,cusername,cusercontent,userid)
            except(AttributeError):
                pass

def write_comments_csv(id,screen_name,reply_text,name):
    result = []
    result.append(id)
    result.append(screen_name.encode("utf-8"))
    result.append(reply_text.encode("utf-8"))
    print result
    with open(name+'.csv', 'a+') as csvfile:
        spamwriter = csv.writer(csvfile,dialect='excel')
        spamwriter.writerow(result)

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
    texts = fetch_weibo_friend("245示例userid4850","1076示例containerid34850")
    #write_csv(texts,'ll')
