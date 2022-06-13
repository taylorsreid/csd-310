from pymongo import MongoClient
url = "mongodb+srv://admin:admin@cluster0.uublv.mongodb.net/pytech"
client = MongoClient(url)
db = client.pytech
print(db.list_collection_names())