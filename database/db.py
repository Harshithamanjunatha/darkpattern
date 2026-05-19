from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

clickstream_collection = db["clickstream"]
sessions_collection = db["sessions"]
alerts_collection = db["alerts"]
companies_collection = db["companies"]