'''
Taylor Reid
6/22/2022
Module 6.3
'''

#necessary imports and global variables
from pymongo import MongoClient
url = "mongodb+srv://admin:admin@cluster0.uublv.mongodb.net/pytech"
client = MongoClient(url)
db = client.pytech

#turned this into a function since we're going to run this code more than once in this program
def printdb():
    #holds all of the contents of the collection since no arguments are passed
    docs = db.students.find({})

    #loops through all of the documents retrieved from the find({}) query and displays them nicely formatted
    for doc in docs:
        print(f"Student ID:  {doc['student_id']}")
        print(f"First Name: {doc['first_name']}")
        print(f"Last Name: {doc['last_name']}")
        print()
    print()

#prints the db nicely formatted
print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
printdb()

#new student
gandalf = {
        "student_id": "1010",
        "first_name": "Gandalf",
        "last_name": "the Gray"
    }

#inserts the new document and assigns its index ID to new_student_Id
new_student_Id = db.students.insert_one(gandalf).inserted_id

#prints the info for the newly inserted student
print("-- INSERT STATEMENTS --")
print(f"Inserted student record {gandalf['student_id']} into the students collection with document_id {new_student_Id}")
print()

#prints the db nicely formatted
print("-- DISPLAYING NEW STUDENT LIST DOC --")
printdb()

#our filter parameters that we will pass to delete_one()
filter = {"student_id" : "1010"}

#deletes record that matches the filter variable
db.students.delete_one(filter)

#prints the db nicely formatted
print(f"-- DELETED STUDENT ID: {filter['student_id']} --")
printdb()