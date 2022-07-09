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
    
    #creates the employee table
    cursor.execute("CREATE TABLE employee(employee_id INT NOT NULL AUTO_INCREMENT, first_name VARCHAR(75) NOT NULL, last_name VARCHAR(75) NOT NULL, PRIMARY KEY(employee_id)")

    #creates a table with a list of suppliers
    cursor.execute("CREATE TABLE supplier(supplier_id INT NOT NULL AUTO_INCREMENT, name VARCHAR(75) NOT NULL, PRIMARY KEY(supplier_id)")

    #creates a table with a list of supplies
    cursor.execute("CREATE TABLE supply(supply_id INT NOT NULL AUTO_INCREMENT, name VARCHAR(75) NOT NULL, PRIMARY KEY(supply_id)")
    
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