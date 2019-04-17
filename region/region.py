# coding = utf-8
import pymysql
class region:

    def __init__(self):
        self.code = ''
        self.name = ''
        self.url = ''
        self.parent_name = ''
        self.parent_code = ''

    def __str__(self):
        return self.code + ":" +self.name + ":" +self.url + ":" + self.parent_code + ":" + self.parent_name




reg = region()
reg.code = '371703110201'
reg.name = '万庄村委会'
reg.parent_code = '371703110000'
reg.parent_name = '南王店镇'
county_dicts = {'371703002000':reg}
reg = region()
reg.code = '371703110202'
reg.name = '万庄村委会'
reg.parent_code = '371703110000'
reg.parent_name = '南王店镇'
county_dicts['371703110212'] = reg
conn = pymysql.connect(host='192.168.0.116', user='root', passwd='sh123456', db='shuheng', port=3306, charset='utf8')
cur = conn.cursor()
insert_sql = "insert into m_region(region_code,region_name,p_code,p_name) values"
param = ""
for county_code in county_dicts.keys():
    county_region = county_dicts.get(county_code)
    param = param + "('{}','{}','{}','{}'),".format(county_region.code,county_region.name,county_region.parent_code,county_region.parent_name)
param = param[0:len(param)-1] + ""
print(param)
insert_sql = insert_sql + param
print(insert_sql)
cur.execute(insert_sql)
conn.commit()

