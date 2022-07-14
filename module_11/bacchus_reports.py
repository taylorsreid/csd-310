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
from connect import db, cursor
import tables
from os import system, name


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

#
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
def getColumnNames(tableName):
    cursor.execute(f"SHOW COLUMNS FROM {tableName};")
    results = cursor.fetchall()
    columnNames = []
    i = 0
    while i < len(results):
        columnNames.append(results[i][0])
        i += 1
    return columnNames

#
def supplyOverdue(reportTitle):

    #asks if the user wants a copy of the report in CSV format too
    yn = input("Do you wish to generate a CSV file of the report as well? [y/n]:  ").lower()
    
    clearScreen()

    #pulls the view
    cursor.execute("SELECT * FROM supply_overdue;")
    orders = cursor.fetchall()

    #formatting string for dates
    dateFormat = "%B %d, %Y"

    #
    if yn == "y":
        createCsv(f"{reportTitle}.csv", "VENDOR NAME, ORDER DATE, PROMISED DATE, ACTUAL DELIVERY DATE, DAYS OVERDUE")

    print(f"\t\t{reportTitle}")

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
            writeCsv(f"{reportTitle}.csv", line)

    #
    if yn == "y":
        print(f"\nCSV file written to {reportTitle} in the same directory as this program.")

    #holds the command line open for viewing the report
    input("\nPress enter to exit to the main menu...")

# 
def pdTable(tableName, dfTitle):

    #executes SQL
    cursor.execute(f"SELECT * FROM {tableName}")

    #under a try block in case the user didn't pip install pandas
    try:
        import pandas

        #loads results of SQL query into a pandas dataframe for later viewing
        df = pandas.DataFrame(cursor.fetchall())
        
        #retrieves names of columns from MySQL and sets the dataframe's to match
        columnNames = getColumnNames(tableName)
        df.columns = columnNames

        #
        bottomTotals = []

        #determines the type of each column, if it's an int then it can be summed
        i = 0
        while i < len(columnNames):
            cursor.execute(f"""
                SELECT DATA_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE 
                    TABLE_SCHEMA = 'bacchus' AND
                    TABLE_NAME   = '{tableName}' AND 
                    COLUMN_NAME  = '{columnNames[i]}'
                """)
            columnType = cursor.fetchall()[0][0]

            if columnType == "int":
                if "_id" not in columnNames[i]:
                    cursor.execute(f"SELECT SUM({columnNames[i]}) FROM {tableName};")
                    cell = cursor.fetchall()[0][0]
                    bottomTotals.append(cell)
                else:
                    bottomTotals.append("")
            else:
                bottomTotals.append("")

            i += 1

        bottomDivider = []
        topDivider = []
        for f in columnNames:
            bottomDivider.append("-" * len(f))
            topDivider.append("-" * len(f))
        
        #adds dividers and sorts it
        df.loc[len(df.index)] = bottomDivider
        df.loc[-1] = topDivider
        df.sort_index(inplace=True)

        #appends the totals of the columns to the bottom row
        df.loc[len(df.index)] = bottomTotals
        

        #
        print(f"\n\t\t\t\t--- {dfTitle} ---\n")
        print(df.to_string(index=False))

        #asks if the user wants a copy of the report in CSV format too
        yn = input("\nDo you wish to generate a CSV file of the report as well? [y/n]:  ").lower()
        if yn == "y":
            df.to_csv(f"{dfTitle}.csv", index=False)
            print(f"\nCSV file written to {dfTitle} in the same directory as this program.")

    except ImportError as err:
        print(err)
        print("\nYou need to run \"pip install pandas\" to view this report!")
    
    except Exception as err:
        print(err)
 
    #holds the command line open for viewing the report
    input("\nPress enter to exit to the main menu...")

#################### BEGIN MAIN METHOD ####################

#creates necessary views in MySQL if they haven't been already
tables.update()

#
masterControl = True
#
while masterControl:

    #
    clearScreen()
    print("\nWelcome to Bacchus Business Reports!")
    print("\n1 - Late Supply Orders Report\n\n2 - Wines Sold Report\n\n3 - Employee Quarterly Hours Report\n\n4 - Exit\n")
    selection = input("Please enter the corresponding number of your selection:  ")

    #
    if selection == "1":
        clearScreen()
        tl = input("View it as a pandas table or a list (list does not require pandas) [t\l]:  ").lower()
        clearScreen()
        if tl == "t":
            pdTable("supply_overdue", "OVERDUE SUPPLIES")
        elif tl == "l":
            supplyOverdue("OVERDUE SUPPLIES")
    elif selection == "2":
        clearScreen()
        pdTable("sales_all", "ALL SALES")
    elif selection == "3":
        clearScreen()
        pdTable("employee", "ALL EMPLOYEE HOURS")
    elif selection == "4":
        clearScreen()
        print("\nGoodbye and thank you for using Bacchus Business Reports!\n")
        masterControl = False
#################### END MAIN METHOD ####################

#closes connection and holds the command line open for viewing
db.close()