'''
Taylor Reid
6/15/2022
Module 5.3
'''

#necessary imports and global variables
from pymongo import MongoClient
url = "mongodb+srv://admin:admin@cluster0.uublv.mongodb.net/pytech"
client = MongoClient(url)
db = client.pytech

#easier and more scalable to use a list than three individual variables
listOfStudents =[
    {
        "student_id": "1007",
        "first_name": "Thorin",
        "last_name": "Oakenshield"
    },

    {
        "student_id": "1008",
        "first_name": "Bilbo",
        "last_name": "Baggins"
    },

    {
        "student_id": "1009",
        "first_name": "Frodo",
        "last_name": "Baggins"
    }
]

#faster and more scalable to use a for loop than to write each statement individually
print("-- INSERT STATEMENTS --")
for student in listOfStudents:
    new_student_Id = db.students.insert_one(student).inserted_id
    print(f"Inserted student record {student['first_name']} {student['last_name']} into the students collection with document_id {str(new_student_Id)}")