from pymongo import MongoClient
from config.config import get_config

def get_mongo_client(collection_name: str):
    conn = MongoClient(get_config().get('MONGO_URI'))
    db = conn['EchoChronicles']
    coll = db[collection_name]
    return conn, coll
