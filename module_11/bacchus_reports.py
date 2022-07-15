
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
    yn = input("\nDo you wish to generate a CSV file of the report as well? [y/n]:  ").lower()
    
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
        df.columns = getColumnNames(tableName)

        #formatting to make the dataframe look pretty
        pandas.set_option('display.width', 1000)
        pandas.set_option('display.colheader_justify', 'right')

        #prints out the title of the report and the report
        print(f"\n\t\t--- {dfTitle} ---\n")
        print(df.to_string(index=False))

        #asks if the user wants a copy of the report in CSV format too
        xchn = input("\nDo you wish to generate a CSV or HTML copy of the report?  Or none? [c/h/n]:  ").lower()
        if xchn == "c":
            df.to_csv(f"{dfTitle}.csv", index=False)
            print(f"\nCSV file written to {dfTitle}.csv in the same directory as this program.")
        elif xchn == "h":
            df.to_html(f"{dfTitle}.html", index=False)
            print(f"\nHTML file written to {dfTitle}.html in the same directory as this program.")

    except ImportError as err:
        print(err)
        print("\nYou need to run \"pip install pandas\" to view this report!")
    
    except Exception as err:
        print(err)
 
    #holds the command line open for viewing the report
    input("\nPress enter to exit to the main menu...")

#################### BEGIN MAIN METHOD ####################

cursor.execute("USE bacchus;")

#variable to control the main loop
masterControl = True

#keeps the program running until the user exits
while masterControl:

    #welcome message and menu
    clearScreen()
    print("\nWelcome to Bacchus Business Reports!")
    print("\nDeveloped by James Brown, Joshua Frazier, Christopher McCracken, and Taylor Reid")
    print("\nThe following reports are available:")
    print("\n\t1 - Late Supply Orders")
    print("\n\t2 - All Wines Sold / by Distributor")
    print("\n\t3 - Total Wines Sold by Wine Type")
    print("\n\t4 - Employee Quarterly Hours Report")
    print("\n\t5 - Exit\n")
    selection = input("Please enter the corresponding number of your selection:  ")

    #picks method based on user input
    if selection == "1":
        clearScreen()
        print("\n1 - List (plain Python, does not require pandas library)\n\n2 - Pandas Table (requires pandas library)\n")
        tl = input("View it as a pandas table or a list (list does not require pandas) [1/2]:  ").lower()
        clearScreen()
        if tl == "1":
            supplyOverdue("OVERDUE SUPPLIES")
        elif tl == "2":
            pdTable("supply_overdue", "OVERDUE SUPPLIES")

    elif selection == "2":
        clearScreen()
        pdTable("sales_all", "ALL WINES SOLD / BY DISTRIBUTOR")

    elif selection == "3":
        clearScreen()
        pdTable("sales_totals_by_wine", "SALES TOTALS BY WINE")

    elif selection == "4":
        clearScreen()
        pdTable("employee", "ALL EMPLOYEE HOURS")
    elif selection == "5":
        clearScreen()
        print("\nGoodbye and thank you for using Bacchus Business Reports!\n")
        masterControl = False
#################### END MAIN METHOD ####################

#closes connection and holds the command line open for viewing
db.close()