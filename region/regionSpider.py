# coding = utf-8
# 爬取国家统计局地域代码

import urllib.request
from bs4 import BeautifulSoup
import re
from region import region
class regionSpider:
    def __init__(self):
        self.url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/37.html'
        self.cityUrls = set()
        self.city_tr_class = 'citytr'
        self.county_tr_class = 'countytr'
        self.town_tr_class = 'towntr'
        self.village_tr_class = 'villagetr'

    def getHtml(self,url):
        page = urllib.request.urlopen(url)
        html = page.read().decode(encoding='gb2312', errors='ignore')
        return html

    def getCityNameAndUrl(self,url):
        dict = {}
        html = self.getHtml(self.url)
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
                print(town_dicts.get(town_code))
                town_region = town_dicts.get(town_code)
                village_dict = spider.getVillageNameAndUrl(town_region)
                if None!=village_dict:
                    village_dicts = dict(village_dicts,**village_dict)
                    for village_code in village_dict.keys():
                        print(village_dicts.get(village_code))


