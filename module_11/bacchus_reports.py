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
#import datetime

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
def overdueCsv():
    pass

overdueSql = """
    SELECT order_date, promised_delivery_date, actual_delivery_date, supply_order.vendor_id, vendor_name 
    FROM supply_order 
    INNER JOIN vendor ON supply_order.vendor_id = vendor.vendor_id
    WHERE actual_delivery_date > promised_delivery_date;
"""


cursor.execute(overdueSql)
results = cursor.fetchall()

#order_date = results[0][0]
#print(order_date.year)


for result in results:
    print(f"Ordered date: {result[0].month}/{result[0].day}/{result[0].year}")


#closes connection and holds the command line open for viewing
db.close()
input("Press enter to continue...")