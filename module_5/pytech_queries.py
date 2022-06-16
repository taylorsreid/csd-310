"""
Taylor Reid
6/15/2022
Module 5.3
"""

#necessary imports and global variables
from pymongo import MongoClient
url = "mongodb+srv://admin:admin@cluster0.uublv.mongodb.net/pytech"
client = MongoClient(url)
db = client.pytech

docs = db.students.find({})

print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
for doc in docs:
    print(f"Student ID:  {doc['student_id']}")
    print(f"First Name: {doc['first_name']}")
    print(f"Last Name: {doc['last_name']}")
    print()
print()

doc = db.students.find_one({"student_id": "1007"})
print("-- DISPLAYING STUDENT DOCUMENTS FROM find() QUERY --")
print(f"Student ID:  {doc['student_id']}")
print(f"First Name: {doc['first_name']}")
print(f"Last Name: {doc['last_name']}")
print()
print()