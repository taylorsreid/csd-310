
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
from datetime import datetime

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

#creates a CSV file for people who can't or won't pip install pandas
def createCsv(csvFileName, header):
    with open(csvFileName, "w") as file:
        file.write(header + "\n")

#writes to that csv file of overdue orders
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

#prints out a report of overdue supply shipments for people who aren't using pandas
def supplyOverdue(reportTitle):

    #asks if the user wants a copy of the report in CSV format too
    yn = input("\nDo you wish to generate a CSV file of the report as well? [y/n]:  ").lower()
    
    clearScreen()

    #pulls the view
    cursor.execute("SELECT * FROM supply_overdue;")
    orders = cursor.fetchall()

    #formatting string for dates
    dateFormat = "%B %d, %Y"

    #if yes, create csv
    if yn == "y":
        createCsv(f"{reportTitle}.csv", "VENDOR NAME, ORDER DATE, PROMISED DATE, ACTUAL DELIVERY DATE, DAYS OVERDUE")

    print(f"\t\t{reportTitle}")

    #loops through the overdue orders and prints them to the screen
    for order in orders:

        #some friendlier names for things at specific indexes
        vendorName = order[3]
        orderDate = order[0]
        promisedDate = order[1]
        actualDate = order[2]
        daysOverdue = order[2] - order[1]
        daysOverdue = daysOverdue.days

        #prints it formatted
        print()
        print(f"Vendor Name         : {vendorName}")
        print(f"Order Date          : {orderDate.strftime(dateFormat)}")
        print(f"Promised Date       : {promisedDate.strftime(dateFormat)}")
        print(f"Actual Delivery Date: {actualDate.strftime(dateFormat)}")
        print(f"Days Overdue        : {daysOverdue}")

        #if user wants to, writes to csv
        if yn == "y":
            line = [vendorName, orderDate, promisedDate, actualDate, daysOverdue]
            writeCsv(f"{reportTitle}.csv", line)

    print(f"\nReport generated on {datetime.now().strftime('%Y-%m-%d @ %H:%M')}")

    #success message
    if yn == "y":
        print(f"\nCSV file written to {reportTitle} in the same directory as this program.")

    #holds the command line open for viewing the report
    input("\nPress enter to exit to the main menu...")

#the star of the show, gets views, puts them in a pandas dataframe, prints it to the screen, then can output it as a csv or html file
def pdTable(args):

    #under a try block in case the user didn't pip install pandas
    try:
        import pandas

        for arg in args:

            #friendlier names again
            viewName = arg[0]
            friendlyName = arg[1]

            #executes SQL
            cursor.execute(f"SELECT * FROM {viewName}")

            #loads results of SQL query into a pandas dataframe for later viewing
            df = pandas.DataFrame(cursor.fetchall())
            
            #retrieves names of columns from MySQL and sets the dataframe's to match
            df.columns = getColumnNames(viewName)

            #formatting to make the dataframe look pretty
            pandas.set_option('display.width', 1000)
            pandas.set_option('display.colheader_justify', 'center')

            #prints out the title of the report and the report
            print(f"\n\t\t--- {friendlyName} ---\n")
            print(df.to_string(index=False))

            print(f"\nReport generated on {datetime.now().strftime('%Y-%m-%d @ %H:%M:%S')}")

            #asks if the user wants a copy of the report in CSV format too
            che = input("\nDo you wish to generate a CSV or HTML copy of this report?  Hit enter for none [c/h/enter]:  ").lower()
            if che == "c":
                df.to_csv(f"{friendlyName}.csv", index=False)
                print(f"\nCSV file written to {friendlyName}.csv in the same directory as this program.")
            elif che == "h":
                df.to_html(f"{friendlyName}.html", index=False)
                print(f"\nHTML file written to {friendlyName}.html in the same directory as this program.")

            #prints a divider for when there's multiple reports
            print()
            print("-" * 100)

    #if the user didn't install pandas
    except ImportError as err:
        print(err)
        print("\nYou need to run \"pip install pandas\" to view this report!")
    
    #for any other exceptions
    except Exception as err:
        print(err)
 
    #holds the command line open for viewing the report
    input("\nPress enter to exit to the main menu...")

#################### BEGIN MAIN METHOD ####################

#had to add this manually to make everything work together
cursor.execute("USE bacchus;")

#variable to control the main loop
masterControl = True

#keeps the program running until the user exits
while masterControl:

    #welcome message and menu
    clearScreen()
    print("\nWelcome to Bacchus Business Reports!")
    print("\nDeveloped by James Brown, Joshua Frazier, Christopher McCracken, and Taylor Reid")
    print("\nThe following options are available:")

    print("\n\t1 - Supplies")
    print("\n\t2 - Wine Sales")
    print("\n\t3 - Employee Hours")

    print("\n\t4 - EXIT\n")
    selection = input("Please enter the number of your selection [1/2/3/4]:  ")

    #picks method based on user input
    if selection == "1":
        clearScreen()
        print("\n1 - List (does not require pandas library)\n")
        print("\n2 - Pandas Table (requires pandas library)\n")
        tl = input("View it as a pandas table or a list [1/2]:  ").lower()
        clearScreen()
        if tl == "1":
            supplyOverdue("Late Supplies Orders")
        elif tl == "2":
            pdTable([["supply_all", "All Supply Shipments Report"],["supply_overdue", "Late Supply Orders Report"]])

    elif selection == "2":
        clearScreen()
        pdTable([["sales_all", "Wine Sales Report"]])
      
    elif selection == "3":
        clearScreen()
        pdTable([["employee_all", "Employee Hours Report"]])

    elif selection == "4":
        clearScreen()
        print("\nGoodbye and thank you for using Bacchus Business Reports!\n")
        masterControl = False
#################### END MAIN METHOD ####################

#closes connection and holds the command line open for viewing
db.close()