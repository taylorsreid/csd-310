#You can ignore this file.  I used to to reset the original value of student_id 1007 during testing.

#necessary imports and global variables
from pymongo import MongoClient
url = "mongodb+srv://admin:admin@cluster0.uublv.mongodb.net/pytech"
client = MongoClient(url)
db = client.pytech

filter = {"student_id" : "1007"}
newValue = {
    "$set":{
        "first_name" : "Thorin",
        "last_name" : "Oakenshield"
    }
}

db.students.update_one(filter, newValue)

print(db.students.find_one({"student_id": "1007"}))