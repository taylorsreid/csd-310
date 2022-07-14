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
from re import I
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

#gets and returns column names
def getColumnNames(viewName):
    cursor.execute(f"SHOW COLUMNS FROM {viewName};")
    results = cursor.fetchall()
    columnNames = []
    i = 0
    while i < len(results):
        columnNames.append(results[i][0])
        i += 1
    return columnNames

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
def pdTable(viewName, dfTitle, startIndex):

    try:
        
        if viewName == "sales_all":
            #creates a view of sales numbers by wine and distributor for easier use later on
            cursor.execute(f"""
                            CREATE VIEW {viewName} AS
                            SELECT sales.distributor_id, distributor_name, merlot, cabernet, chablis, chardonnay FROM sales
                            INNER JOIN distributor ON sales.distributor_id = distributor.distributor_id
                            ORDER BY sales.distributor_id ASC;
                            """)        
        
        elif viewName == "hours_all":
            #
            cursor.execute(f"""
                            CREATE VIEW {viewName} AS
                            SELECT * FROM employee
                            ORDER BY employee_id ASC;
                            """)

    except:
        #I intentionally want this exception to pass silently
        pass

    #in case the user didn't install pandas as instructed
    try:
        import pandas

        #gets the entire SQL view, puts it into a pandas data frame
        cursor.execute(f"SELECT * FROM {viewName};")
        results = cursor.fetchall()
        df = pandas.DataFrame(results)

        #assigns the dataframe columns names to the same as the column names in the view
        df.columns = getColumnNames(f"{viewName}")

        #creates the last row of our dataframe, appends enough blank cells to make them line up with the others by using a loop and the startIndex
        lastRow = []
        i = 1
        while i < startIndex:
            lastRow.append("")
            i += 1
        lastRow.append("TOTAL:")
        
        #appends the sum of the columns to lastRow
        i = startIndex
        while i < len(df.columns):
            cursor.execute(f"""
                            SELECT SUM({df.columns[i]})
                            FROM {viewName}
                            """)
            results = cursor.fetchall()
            lastRow.append(int(results[0][0]))
            i += 1

        #both exactly what they sound like
        horizontalDivider = []
        verticalDivider = []

        i = 0
        while i < len(df.columns):
            if i < startIndex:
                horizontalDivider.append("")
            else:
                horizontalDivider.append("----")
            i += 1

        df.loc[len(df.index)] = horizontalDivider
        
        #appends lastRow to the dataframe
        df.loc[len(df.index)] = lastRow
        
        #finally, we get to print the title of the report and the actual dataframe
        print(f"\n\t\t\t\t--- {dfTitle} ---\n")
        print(df.to_string(index=False))

        


    except ImportError as err:
        print(err)
        print("\nYou need to run \"pip install pandas\" to view this report!")
    
    except Exception as err:
        print(err)
 
    #holds the command line open for viewing the report
    input("\nPress enter to exit to the main menu...")

#################### BEGIN MAIN METHOD ####################
#
masterControl = True
#
while masterControl:

    #
    clearScreen()
    print("Welcome to Bacchus Business Reports!")
    print("\n1 - Late Supply Orders Report\n\n2 - Wines Sold Report\n\n3 - Employee Quarterly Hours Report\n\n4 - Exit\n")
    selection = input("Please enter the corresponding number of your selection:  ")

    #
    if selection == "1":
        clearScreen()
        supplyOverdue()
    elif selection == "2":
        clearScreen()
        pdTable("sales_all", "ALL SALES", 2)
    elif selection == "3":
        clearScreen()
        pdTable("hours_all", "ALL EMPLOYEE HOURS", 4)
    elif selection == "4":
        clearScreen()
        print("Goodbye!")
        masterControl = False
#################### END MAIN METHOD ####################

#closes connection and holds the command line open for viewing
db.close()