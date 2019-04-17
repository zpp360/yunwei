# coding = utf-8
from db.my_db import my_db
from region import region

my_db = my_db('192.168.0.116', 'root', 'sh123456', 'shuheng', 3306, 'utf8')
city_dict = {}
re = region()
re.code = '370900000000'
re.name = '泰安市'
re.parent_name = '山东省'
re.parent_code = '370000000000'
city_dict[re.code] = re
my_db.insert_region_dict(city_dict)