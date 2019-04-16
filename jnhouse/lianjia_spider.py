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

class lianjia_spider:
    def __init__(self):
        self.url = 'https://jn.fang.lianjia.com/loupan/nht1pg'
        self.datas = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.cookies = {
            'Cookie' : 'lianjia_uuid=1588a2ec-fc35-4c3f-96ac-056da587f02f; _ga=GA1.2.1135038770.1536558988; UM_distinctid=165c20d7aaf443-0e01deea10dfb9-323b5b03-1fa400-165c20d7ab0c70; _jzqa=1.287148108683915420.1536558984.1536558984.1536558984.1; _smt_uid=5b9607c6.4b5d270c; select_city=370101; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1536558983,1536804988; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1536804988; _jzqa=1.287148108683915420.1536558984.1536558984.1536804989.2; _jzqc=1; _jzqy=1.1536558984.1536804989.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; _jzqckmp=1; _gid=GA1.2.2052949435.1536804990; CNZZDATA1257392697=1889158887-1536557843-https%253A%252F%252Fjn.lianjia.com%252F%7C1536803901; CNZZDATA1254525948=70325977-1536553986-https%253A%252F%252Fjn.lianjia.com%252F%7C1536801211; CNZZDATA1255633284=2109983578-1536553923-https%253A%252F%252Fjn.fang.lianjia.com%252F%7C1536800167; CNZZDATA1255604082=497868371-1536555195-https%253A%252F%252Fjn.fang.lianjia.com%252F%7C1536800757; _qzjc=1; _jzqc=1; _qzja=1.147018602.1536559004916.1536559004916.1536804992954.1536805009265.1536805106531.0.0.0.11.2; _qzjto=5.1.0'
        }

    def get_db(self, db_name='jnhouse_db'):
        client = pymongo.MongoClient("mongodb://192.168.1.116:27017/")
        db = client[db_name]
        return db

    def get_collection(self, collection_name):
        db = self.get_db()
        return db[collection_name]

    def getContent(self,url):
        post = requests.get(url=url,cookies=self.cookies,headers=self.cookies,data=self.datas)
        content = post.text
        return content

    def getHouseInfo(self):
        page_total = int(input('请输入总页数\n'))
        data_from = input("请输入数据来源：\n")
        for page_no in range(page_total):
            page_no = page_no + 1
            url = self.url + str(page_no)
            print(url)
            content = self.getContent(url)
            soup = BeautifulSoup(content,'html.parser')
            house_list = soup.find_all('div',class_='resblock-desc-wrapper')
            house_datas = []
            for i in range(len(house_list)):
                house_name = str.strip(house_list[i].find('div',class_='resblock-name').find('a').text)
                house_status = str.strip(house_list[i].find('div',class_='resblock-name').find('span',class_='sale-status').text)
                house_addr = str.strip(house_list[i].find('div',class_='resblock-location').find('a').text)
                house_tag = str.strip(house_list[i].find('div',class_='resblock-tag').text)
                house_type = str.strip(house_list[i].find('div',class_='resblock-area').text)
                house_price = str.strip(house_list[i].find('div',class_='resblock-price').find('span',class_='number').text)
                if house_price!='价格待定':
                    house_price = int(str.strip(house_price))

                house_data = {
                    'house_name':house_name,
                    'house_status':house_status,
                    'house_addr':house_addr,
                    'house_tag':house_tag,
                    'house_type':house_type,
                    'house_price':house_price,
                    'data_from':data_from
                }
                print(house_data)
                house_datas.append(house_data)
            db = self.get_collection('lianjia_collection')
            db.insert_many(house_datas)



lianjia_spider = lianjia_spider()
content = lianjia_spider.getHouseInfo()
