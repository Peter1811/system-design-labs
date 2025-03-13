import os

from dotenv import load_dotenv
from pymongo import MongoClient

MONGODB_URL = 'mongodb://mongo:27017/'

mongo_client = MongoClient(MONGODB_URL)

def get_mongo():
    db = mongo_client['conference']
    collection = db['presentations']
    try:
        yield collection
    finally:
        pass
