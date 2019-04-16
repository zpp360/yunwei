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
import requests
from bs4 import BeautifulSoup
import pymongo



class jnhouse_spider:
    def __init__(self):
        self.url = 'http://www.jnhouse.com/lpzs/list.php?switch=1&type=1&pageno=1'
        self.datas = {'switch':'1','type':'1','pageno':'10'}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.cookies = {
            'Cookie':'PHPSESSID=cvm0pnivaa91fc851u5su824s7; CITY_LETTER=Tjs%3D; Hm_lvt_8434a01c0f1aa5061b6b89386e88ac73=1536558813; _smt_uid=5b96071c.3eb0b33e; Hm_lpvt_8434a01c0f1aa5061b6b89386e88ac73=1536561450'
        }

    def get_db(self, db_name='jnhouse_db'):
        client = pymongo.MongoClient("mongodb://192.168.1.116:27017/")
        db = client[db_name]
        return db

    def get_collection(self, collection_name):
        db = self.get_db()
        return db[collection_name]

    def getContent(self,page_no=1):
        self.url = 'http://www.jnhouse.com/lpzs/list.php?switch=1&type=1&pageno='+str(page_no)
        post = requests.post(url=self.url, cookies=self.cookies, headers=self.headers,data=self.datas)
        return post.text

    def getHouseInfo(self):
        page_total = int(input("总页码:\n"))
        data_from = input("数据来源:\n")
        for page_no in range(0,page_total):
            html = self.getContent(page_no+1)
            soup = BeautifulSoup(html,'html.parser')
            house_list = soup.find_all('div',class_='unit')
            house_data = []
            for i in range(len(house_list)):
                house_name = house_list[i].find('div',class_='title').contents[0].strip()
                house_status = house_list[i].find('span',class_='blue').text
                house_addr = house_list[i].find('div',class_='address').text
                house_type = house_list[i].find('div',class_='houseType').text
                house_tag = house_list[i].find('div',class_='tag').text
                house_price = house_list[i].find('div',class_='price').find('span',class_='tx').text
                if house_price!='待定':
                    house_price = int(str.strip(house_price))
                house = {
                    'house_name':str.strip(house_name),
                    'house_status':str.strip(house_status),
                    'house_addr':str.strip(house_addr),
                    'house_type':str.strip(house_type),
                    'house_tag':str.strip(house_tag),
                    'house_price':house_price,
                    'data_from':data_from
                }
                house_data.append(house)
            db = self.get_collection("jnhouse_collection")
            db.insert_many(house_data)
            print("第{}页爬取完成".format(page_no+1))

spider = jnhouse_spider()
spider.getHouseInfo()
