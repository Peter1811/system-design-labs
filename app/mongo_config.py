import os

from dotenv import load_dotenv
from pymongo import MongoClient

MONGODB_URL = 'mongodb://mongo:27017/'

mongo_client = MongoClient(MONGODB_URL)

mongo_presentations = mongo_client['conference']['presentations']
