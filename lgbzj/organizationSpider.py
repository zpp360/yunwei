#coding = utf-8

import urllib.request
from bs4 import BeautifulSoup
import re

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode(encoding='gb2312',errors='ignore')
    return html
org_list = []
domain = "http://www.lgbzyz.com"
page_total = int(input("总页码:\n"))
for page_num in range(0,page_total):
    url = domain + "/mcase.php?lb=0&dq=0&state=0&page="+str(page_num)
    html = getHtml(url)
    soup = BeautifulSoup(html,'html.parser')
    data_li = soup.find('div',class_='data_list_data').find_all('li',class_='clearfix')
    for li in data_li:
        org_dic = {}
        home_href = domain + "/" + li.find(href=re.compile('showdown.php?'))['href']
        home_html = getHtml(home_href)
        soup = BeautifulSoup(home_html,'html.parser')
        org_title = soup.find('div',class_='pro_config').find('h1').text
        org_dic['org_title'] = org_title
        org_img = soup.find('div',class_='pic2').find('img')['src']
        org_dic['org_pic'] = domain + org_img
        for li in soup.find('div',class_='info').find_all('li'):
            text = li.text
            if text.find('所属地区：')!=-1:
                org_dic['org_city'] = text[5:]
                continue
            if text.find('主管单位：')!=-1:
                org_dic['org_unit'] = text[5:]
                continue
            if text.find('人数：')!=-1:
                org_dic['person_count'] = text[3:]
                continue
            if text.find('成立日期：')!=-1:
                org_dic['org_time'] = text[5:]
                continue
            if text.find('负责人：')!=-1:
                org_dic['org_linkman'] = text[4:]
                continue

        table_tr = soup.find('table',class_='pro_table').find_all('tr')
        for tr in table_tr:
            td = tr.find_all('td')
            if(td[0].text.find('联系人:')>-1):
                org_dic['org_linkman'] = td[1].text
                continue
            if (td[0].text.find('电子邮箱:')>-1):
                org_dic['org_email'] = td[1].text
                continue
            if (td[0].text.find('详细通讯地址')>-1):
                org_dic['org_address'] = td[1].text
                continue

        org_dic['org_desc'] = soup.select('p[class="m5"]')[0].text
        print(org_dic)





