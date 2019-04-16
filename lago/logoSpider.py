# coding = utf-8
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import urllib.request
from bs4 import BeautifulSoup
import requests
import json
import time
import pymongo


class logoSpider:

    def get_db(self, db_name='lago_db'):
        client = pymongo.MongoClient("mongodb://192.168.0.116:27017/")
        db = client[db_name]
        return db

    def get_collection(self, collection_name):
        db = self.get_db()
        return db[collection_name]

    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/positionAjax.json'
        self.datas = {'city':'青岛','needAddtionalResult':'false','kd':'java','first':'true'}
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '23',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.lagou.com/jobs/list_java?city=%E6%B5%8E%E5%8D%97&cl=false&fromSearch=true&labelWords=&suginput=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.cookies = {
            'Cookie' : 'user_trace_token=20180313112427-25b844be-2e87-47e4-9eec-d9178359ed3d; LGUID=20180313112428-095b9ed4-266e-11e8-b1de-5254005c3644; _ga=GA1.2.863354284.1520911468; index_location_city=%E5%85%A8%E5%9B%BD; LG_LOGIN_USER_ID=71b5d7e54cb0876b72158d675a92a65fb828b3689c81e61a; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=39; JSESSIONID=ABAAABAABEEAAJAB5173ADEDE726D745D2D0A695FE51F77; _gid=GA1.2.2007363481.1535945859; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1534764004,1535707668,1535707689,1535945859; _putrc=9E146D865DDC7585; login=true; unick=%E9%83%91%E9%B9%8F%E9%B9%8F; gate_login_token=bdce41a18d2241b98b95bcc8c8d531861638786848688b2d; TG-TRACK-CODE=jobs_code; _gat=1; LGSID=20180903154139-cad92d18-af4c-11e8-b4e7-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3Fcity%3D%25E6%25B5%258E%25E5%258D%2597%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535960568; LGRID=20180903154248-f41fbb15-af4c-11e8-8562-525400f775ce; SEARCH_ID=4697bf0dbcb444df9a35267c77bfea7f'
        }


    def get_content(self,page_num):
        self.datas.update({'pn':page_num})
        self.headers.update({'Referer':'https://www.lagou.com/jobs/list_java?city=%E6%B5%8E%E5%8D%97&cl=false&fromSearch=true&labelWords=&suginput='})
        content = requests.post(url=self.url, cookies=self.cookies, headers=self.headers, data=self.datas)
        json_str = content.json()
        return json_str

    def get_job_details(self,json_str):
        job_list = json_str['content']['positionResult']['result']
        job_detail_list = []
        for j in range(len(job_list)):
            job_detail = {}
            job_detail['_id'] = job_list[j]['positionId']
            job_detail['positionId'] = job_list[j]['positionId']
            job_url = 'https://www.lagou.com/jobs/'+str(job_list[j]['positionId'])+'.html'
            self.headers.update({'Referer':job_url})
            html = requests.post(url=job_url,cookies=self.cookies, headers=self.headers, data=self.datas).text
            soup = BeautifulSoup(html, 'html.parser')
            job_info = soup.find('dd',class_='job_bt')
            if job_info!=None:
                job_detail["job_info"] = job_info.text
            job_detail["workYear"] = job_list[j]['workYear']
            job_detail["companyFullName"] = job_list[j]['companyFullName']
            job_detail["education"] = job_list[j]['education']
            job_detail["city"] = job_list[j]['city']
            job_detail["district"] = job_list[j]['district']
            job_detail["companySize"] = job_list[j]['companySize']
            job_detail["salary"] = job_list[j]['salary']
            job_detail["positionName"] = job_list[j]['positionName']
            job_detail_list.append(job_detail)
        return job_detail_list

lago = logoSpider()
json_str = lago.get_content(1)
# json_obj = json.loads(json_str)
page_size = json_str['content']['pageSize']
total_count = json_str['content']['positionResult']['totalCount']
page_num = total_count//page_size + 1
for i in range(page_num):
    time.sleep(10)
    print(i+1)
    json_str = lago.get_content(i + 1)
    while(json_str['success']==False):
        time.sleep(10)
        json_str = lago.get_content(i + 1)
    print(json_str)
    job_detail_list = lago.get_job_details(json_str)
    db = lago.get_collection('lago_collection')
    if job_detail_list!=None and len(job_detail_list)>0:
        try:
            ids = db.insert_many(job_detail_list)
            print(ids.inserted_ids)
        except Exception:
            print("主键重复")



