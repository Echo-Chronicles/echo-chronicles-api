from pymongo import MongoClient

def get_mongo_client(collection_name: str):
    conn = MongoClient('mongodb://admin:password@93.127.199.229:27017/')
    db = conn['EchoChronicles']
    coll = db[collection_name]
    return conn, coll
