import requests
from bs4 import BeautifulSoup
import urllib
import re
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import GoodsType, GoodsDetail

import json
import time
millis = int(round(time.time() * 1000))

#momo爬蟲 商品數量約 5912700
def momogoods(goodnumber):
    link = 'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code='
    url = link+str(goodnumber)   #選擇網址
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15' #偽裝使用者
    headers = {'User-Agent':user_agent}
    data_res = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(data_res, timeout=20)
    sp = BeautifulSoup(data, "lxml")
    try:
        #商品名稱
        pdname_bs4 = sp.find("div",{"class":"prdnoteArea"}).find("h1")
        pdname_text = str(pdname_bs4.text)
        momopdname = pdname_text
        #商城名稱
        momopdshop = 'momo購物網'
        #商品類別
        try:
            pdclass_bs4 = sp.find("div",{"id":"bt_2_layout_NAV"}).find("h5")
            pdclass = str(pdclass_bs4.text)
            momopdclass = pdclass
        except:
            momopdclass = '尚無類別'
        #商品價格
        pdprice_bs4 = sp.find("li",{"class":"special"}).find("span")
        momopdprice_removesymbol = str(pdprice_bs4.text).replace(',','')
        momopdprice = momopdprice_removesymbol

        #商品圖片連結
        momoimgs_bs4 = sp.find("div",{"class":"gmclass"}).findAll("a", href = re.compile('goodsimg'))
        for momoimg_getlink in momoimgs_bs4:
            momoimg = 'https:'+ momoimg_getlink['href']
        print(momopdname)
        print(momopdprice)
        print(momopdclass)
        print(momopdshop)
        print(momoimg)
        print(url)
        momosql(momopdname,momopdprice,momopdclass,momopdshop,momoimg,url)
    except:
       print('該編號無商品')


def momosql(momopdname,momopdprice,momopdclass,momopdshop,momoimg,url):
    goodname = momopdname
    goodprice = momopdprice
    goodshop = momopdshop
    goodtype = momopdclass
    goodlink = url
    goodimglink = momoimg

    try:
        typename = GoodsType.objects.get(type_name=goodtype)
        print('存入分類')
    except:
        typename = GoodsType.objects.create(type_name=goodtype)
        print('創建分類')
    typename.save()
        
    try:
        momodb = GoodsDetail.objects.get(goodlink=goodlink)
        momodb.goodname = goodname
        momodb.goodprice = momopdprice
        momodb.goodshop = momopdshop
        momodb.goodtype = typename
        momodb.goodlink = url
        momodb.goodimglink = momoimg
        momodb.save()
        print('更新資料')
    except:
         momodb = GoodsDetail.objects.create(goodname=goodname, goodprice=goodprice, goodshop=goodshop, goodtype=typename, goodlink=goodlink, goodimglink=goodimglink)
         momodb.save()
         print('成功存入一筆資料')


def momocrawler(request):
    for code in range(5626760,5900162):
        try:
            momogoods(code)
        except:
            print("爬取錯誤")
    return redirect('home')

def pcgood(pccid,page,pcclname):
    url = 'https://ecapi.pchome.com.tw/mall/prodapi/v1/newarrival/prod&region=' + str(pccid) + '&offset='+ str(page) +'&limit=50&_callback=jsonpcb_newarrival'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' #偽裝使用者
    headers = {'User-Agent':user_agent,
              'server': 'PChome/1.0.4',
              'Referer': 'https://mall.pchome.com.tw/newarrival/'}
    res = requests.get(url=url,headers=headers)#分析得出的網址
    res_text = res.text
    res_text_format = res_text.replace('try{jsonpcb_newarrival(','').replace(');}catch(e){if(window.console){console.log(e);}}','')
    jd = json.loads(res_text_format)
    if jd['Rows'] != []:
        pcgoods = (jd['Rows'][:])
        for pcgood in pcgoods:
            pcname = pcgood['Name']
            pcimg = 'https://b.ecimg.tw' + pcgood['Pic']['S']
            pcprice = pcgood['Price']['P']
            pclink = 'https://mall.pchome.com.tw/prod/'+ pcgood['Id']
            pcshop = 'PChome購物中心'
            if pcclname == '運動戶外':
                pcclname = '運動休閒'
            if pcclname == '生活':
                pcclname = '居家生活'
            if pcclname == '時尚':
                pcclname = '鞋包配飾'
            print(pcname)
            print(pcimg)
            print(pcprice)
            print(pclink)
            print('分類：'+pcclname)
            pchomesql(pcname,pcprice,pcclname,pcshop,pcimg,pclink)
    else:
        status = 'no_data'
        return status



def pchomesql(pcname,pcprice,pcclname,pcshop,pcimg,pclink):
    goodname = pcname
    goodprice = pcprice
    goodshop = pcshop
    goodtype = pcclname
    goodlink = pclink
    goodimglink = pcimg

    try:
        typename = GoodsType.objects.get(type_name=goodtype)
        print('存入分類')
    except:
        typename = GoodsType.objects.create(type_name=goodtype)
        print('創建分類')
    typename.save()
        
    try:
        pcdb = GoodsDetail.objects.get(goodlink=goodlink)
        pcdb.goodname = goodname
        pcdb.goodprice = goodprice
        pcdb.goodshop = goodshop
        pcdb.goodtype = typename
        pcdb.goodlink = goodlink
        pcdb.goodimglink = goodimglink
        pcdb.save()
        print('更新資料')
    except:
         momodb = GoodsDetail.objects.create(goodname=goodname, goodprice=goodprice, goodshop=goodshop, goodtype=typename, goodlink=goodlink, goodimglink=goodimglink)
         momodb.save()
         print('成功存入一筆資料')




#分類、頁數遍歷
#分析後，網址結尾需加上13位unix時間戳記
def pchomecrawler(request):
    url = 'https://ecapi.pchome.com.tw/mall/cateapi/v1/sign&tag=newarrival&fields=Id,Name,Sort,Nodes&_callback=jsonpcb_newarrival&'+str(millis)
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' #偽裝使用者
    headers = {'User-Agent':user_agent,
              'server': 'PChome/1.0.4',
              'Referer': 'https://mall.pchome.com.tw/newarrival/'}
    res = requests.get(url=url,headers=headers)#分析得出的網址
    res_text = res.text
    res_text_format = res_text.replace('try{jsonpcb_newarrival(','').replace(');}catch(e){if(window.console){console.log(e);}}','')
    jd = json.loads(res_text_format)
    pcclass = jd[2:5]
    #print(pc)
    for pc in pcclass:
        pcclname = pc['Name']
        print(pc['Name'])
        for pccl in pc['Nodes']:
            pccid = pccl['Id']
            pageid = 1
            for page in range(10):  
                print(page)
                if pcgood(pccid,pageid,pcclname) != 'no_data':
                    pcgood(pccid,pageid,pcclname)
                    pageid = pageid + 50
                    time.sleep(8)
                else:
                    break


    return redirect('home')
        