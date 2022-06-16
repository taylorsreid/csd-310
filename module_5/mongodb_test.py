"""
Taylor Reid
6/15/2022
Module 5.2
"""

from pymongo import MongoClient
url = "mongodb+srv://admin:admin@cluster0.uublv.mongodb.net/pytech"
client = MongoClient(url)
db = client.pytech
print(db.list_collection_names())