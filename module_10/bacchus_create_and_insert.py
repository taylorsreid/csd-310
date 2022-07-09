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

#credentials configuration
config = {
    "user": "bacchus_user",
    "password": "winesnob",
    "host": "127.0.0.1",
    "database": "bacchus",
    "raise_on_warnings": True
}

try:
    #credentials loaded in and connection created
    db = mysql.connector.connect(**config)
    cursor = db.cursor() 

    def insertVendor(vendor_name):
        cursor.execute(f"INSERT INTO vendor(vendor_id, vendor_name) VALUES({vendor_name});")

    def insertSupply(supply_name, supply_price, vendor_id):
        cursor.execute(f"INSERT INTO supply(supply_name, supply_price, vendor_id) VALUES({supply_name}, {supply_price}, {vendor_id});")

    def insertSupplyOrders(order_date, promised_delivery_date, actual_delivery_date, order_price, vendor_id):
        cursor.execute(f"INSERT INTO supply_orders(order_date, promised_delivery_date, actual_delivery_date, order_price, vendor_id) VALUES({order_date}, {promised_delivery_date}, {actual_delivery_date}, {order_price}, {vendor_id});")

    def insertEmployee(employee_first_name, employee_last_name, employee_role):
        cursor.exectue(f"INSERT INTO employee(employee_first_name, employee_last_name, employee_role) VALUES({employee_first_name}, {employee_last_name}, {employee_role});")


    #creates a table with a list of vendors
    cursor.execute("CREATE TABLE vendor(vendor_id INT NOT NULL AUTO_INCREMENT, vendor_name VARCHAR(75) NOT NULL, PRIMARY KEY(vendor_id);")

    #creates a table with a list of supplies
    cursor.execute("CREATE TABLE supply(supply_id INT NOT NULL AUTO_INCREMENT, supply_name VARCHAR(75) NOT NULL, supply_price DECIMAL, vendor_id INT NOT NULL, PRIMARY KEY(supply_id), CONSTRAINT fk_vendor_id FOREIGN KEY(vendor_id) REFERENCES vendor(vendor_id);")

    #creates a table for supply orders
    cursor.execute("CREATE TABLE supply_orders(order_id INT NOT NULL AUTO_INCREMENT, order_date DATE, promised_delivery_date DATE NOT NULL, actual_delivery_date DATE, order_price DECIMAL NOT NULL, vendor_id INT NOT NULL, PRIMARY KEY(order_id), CONSTRAINT fk_vendor_id FOREIGN KEY(vendor_id) REFERENCES vendor(vendor_id);")

    #creates the employee table
    cursor.execute("CREATE TABLE employee(employee_id INT NOT NULL AUTO_INCREMENT, employee_first_name VARCHAR(75) NOT NULL, employee_last_name VARCHAR(75) NOT NULL, employee_role VARCHAR(75) NOT NULL, PRIMARY KEY(employee_id);")
    
    #time to start filling the tables

    #inserts vendors
    
        #cursor.execute(f"INSERT INTO vendor(name) VALUES('{vendor}');")

    #commits and closes connections
    db.commit()
    db.close()
    
    #holds the command line open
    input("Press any key to continue...")

#in case there's a connection error
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")

    else:
        print(err)