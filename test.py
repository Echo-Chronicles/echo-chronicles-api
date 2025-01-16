from pymongo import MongoClient
conn = MongoClient('mongodb://admin:password@93.127.199.229:27017/')
db = conn['EchoChronicles']



conn_ser = MongoClient('mongodb://echo:password12@178.128.94.112:27017/')
db_ser = conn_ser['EchoChronicles']

for coll in db.list_collection_names():
    for doc in db[coll].find():
        db_ser[coll].insert_one(doc)
        print("====================================")