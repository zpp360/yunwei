# coding = utf-8
import pymysql
class my_db:
    def __init__(self,host,user,passwd,db,port,charset):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset

    def get_connection(self):
        conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port, charset=self.charset)
        return conn

    def get_cursor(self,conn):
        cur = conn.cursor()
        return cur

    def insert_region_dict(self,region_dict):
        conn = self.get_connection()
        cur = self.get_cursor(conn)
        insert_sql = "insert into m_region_copy(region_code,region_name,p_code,p_name) values"
        param = ""
        for county_code in region_dict.keys():
            county_region = region_dict.get(county_code)
            param = param + "('{}','{}','{}','{}'),".format(county_region.code, county_region.name, county_region.parent_code, county_region.parent_name)
        param = param[0:len(param) - 1] + ""
        insert_sql = insert_sql + param
        print(insert_sql)
        cur.execute(insert_sql)
        conn.commit()

        cur.close()
        conn.close()