'''
Red Team
    James Brown
    Joshua Frazier
    Christopher McCracken
    Taylor Reid
7/10/2022
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

#makes a connection to MySQL
try:
    #credentials loaded in and connection created
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    print("\nConnected to MySQL Database.\n")
#in case there's a connection error
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")
    else:
        print(err)

#displays the vendor table
    print("\t\t-- VENDOR TABLE --\n")
    cursor.execute("SELECT * FROM vendor")
    vendors = cursor.fetchall()
    for vendor in vendors:
        print(f"Vendor ID: {vendor[0]}")
        print(f"Vendor Name: {vendor[1]}")
        print()

#displays the employee table
print("\t\t-- EMPLOYEE TABLE --\n")
cursor.execute("SELECT * FROM employee")
employees = cursor.fetchall()
for employee in employees:
    print(f"Employee ID: {employee[0]}")
    print(f"First Name: {employee[1]}")
    print(f"Last Name: {employee[2]}")
    print(f"Role: {employee[3]}")
    print(f"Hours per quarter in the last year: \n\tQ1: {employee[4]} | Q2: {employee[5]} | Q3: {employee[6]} | Q4: {employee[7]}")
    print()

#displays the distributor table
print("\t\t-- DISTRIBUTOR TABLE --\n")
cursor.execute("SELECT * FROM distributor")
distributors = cursor.fetchall()
for distributor in distributors:
    print(f"Distributor ID: {distributor[0]}")
    print(f"Distributor Name: {distributor[1]}")
    print()

#displays the sales table
print("\t\t-- SALES TABLE --\n")
cursor.execute("SELECT merlot, cabernet, chablis, chardonnay, sales.distributor_id, distributor_name FROM sales INNER JOIN distributor ON sales.distributor_id = distributor.distributor_id;")
sales = cursor.fetchall()
for sale in sales:
    print(f"Distributor ID: {sale[4]}")
    print(f"Distributor name: {sale[5]} [INNER JOIN]")
    print("Sales in bottles in the last month:")
    print(f"\tMerlot: {sale[0]} | Cabernet: {sale[1]} | Chablis: {sale[2]} | Chardonnay: {sale[3]}")
    print()

#displays the supply table
print("\t\t-- SUPPLY TABLE --\n")
cursor.execute("SELECT supply_id, supply_name, supply_price, supply.vendor_id, vendor_name FROM supply INNER JOIN vendor ON supply.vendor_id = vendor.vendor_id;")
supplies = cursor.fetchall()
for supply in supplies:
    print(f"Supply ID: {supply[0]}")
    print(f"Supply Name: {supply[1]}")
    print(f"Supply Price: ${supply[2]}")
    print("Sold by:")
    print(f"\tVendor Name: {supply[4]} [INNER JOIN]")
    print(f"\tVendor ID: {supply[3]}")
    print()

#displays the supply_order table
print("\t\t-- SUPPLY_ORDER TABLE --\n")
cursor.execute("SELECT order_date, promised_delivery_date, actual_delivery_date, order_price, supply_order.vendor_id, vendor_name FROM supply_order INNER JOIN vendor ON supply_order.vendor_id = vendor.vendor_id;")
orders = cursor.fetchall()
for order in orders:
    print(f"Date Ordered: {order[0]}")
    print(f"Date Promised: {order[1]}")
    print(f"Date Delivered: {order[2]}")
    print(f"Order Total: ${order[3]}")
    print("Ordered from:")
    print(f"\tVendor Name: {order[5]} [INNER JOIN]")
    print(f"\tVendor ID: {order[4]}")
    print()

#closes connection and holds the command line open for viewing
db.close()
input("Press enter to continue...")