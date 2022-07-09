import mysql.connector

config = {
    "user": "bacchus_user",
    "password": "winesnob",
    "host": "127.0.0.1",
    "database": "bacchus",
    "raise_on_warnings": True
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
import json

with open("bacchus.json") as bacchus_json:
    bacchus = json.load(bacchus_json)

print(type(bacchus))

def insertEmployee(employee_id, employee_first_name, employee_last_name, employee_role):
        cursor.execute(f"INSERT INTO employee(employee_id, employee_first_name, employee_last_name, employee_role) VALUES({employee_first_name}, {employee_last_name}, {employee_role});")

i = 0
while i < len(bacchus["employee"]):
    employee_id = bacchus["employee"][i]["employee_id"]
    employee_first_name = bacchus["employee"][i]["employee_first_name"]
    employee_last_name = bacchus["employee"][i]["employee_last_name"]
    employee_role = bacchus["employee"][i]["employee_role"]
    insertEmployee(employee_id, employee_first_name, employee_last_name, employee_role)

    i += 1