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
from os import system, name

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

##################################################################################################

#clears the screen and makes everything look pretty
def clearScreen():
    try:
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
    except:
        pass

def createCsv(csvFileName, header):
    with open(csvFileName, "w") as file:
        file.write(header + "\n")

#writes a csv file of overdue orders
def writeCsv(csvFileName, line):
    with open(csvFileName, "a") as file:
        i = 0
        while i < (len(line) - 1):
            file.write(str(line[i]) + ", ")
            i += 1
        file.write(str(line[-1]) + "\n")

def supplyOverdue():

    #
    csvFileName = "Overdue_Supplies.csv"

    #welcome message that also asks if the user wants a copy of the report in CSV format too
    print("This report will show all overdue supply shipments in the database.")
    yn = input("Do you wish to generate a CSV file as well? [y/n]:  ").lower()
    
    #creates a view of overdue supply shipments that is easier to work with later on
    try:
        cursor.execute(f"""CREATE VIEW supply_overdue AS 
                           SELECT order_date, promised_delivery_date, actual_delivery_date, vendor_name 
                           FROM supply_order 
                           INNER JOIN vendor ON supply_order.vendor_id = vendor.vendor_id
                           WHERE actual_delivery_date > promised_delivery_date;
                        """)
    except:
        #I intentionally want this exception to pass silently
        pass

    #pulls the view
    cursor.execute("SELECT * FROM supply_overdue;")
    orders = cursor.fetchall()

    #formatting string for dates
    dateFormat = "%B %d, %Y"

    #
    if yn == "y":
        createCsv(csvFileName, "VENDOR NAME, ORDER DATE, PROMISED DATE, ACTUAL DELIVERY DATE, DAYS OVERDUE")

    #
    for order in orders:

        #
        vendorName = order[3]
        orderDate = order[0]
        promisedDate = order[1]
        actualDate = order[2]
        daysOverdue = order[2] - order[1]
        daysOverdue = daysOverdue.days

        #
        print()
        print(f"Vendor Name         : {vendorName}")
        print(f"Order Date          : {orderDate.strftime(dateFormat)}")
        print(f"Promised Date       : {promisedDate.strftime(dateFormat)}")
        print(f"Actual Delivery Date: {actualDate.strftime(dateFormat)}")
        print(f"Days Overdue        : {daysOverdue}")

        #
        if yn == "y":
            line = [vendorName, orderDate, promisedDate, actualDate, daysOverdue]
            writeCsv(csvFileName, line)

    #
    if yn == "y":
        print(f"\nCSV file written to {csvFileName} in the same directory as this program.")

    #holds the command line open for viewing the report
    input("\nPress enter to exit to the main menu...")

# 
def getMaxMin(maxOrMin, wineName):
    maxMinQuery = f"""SELECT MAX(merlot), distributor_name
                      FROM sales
                      INNER JOIN distributor
                      ON sales.distributor_id = distributor.distributor_id;
                   """


# 
def winesSold():
    
    cursor.execute("SHOW COLUMNS FROM bacchus.sales;")
    results = cursor.fetchall()
    wineNames = []
    #for result in results:
    #    print(result[0])
     
    i = 1
    while i < len(results):
        print(results[i][0])
        wineNames.append(results[i][0])
        i += 1





    # 
    
    
    #holds the command line open for viewing the report
    input("\nPress enter to exit to the main menu...")

########## BEGIN MAIN METHOD ##########
#
masterControl = True
#
while masterControl:

    #
    clearScreen()
    print("Welcome to Bacchus Business Reports!")
    print("\n1 - Overdue Supply Orders\n\n2 - Wines Sold Report\n\n3 - SOMETHING ELSE\n\n4 - Exit\n")
    selection = input("Please enter the corresponding number of your selection:  ")

    #
    if selection == "1":
        clearScreen()
        supplyOverdue()
    elif selection == "2":
        clearScreen()
        winesSold()
    elif selection == "3":
        pass
    elif selection == "4":
        clearScreen()
        print("Goodbye!")
        masterControl = False
########## END MAIN METHOD ##########

#closes connection and holds the command line open for viewing
db.close()