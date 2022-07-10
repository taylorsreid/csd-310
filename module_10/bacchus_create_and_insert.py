'''
Red Team
    James Brown
    Joshua Frazier
    Christopher McCracken
    Taylor Reid
7/8/2022
Module 10.3
'''

#library imports
import mysql.connector
from mysql.connector import errorcode
import json

#credentials configuration
config = {
    "user": "bacchus_user",
    "password": "winesnob",
    "host": "127.0.0.1",
    "database": "bacchus",
    "raise_on_warnings": True
}

#the python script would be incredibly long and messy if I put all of the values to insert into it
#instead I put them into a JSON file
try:
    with open("bacchus.json") as bacchus_json:
        bacchus = json.load(bacchus_json)
except:
    print("Failed to open the JSON file, please ensure that it is in the same directory as this script and that you are running this script from the command line and not your IDE.")

#makes a connection to MySQL
try:
    #credentials loaded in and connection created
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    print("\nConnected to MySQL Database.")

#in case there's a connection error
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")

    else:
        print(err)

print("\nCreating tables:")

#creates a table with a list of vendors
cursor.execute("CREATE TABLE vendor(vendor_id INT NOT NULL, vendor_name VARCHAR(75) NOT NULL, PRIMARY KEY(vendor_id));")
print("\tvendor")

#creates the employee table
cursor.execute("CREATE TABLE employee(employee_id INT NOT NULL, employee_first_name VARCHAR(75) NOT NULL, employee_last_name VARCHAR(75) NOT NULL, employee_role VARCHAR(75) NOT NULL, q1_hours INT NOT NULL, q2_hours INT NOT NULL, q3_hours INT NOT NULL, q4_hours INT NOT NULL, PRIMARY KEY(employee_id));")
print("\temployee")

#creates a table with distributors
cursor.execute("CREATE TABLE distributor(distributor_id INT NOT NULL, distributor_name VARCHAR(75) NOT NULL, PRIMARY KEY(distributor_id));")
print("\tdistributor")

#creates a table to hold the LAST MONTH'S sales
cursor.execute("CREATE TABLE sales(distributor_id INT NOT NULL, merlot VARCHAR(75) NOT NULL, cabernet VARCHAR(75) NOT NULL, chablis VARCHAR(75) NOT NULL, chardonnay VARCHAR(75) NOT NULL, CONSTRAINT fk_distributor_id FOREIGN KEY(distributor_id) REFERENCES distributor(distributor_id), PRIMARY KEY(distributor_id));")
print("\tsales")

#creates a table with a list of supplies
cursor.execute("CREATE TABLE supply(supply_id INT NOT NULL, supply_name VARCHAR(75) NOT NULL, supply_price DOUBLE, vendor_id INT NOT NULL, PRIMARY KEY(supply_id), CONSTRAINT fk_supply_vendor_id FOREIGN KEY(vendor_id) REFERENCES vendor(vendor_id));")
print("\tsupply")

#creates a table for supply orders
cursor.execute("CREATE TABLE supply_order(order_date DATE NOT NULL, promised_delivery_date DATE NOT NULL, actual_delivery_date DATE, order_price DOUBLE NOT NULL, vendor_id INT NOT NULL, PRIMARY KEY(order_date), CONSTRAINT fk_order_vendor_id FOREIGN KEY(vendor_id) REFERENCES vendor(vendor_id));")
print("\tsupply_orders")

#time to start filling the tables
print("\nFilling SQL tables with values from bacchus.json:")

#fills the vendor table from the JSON file
i = 0
while i < len(bacchus["vendor"]):
    vendor_id = bacchus["vendor"][i]["vendor_id"]
    vendor_name = bacchus["vendor"][i]["vendor_name"]
    cursor.execute(f"INSERT INTO vendor(vendor_id, vendor_name) VALUES('{vendor_id}', '{vendor_name}');")
    i += 1
print("\tvendor")

#fills the employee table from the JSON file
i = 0
while i < len(bacchus["employee"]):
    employee_id = bacchus["employee"][i]["employee_id"]
    employee_first_name = bacchus["employee"][i]["employee_first_name"]
    employee_last_name = bacchus["employee"][i]["employee_last_name"]
    employee_role = bacchus["employee"][i]["employee_role"]

    q1_hours = bacchus["employee"][i]["q1_hours"]
    q2_hours = bacchus["employee"][i]["q2_hours"]
    q3_hours = bacchus["employee"][i]["q3_hours"]
    q4_hours = bacchus["employee"][i]["q4_hours"]

    cursor.execute(f"INSERT INTO employee(employee_id, employee_first_name, employee_last_name, employee_role, q1_hours, q2_hours, q3_hours, q4_hours) VALUES('{employee_id}', '{employee_first_name}', '{employee_last_name}', '{employee_role}', '{q1_hours}', '{q2_hours}', '{q3_hours}', '{q4_hours}');")
    i += 1
print("\temployee")

#fills the distributor table from the JSON file
i = 0
while i < len(bacchus["distributor"]):
    distributor_id = bacchus["distributor"][i]["distributor_id"]
    distributor_name = bacchus["distributor"][i]["distributor_name"]
    cursor.execute(f"INSERT INTO distributor(distributor_id, distributor_name) VALUES('{distributor_id}', '{distributor_name}');")
    i += 1
print("\tdistributor")

#fills the sales table from the JSON file
i = 0
while i < len(bacchus["sales"]):
    distributor_id = bacchus["sales"][i]["distributor_id"]
    merlot = bacchus["sales"][i]["merlot"]
    cabernet = bacchus["sales"][i]["cabernet"]
    chablis = bacchus["sales"][i]["chablis"]
    chardonnay = bacchus["sales"][i]["chardonnay"]
    cursor.execute(f"INSERT INTO sales(distributor_id, merlot, cabernet, chablis, chardonnay) VALUES('{distributor_id}', '{merlot}', '{cabernet}', '{chablis}', '{chardonnay}');")
    i += 1
print("\tsales")

#fills the supply table from the JSON file
i = 0
while i < len(bacchus["supply"]):
    supply_id = bacchus["supply"][i]["supply_id"]
    supply_name = bacchus["supply"][i]["supply_name"]
    supply_price = bacchus["supply"][i]["supply_price"]
    vendor_id = bacchus["supply"][i]["vendor_id"]
    cursor.execute(f"INSERT INTO supply(supply_id, supply_name, supply_price, vendor_id) VALUES('{supply_id}', '{supply_name}', '{supply_price}', '{vendor_id}');")
    i += 1
print("\tsupply")

#fills the supply order table from the JSON file
i = 0
while i < len(bacchus["supply_order"]):
    order_date = bacchus["supply_order"][i]["order_date"]
    order_date = bacchus["supply_order"][i]["order_date"]
    promised_delivery_date = bacchus["supply_order"][i]["promised_delivery_date"]
    actual_delivery_date = bacchus["supply_order"][i]["actual_delivery_date"]
    order_price = bacchus["supply_order"][i]["order_price"]
    vendor_id = bacchus["supply_order"][i]["vendor_id"]
    cursor.execute(f"INSERT INTO supply_order(order_date, promised_delivery_date, actual_delivery_date, order_price, vendor_id) VALUES('{order_date}', '{promised_delivery_date}', '{actual_delivery_date}', '{order_price}', '{vendor_id}');")
    i += 1
print("\tsupply_order")

#commits and closes connections
db.commit()
db.close()

#holds the command line open for viewing
print(f"\nSuccessfully comitted to {config['database']} database!")
input("Press enter to continue...")