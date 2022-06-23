'''
Taylor Reid
6/22/2022
Module 6.2
'''

#necessary imports and global variables
from pymongo import MongoClient
url = "mongodb+srv://admin:admin@cluster0.uublv.mongodb.net/pytech"
client = MongoClient(url)
db = client.pytech

#holds all of the contents of the collection since no arguments are passed
docs = db.students.find({})

print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")

#loops through all of the documents retrieved from the find({}) query and displays them nicely formatted
for doc in docs:
    print(f"Student ID:  {doc['student_id']}")
    print(f"First Name: {doc['first_name']}")
    print(f"Last Name: {doc['last_name']}")
    print()
print()

#our filter parameters that we will pass to update_one() later
filter = {"student_id" : "1007"}

#in keeping with the theme, we will change the last name to the actor's last name
newValue = {"$set":{"last_name" : "Armitage"}}

#passing arguments to update the document that matches the filter parameter to have the values of newValue
db.students.update_one(filter, newValue)

#prints out just one student record, the information from the student with a student_id of 1007
doc = db.students.find_one({"student_id": "1007"})
print("-- DISPLAYING UPDATED STUDENT DOCUMENT FROM find_one() QUERY --")
print(f"Student ID:  {doc['student_id']}")
print(f"First Name: {doc['first_name']}")
print(f"Last Name: {doc['last_name']}")
print()
print()