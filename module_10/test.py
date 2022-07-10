'''
IGNORE THIS FILE
IT'S JUST FOR TESTING SNIPPETS OF CODE
'''

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

i = 0
while i < len(bacchus["vendor"]):
    vendor_id = bacchus["vendor"][i]["vendor_id"]
    vendor_name = bacchus["vendor"][i]["vendor_name"]

    print(str(vendor_id) + vendor_name + str(i))

    cursor.execute(f"INSERT INTO vendor(vendor_id, vendor_name) VALUES('{vendor_id}', '{vendor_name}');")

    i += 1

db.commit()