# coding = utf-8
# 爬取国家统计局地域代码
import urllib3
import urllib.request
from bs4 import BeautifulSoup
import re
from region import region
import pymysql
import random
class regionSpider:
    def __init__(self):
        self.city_tr_class = 'citytr'
        self.county_tr_class = 'countytr'
        self.town_tr_class = 'towntr'
        self.village_tr_class = 'villagetr'

    def getHtml(self,url):
        USER_AGENTS = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
        ]
        user_agent = random.choice(USER_AGENTS)
        headers = ('User-Agent', user_agent)
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        page = opener.open(url+"?COLLCC=46711612&")
        html = page.read().decode(encoding='gb2312', errors='ignore')
        return html

    def getCityNameAndUrl(self,url):
        dict = {}
        html = self.getHtml(url)
        soup = BeautifulSoup(html,'html.parser')
        city_trs = soup.find_all(class_=self.city_tr_class)
        for tr in city_trs:
            atags = tr.find_all(re.compile('td'))
            reg = region()
            for atag in atags:
                aurl = atag.find('a')["href"]
                reg.url = url[0:url.rindex("/")+1] + aurl
                pattern = re.compile(r'\d')
                if None==pattern.match(atag.find('a').text):
                    reg.name = atag.find('a').text
                else:
                    reg.code = atag.find('a').text
            dict[reg.code] = reg
        return dict

    def getCountyNameAndUrl(self,city_region):
        if None == city_region.url:
            return None
        county_dict = {}
        html = self.getHtml(city_region.url)
        soup = BeautifulSoup(html, 'html.parser')
        county_trs = soup.find_all(class_=self.county_tr_class)
        for tr in county_trs:
            atags = tr.find_all(re.compile('td'))
            reg = region()
            reg.parent_name = city_region.name
            reg.parent_code = city_region.code
            for atag in atags:
                if atag.find('a')!=None:
                    aurl = atag.find('a')["href"]
                    reg.url = city_region.url[0:city_region.url.rindex("/")+1] + aurl
                    pattern = re.compile(r'\d')
                    if None==pattern.match(atag.find('a').text):
                        reg.name = atag.find('a').text
                    else:
                        reg.code = atag.find('a').text
            county_dict[reg.code] = reg
        return county_dict

    def getTownNameAndUrl(self,county_region):
        if None==county_region.url or ''==county_region.url:
            return None
        town_dict = {}
        html = self.getHtml(county_region.url)
        soup = BeautifulSoup(html, 'html.parser')
        town_trs = soup.find_all(class_=self.town_tr_class)
        for tr in town_trs:
            td_tags = tr.find_all(re.compile('td'))
            reg = region()
            reg.parent_name = county_region.name
            reg.parent_code = county_region.code
            for td_tag in td_tags:
                if td_tag.find('a') != None:
                    aurl = td_tag.find('a')["href"]
                    reg.url = county_region.url[0:county_region.url.rindex("/") + 1] + aurl
                    pattern = re.compile(r'\d')
                    if None == pattern.match(td_tag.find('a').text):
                        reg.name = td_tag.find('a').text
                    else:
                        reg.code = td_tag.find('a').text
            town_dict[reg.code] = reg
        return town_dict

    def getVillageNameAndUrl(self,village_region):
        if None == village_region.url or ''==village_region.url:
            return None
        village_dict = {}
        html = self.getHtml(village_region.url)
        soup = BeautifulSoup(html, 'html.parser')
        village_trs = soup.find_all(class_=self.village_tr_class)
        for tr in village_trs:
            td_tags = tr.find_all(re.compile('td'))
            reg = region()
            reg.parent_name = village_region.name
            reg.parent_code = village_region.code
            for td_tag in td_tags:
                if td_tag != None:
                    pattern = re.compile(r'\d')
                    if None == pattern.match(td_tag.text):
                        reg.name = td_tag.text
                    else:
                        if len(td_tag.text)>3:
                            reg.code = td_tag.text
            village_dict[reg.code] = reg
        return village_dict

spider = regionSpider()
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/37.html'
city_dict = spider.getCityNameAndUrl(url)
county_dicts = {}
town_dicts = {}
village_dicts = {}
for city_code in city_dict.keys():
    #循环遍历市，获取各市的区县（市）
    city_region = city_dict.get(city_code)
    print(city_region)
    print("/n")
    county_dict = spider.getCountyNameAndUrl(city_region)
    county_dicts = dict(county_dicts, **county_dict)
    for county_code in county_dict.keys():
        #循环遍历区县（市），获取街道（镇）
        county_region = county_dict.get(county_code)
        print(county_region)
        town_dict = spider.getTownNameAndUrl(county_region)
        if None!=town_dict:
            town_dicts = dict(town_dicts,**town_dict)
            for town_code in town_dict:
                #循环遍历街道（镇），获取社区（村）
                print(town_dict.get(town_code))
                town_region = town_dict.get(town_code)
                village_dict = spider.getVillageNameAndUrl(town_region)
                if None!=village_dict:
                    village_dicts = dict(village_dicts,**village_dict)
                    for village_code in village_dict.keys():
                        print(village_dict.get(village_code))
#使用pymysql将数据插入数据库
try:
    conn = pymysql.connect(host='192.168.0.116', user='root', passwd='sh123456', db='shuheng', port=3306,charset='utf8')
    cur = conn.cursor()
    insert_sql = "insert into m_region(region_code,region_name,p_code,p_name) values"
    param = ""
    for county_code in county_dicts.keys():
        county_region = county_dicts.get(county_code)
        param = param + "('{}','{}','{}','{}'),".format(county_region.code, county_region.name,county_region.parent_code, county_region.parent_name)
    param = param[0,len(param)-1]
    insert_sql = insert_sql + param
    print(insert_sql)
    cur.execute(insert_sql)
    conn.commit()
except Exception:
    conn.rollback()
    print("发生异常")






