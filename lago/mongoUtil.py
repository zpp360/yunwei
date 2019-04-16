import pymongo

def get_db(self,db_name='lago_db'):
    client = pymongo.MongoClient("mongodb://192.168.0.116:27017/")
    db = client[db_name]
    return db

def get_collection(self,collection_name):
    db = self.get_db()
    return db[collection_name]