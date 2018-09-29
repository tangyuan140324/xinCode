# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-03-12 14:22:38
# Project: taobao
import base64
import hashlib
import random
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *
import re
import time
import json
from Api import *
from pyspider_Func import parser, binarySearch
from redis_update import oPut_proxy_redis

####################


keywordsConfigPath = '/web/spider/config/keywords.conf'
keywordsDonePath = '/web/spider/log/keywordsDone.log'
wr = configparser.ConfigParser()
wr.read("/web/spider/config/host.conf")

host = wr.get('redis', 'redis_host')
port = wr.get('redis', 'redis_port')



proxy_list_out = oPut_proxy_redis(host,port,db = 14)


class Handler(BaseHandler):
    @every(minutes=5 * 24 * 60)
    def on_start(self):
        def get_keywords(n=1):
            # Read config file for keyword and page_count.
            with open(keywordsConfigPath, 'r') as f:
                keywords = f.read().split(",")
                if keywords == ['']:
                    print("All keywords cralwed.")
                    return
            keyword = keywords[0:n]
            b = ",".join(keyword[0:n])
            a = ",".join(keywords[n:])
            with open(keywordsConfigPath, 'w') as fp:
                fp.write(a)
            with open(keywordsDonePath, 'a') as g:
                if keywords != ['']:
                    g.write(',' + b)
            return keyword
        li = get_keywords()
        for keyword in li:
            url = "https://s.taobao.com/search?q=" + keyword
            proxy = random.choice(proxy_list_out)
            save = {'keyword': keyword}
            self.crawl(url, callback=self.listpage, save=save, validate_cert=False, proxy=proxy)

    @config(age=24 * 60 * 60)
    def listpage(self, response):
        '''
        1:获取首页前部分的商品ID。
        2：获取keyword能得到的最大页数。
        '''
        cookie = response.cookies
        content = re.findall(r' g_page_config = (.*?)g_srp_loadCss', response.text, re.S)
        content = content[0].strip()
        content = content[:-1]
        content = json.loads(content)
        currentUrl = response.url
        time.sleep(0.5)
        data_list = content['mods']['itemlist']['data']['auctions']

        # 获取keyword的最大页数。
        page_count = content['mods']['pager']['data']['totalPage']

        url = 'https://s.taobao.com/api?_ksTS=1520660552889_267&callback=jsonp268&m=customized&q=' + response.save[
            'keyword'] + '&commend=all&ie=utf8'
        proxy = random.choice(proxy_list_out)
        save = {'page_count': page_count, 'keyword': response.save['keyword'], 'referer': currentUrl, 'cookies': cookie}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'referer': currentUrl
        }
        self.crawl(url, callback=self.firstPageBottomHalf, save=save, validate_cert=False, headers=headers, proxy=proxy)

        # 36 products
        ret_data = []
        for item in data_list:
            temple = parser(item, currentUrl, response)
            if Filter_Redis(host, port, temple['nid']) == True and temple['isTmall'] == True:
                setTmallId(host, port, temple['nid'], db=5)
                if "click" not in temple['detail_url']:
                    proxy = random.choice(proxy_list_out)
                    headers = {
                        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                                      "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
                        "referer": currentUrl
                    }
                    save = {'source_nid': temple['nid'], 'keyword': response.save['keyword']}
                    self.crawl(temple['detail_url'], callback=self.product_Tmallpage, save=save, validate_cert=False,
                               headers=headers, proxy=proxy)
                    ret_data.append(temple)
            else:
                if Filter_Redis(host, port, temple['nid']) == True and temple['isTmall'] == False:
                    W_Shop_Id(host, port, temple['nid'], db=4)
                    proxy = random.choice(proxy_list_out)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                        'referer': currentUrl
                    }
                    self.crawl(temple['detail_url'], callback=self.product_taobao, validate_cert=False, headers=headers,
                               proxy=proxy)
                    basic_url = 'http://s.m.taobao.com/search?m=api4h5&n=40&nick='
                    url_taobao_shop = basic_url + item["nick"]
                    save = {'url': url_taobao_shop}
                    self.crawl(url_taobao_shop, callback=self.product_taobaopage, save=save, headers=headers,
                               proxy=proxy)
                    ret_data.append(temple)
        return ret_data

    @config(age=24 * 60 * 60)
    def firstPageBottomHalf(self, response):
        '''
        1:加载下半页12条商品数据。
        2：做翻页处理。
        3：进入每一个可爬的商品页面爬取
        '''

        cookie = response.save['cookies']
        keyword = response.save['keyword']
        page_count = response.save['page_count']
        referer = response.save['referer']

        '''
        翻页
        '''
        for i in range(1, int(page_count) + 1):
            # time.sleep(1)
            ktsts = time.time()
            _ksTS = '%s%s' % (int(ktsts * 1000), str(ktsts)[-3:])
            callback = "jsonp%s" % (int(str(ktsts)[-3:]) + 1)
            data_vale = 44 * i
            url = 'https://s.taobao.com/search?data-key=s&data-value={}&ajax=true&_ksTS={}&callback={}&q={}&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=4&ntoffset=0&p4ppushleft=1%2C48'.format(
                data_vale, _ksTS, callback, keyword)

            print(url)
            print("pagenumber:", i)
            proxy = random.choice(proxy_list_out)
            save = {'page_count': response.save['page_count'], 'keyword': response.save['keyword'], 'cookies': cookie}
            self.crawl(url, callback=self.index_page, save=save, validate_cert=False, proxy=proxy)

        ## 12 records
        html = response.text
        content = re.findall(r'{.*}', html, re.S)[0]
        content = json.loads(content)
        data_list = content['API.CustomizedApi']['itemlist']['auctions']
        ret_data = []
        for item in data_list:
            temple = parser(item, referer, response)
            if Filter_Redis(host, port, temple['nid']) == True and temple['isTmall'] == True:
                setTmallId(host, port, temple['nid'], db=5)
                if "click" not in temple['detail_url']:
                    proxy = random.choice(proxy_list_out)
                    headers = {
                        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                                      "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
                        "referer": referer
                    }
                    save = {'source_nid': temple['nid'], 'keyword': response.save['keyword']}
                    self.crawl(temple['detail_url'], callback=self.product_Tmallpage, save=save, validate_cert=False,
                               headers=headers, proxy=proxy)
                    ret_data.append(temple)
            else:
                if Filter_Redis(host, port, temple['nid']) == True and temple['isTmall'] == False:
                    W_Shop_Id(host, port, temple['nid'], db=4)
                    proxy = random.choice(proxy_list_out)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                        'referer': referer
                    }
                    self.crawl(temple['detail_url'], callback=self.product_taobao, validate_cert=False, headers=headers,
                               proxy=proxy)
                    basic_url = 'http://s.m.taobao.com/search?m=api4h5&n=40&nick='
                    url_taobao_shop = basic_url + item["nick"]
                    save = {'url': url_taobao_shop}
                    self.crawl(url_taobao_shop, callback=self.product_taobaopage, save=save, headers=headers,
                               proxy=proxy)
                    ret_data.append(temple)
        return ret_data

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        '''
        1：翻页后的（2——end）每一页商品解析。
        2：获取每一个商品并进入每一个商品页面的数据详情。

        '''
        cookie = response.save['cookies']
        #save = {'cookie': cookie, 'page_count': response.save['page_count'], 'keyword': response.save['keyword']}
        referer = response.url
        html = response.text
        ret_data = []
        re_context = re.findall(r'{.*}', html, re.S)
        if re_context:
            content = json.loads(re_context[0])
            data_list = content['mods']['itemlist']['data']['auctions']
            for item in data_list:
                temple = parser(item, referer, response)
                if Filter_Redis(host, port, temple['nid']) == True and temple['isTmall'] == True:
                    setTmallId(host, port, temple['nid'], db=5)
                    if "click" not in temple['detail_url']:
                        proxy = random.choice(proxy_list_out)
                        headers = {
                            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                                          "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
                            "referer": referer
                        }
                        save = {'source_nid': temple['nid'], 'keyword': response.save['keyword']}
                        self.crawl(temple['detail_url'], callback=self.product_Tmallpage, save=save, validate_cert=False,
                                   headers=headers, proxy=proxy)
                        ret_data.append(temple)
                else:
                    if Filter_Redis(host, port, temple['nid']) == True and temple['isTmall'] == False:
                        W_Shop_Id(host, port, temple['nid'], db=4)
                        proxy = random.choice(proxy_list_out)
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                            'referer': referer
                        }
                        self.crawl(temple['detail_url'], callback=self.product_taobao, validate_cert=False, headers=headers,
                                   proxy=proxy)
                        basic_url = 'http://s.m.taobao.com/search?m=api4h5&n=40&nick='
                        url_taobao_shop = basic_url + item["nick"]
                        save = {'url': url_taobao_shop}
                        self.crawl(url_taobao_shop, callback=self.product_taobaopage, save=save, headers=headers,
                                   proxy=proxy)
                        ret_data.append(temple)
        return ret_data

    @config(age=24 * 60 * 60)
    def product_taobaopage(self,response):
        html = response.text
        saveurl = response.save['url']
        totalPage_old = json.loads(html).get('totalPage')
        urlfun = saveurl+"&page="+totalPage_old
        totalPage = binarySearch(urlfun,page2=int(totalPage_old))
        urls = []
        for item in range(1,int(totalPage)+1):
            url = saveurl+'&page='+str(item)
            urls.append(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        proxy = random.choice(proxy_list_out)
        save = {'saveurl':saveurl}
        self.crawl(urls, callback=self.product_taobaourls,save = save, headers=headers, proxy=proxy)

    @config(age=24 * 60 * 60)
    def product_taobaourls(self,response):
        html = response.text
        currentUrl = response.save['saveurl']
        ta = json.loads(html)
        time.sleep(0.5)
        data = ta.get('listItem')
        for item in data:
            item['dateType'] = 'taobao_list'
            item['crawlDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['uz_id'] = hashlib.md5((str(item['item_id']) + str(time.time())).encode('utf-8')).hexdigest()
            detail_url = urljoin(currentUrl, item['url'])
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
            }
            proxy = random.choice(proxy_list_out)
            self.crawl(detail_url, callback=self.product_taobao, headers=headers, proxy=proxy)
        return data

    @config(age=24 * 60 * 60)
    def product_taobao(self, response):
        '''
        1：解析单凭页面的数据详情。
        2：数据传递接给kafka。
        '''

        html = response.text
        loc = 'taobao'

        bsObj = BeautifulSoup(html, 'lxml')
        try:
            attributesList = bsObj.find('ul', {'class': 'attributes-list'}).findAll('li')
            attributes = []
            for attribute in attributesList:
                attribute = attribute.get_text()
                num = attribute.split(':')
                print(num)
                if len(num) > 2:
                    abc = ":".join(num[1:])
                    dic = {num[0]: abc}
                    attributes.append(dic)
                attributes.append({num[0]: num[1]})
        except AttributeError:
            attributes = None

        try:
            title = bsObj.h3.get_text().strip()
        except AttributeError:
            title = bsObj.h1.get_text().strip()
        try:
            if bsObj.find('em', {'class': 'tb-rmb-num'}):
                price = bsObj.find('em', {'class': 'tb-rmb-num'}).get_text()
            else:
                price = None
        except AttributeError:
            if bsObj.find('span', {'class': 'tm-price'}):
                price = bsObj.find('span', {'class': 'tm-price'}).get_text()
            else:
                price = None

        try:
            if bsObj.find('div', {'id': 'service'})['data-item-id']:
                nid = bsObj.find('div', {'id': 'service'})['data-item-id']
            else:
                nid = None
        except AttributeError:
            if bsObj.find('div', {'id': 'service'})['data-item-id']:
                nid = bsObj.find('div', {'id': 'service'})['data-item-id']
            else:
                nid = None
        com = bsObj.find('div', {'class': "tb-booth tb-pic tb-main-pic"}).a['href']
        shop_id_list = com.split('shopId=')
        if len(shop_id_list) == 2:
            shop_id = shop_id_list[1].split('&')[0]

        else:
            shop_id = shop_id_list[0]
        soup = html.split('g_config = {')[1].split("};")[0].strip().replace(' ', '')
        li = soup.split(',\n')
        for x in li:
            if isinstance(x, str):
                if "\'" in x or "\n" in x:
                    i = li.index(x)
                    x = x.replace("\'", "").replace("\n", "")
                    li[i] = x
        g_config = []
        for item in li:
            num = item.split(':')
            if len(num) > 2:
                abc = ":".join(num[1:])
                dic = {num[0]: abc}
                g_config.append(dic)
            g_config.append({num[0]: num[1]})
        uz_id = hashlib.md5((nid + str(time.time())).encode('utf-8')).hexdigest()
        ## download images
        img_urls = []
        location = re.findall(r'img data-src="(.*?)" /></a>', html, re.S)
        for i in range(len(location)):
            tep = location[i].split('.jpg')[0]
            tep_c = tep + '.jpg'
            if tep_c[0:2] != '//':
                url_new = tep_c
            else:
                url_new = 'https:' + tep_c
            img_urls.append(url_new)
        product_info = {"title": title,
                        "price": price,
                        "nid": nid,
                        "attributes": attributes,
                        "shop_id": shop_id,
                        "crawlDate": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        'dateType': 'product',
                        'uz_id' : uz_id,
                        "g_config":g_config,
                        "img_urls":img_urls
                        }
        #dowloadPic(loc, response, nid)
        return product_info

    @config(age=24 * 60 * 60)
    def product_Tmallpage(self, response):

        '''
        获取tmall店铺获取商品总页数的URL
        '''
        html = response.text
        source_nid = response.save['source_nid']
        print(html)
        soup = BeautifulSoup(html, 'lxml')
        shop_url = soup.find('a', {'class': 'toshop cell'})['href']
        shop_name = re.findall('//(.*?).m.tmall.com', shop_url, re.S)[0]

        url_beg = 'https://{}.m.tmall.com'.format(shop_name)
        num = random.randint(83739921, 87739530)
        endurl = '/shop/shop_auction_search.do?sort=s&p=1&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        url = url_beg + endurl.format(num)
        print('获取总页数的url:', url)
        save = {'url': url_beg,'source_nid':source_nid, 'keyword': response.save['keyword']}
        proxy = random.choice(proxy_list_out)
        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                          "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }
        self.crawl(url, callback=self.product_Tmallurls, save=save, validate_cert=False, headers=headers, proxy=proxy)

    @config(age=24 * 60 * 60)
    def product_Tmallurls(self, response):
        html = response.text
        source_nid = response.save['source_nid']
        infos = re.findall('\(({.*})\)', html)[0]
        infos = json.loads(infos)
        total_page = infos.get('total_page')
        url_beg = response.save['url']
        urls = []
        for i in range(1, int(total_page) + 1):
            time.sleep(1+random.random())
            num = random.randint(83739921, 87739530)
            page = i
            endurl = '/shop/shop_auction_search.do?sort=s&p={}&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
            url = url_beg + endurl.format(page, num)
            urls.append(url)
        #proxy = random.choice(proxy_list_out)
        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                          "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }
        save = {'url': url_beg, 'source_nid': source_nid, 'keyword': response.save['keyword']}
        self.crawl(urls, callback=self.product_tmall, validate_cert=False, headers=headers,save=save,
                   proxy=random.choice(proxy_list_out))

    @config(age=24 * 60 * 60)
    def product_tmall(self, response):
        ret_data = []
        source_nid = response.save['source_nid']
        keyword = response.save['keyword']
        html = response.text
        currentUrl = response.url
        infos = re.findall('\(({.*})\)', html)[0]
        infos = json.loads(infos)
        products = infos.get('items')
        shopName = infos.get('shop_title')
        shop_id = infos.get('shop_id')
        for item in products:
            try:
                sold = item['sold']
            except:
                sold =  None
            detail_url = urljoin(currentUrl, item['url'])
            uz_id = hashlib.md5((str(item['item_id']) + str(time.time())).encode('utf-8')).hexdigest()
            temple = {
                "nid": item['item_id'],
                "source_nid":source_nid,
                "title": item['title'],
                "img": item['img'],
                "sold": sold,
                "shopName":shopName,
                "shop_id":shop_id,
                "quantity": item['quantity'],
                "totalSoldQuantity": item['totalSoldQuantity'],
                "url": detail_url,
                "price": item['price'],
                "productType": keyword,
                'crawlDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "titleUnderIconList": item['titleUnderIconList'],
                "dateType":"list",
                "uz_id" : uz_id,
                "_meta":{ 'store': 'mongodb'}
            }
            ret_data.append(temple)
            headers = {
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                              "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
            }
            save = {"nid":item['item_id'],"source_nid":source_nid}
            self.crawl(detail_url, callback=self.product_tmallinfo, validate_cert=False, headers=headers,save=save,
                       proxy=random.choice(proxy_list_out))
        return ret_data

    @config(age=24 * 60 * 60)
    def product_tmallinfo(self,response):
        html = response.text
        source_nid = response.save['source_nid']
        nid = response.save['nid']
        groupProps = re.findall(r'"groupProps":\[(.*?)\],"props', html, re.S)
        groupProps = groupProps[0]
        tmall_product_data = json.loads(groupProps)
        tmall_product_data['nid'] = nid
        tmall_product_data['uz_id'] = hashlib.md5((str(nid) + str(time.time())).encode('utf-8')).hexdigest()
        tmall_product_data['source_nid'] = source_nid
        tmall_product_data['dateType'] = 'product'
        tmall_product_data['crawlDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        url = "https://detail.tmall.com/item.htm?id="+str(nid)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        proxy = random.choice(proxy_list_out)
        save = {"nid":nid}
        self.crawl(url, callback=self.product_taobaophoto,save = save, headers=headers, proxy=proxy)
        return tmall_product_data

    def product_taobaophoto(self, response):
        # nid = response.save['nid']
        # loc = "tmall"
        nid = response.save['nid']
        html = response.text
        title = re.findall(r'<title>(.*?)</title>', html, re.S)[0]
        img_urls = []
        location = re.findall(r'img src="(.*?)" /></a>',html,re.S)
        for i in range(len(location)):
            tep = location[i].split('.jpg')[0]
            tep_c = tep + '.jpg'
            if tep_c[0:2] != '//':
                url_new = tep_c
            else:
                url_new = 'https:' + tep_c
            img_urls.append(url_new)
        product_info = {
            "title":title,
            "img_urls":img_urls,
            "nid":nid
        }
        return product_info

        #dowloadPic(loc, response, nid)
