'''
Red Team
    James Brown
    Joshua Frazier
    Christopher McCracken
    Taylor Reid
7/11/2022
Module 11.1
'''

#library imports
import mysql.connector
from mysql.connector import errorcode
import datetime

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

#writes a csv file of overdue orders
def writeCsv():
    pass

def supplyOverdue():

    #welcome message that also asks if the user wants a copy of the report in CSV format too
    print("This report will show all overdue supply shipments in the database.")
    yn = input("Do you wish to generate a CSV file as well? [y/n]").lower()
    
    #creates a view of overdue supply shipments that is easier to work with later on
    try:
        cursor.execute(f"""CREATE VIEW supply_overdue AS 
                           SELECT order_date, promised_delivery_date, actual_delivery_date, vendor_name 
                           FROM supply_order 
                           INNER JOIN vendor ON supply_order.vendor_id = vendor.vendor_id
                           WHERE actual_delivery_date > promised_delivery_date;
                        """)
        print("supply_overdue view created\n")
    except:
        print("supply_overdue view already exists, continuing...\n")

    #pulls the view
    cursor.execute("SELECT * FROM supply_overdue;")
    orders = cursor.fetchall()

    #formatting string for dates
    format = "%B %d, %Y"

    #
    for order in orders:
        vendorName = order[0]
        orderDate = order[0].strftime(format)
        promisedDate = order[1].strftime(format)
        actualDate = order[2].strftime(format)
        daysOverdue = order[2] - order[1]

        print(f"Vendor Name         : {vendorName}")
        print(f"Order Date          : {orderDate}")
        print(f"Promised Date       : {promisedDate}")
        print(f"Actual Delivery Date: {actualDate}")
        print(f"Days Overdue        : {daysOverdue}")
        print()



#MAIN
supplyOverdue()
#/MAIN

#closes connection and holds the command line open for viewing
db.close()
#input("Press enter to continue...")