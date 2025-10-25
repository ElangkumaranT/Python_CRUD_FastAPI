# database.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client[os.getenv("DATABASE_NAME")]  # Database
student_collection = db[os.getenv("COLLECTION_NAME")]  # Collection
