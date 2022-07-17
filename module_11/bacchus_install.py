'''
Red Team
    James Brown
    Joshua Frazier
    Christopher McCracken
    Taylor Reid
7/11/2022
Module 11.1
'''

#imports connection protocols and JSON utilities
import errno
from connect import db, cursor
import json
import time

import mysql.connector
from mysql.connector import errorcode

#used for showing execution time
startTime = time.time()

#some shorthand aliases for success/error messages for later
ts = " table create.... SUCCESS"
ds = " data insert..... SUCCESS"
vs = " view create..... SUCCESS"
tf = " table create.... FAIL | Reason: "
df = " data insert..... FAIL | Reason: "
vf = " view create..... FAIL | Reason: "

################################# OPENING JSON FILE WITH VALUES TO FILL DATABASE ###########################################

try:
    with open("bacchus.json") as bacchus_json:
        bacchus = json.load(bacchus_json)
except Exception as err:
    print(err)

################################# DROP AND RECREATE DATABASE ###########################################

print("Recreating database:")

#self explanatory
try:
    cursor.execute("DROP DATABASE IF EXISTS bacchus;")
    print("\tDropping existing bacchus database if it exists... SUCCESS")
except mysql.connector.Error:
    print("\tDropping existing bacchus database if it exists... DOESN'T EXIST")

try:
    cursor.execute("CREATE DATABASE bacchus;")
    print("\tRecreating bacchus database... SUCCESS")
except Exception as err:
    print(f"\tCREATE DATABASE bacchus;... FAIL | Reason: {err}")

try:
    cursor.execute("USE bacchus;")
except Exception as err:
    print(f"USE bacchus;... FAIL | Reason: {err}")

################################# RECREATING TABLES ###########################################

print("\nRecreating tables:")

#creates a table with a list of vendors
try:
    cursor.execute("CREATE OR REPLACE TABLE vendor(vendor_id INT NOT NULL, vendor_name VARCHAR(75) NOT NULL, PRIMARY KEY(vendor_id));")
    print(f"\tvendor{ts}")
except Exception as err:
    print(f"\tvendor{tf}{err}")

#creates the employee table
try:
    cursor.execute("""CREATE OR REPLACE TABLE employee
                        (employee_id INT NOT NULL, 
                        employee_first_name VARCHAR(75) NOT NULL, 
                        employee_last_name VARCHAR(75) NOT NULL, 
                        employee_role VARCHAR(75) NOT NULL, 
                        q1_hours INT NOT NULL, 
                        q2_hours INT NOT NULL, 
                        q3_hours INT NOT NULL, 
                        q4_hours INT NOT NULL, 
                        PRIMARY KEY(employee_id));""")
    print(f"\temployee{ts}")
except Exception as err:
    print(f"\temployee{tf}{err}")

#creates a table with distributors
try:
    cursor.execute("CREATE OR REPLACE TABLE distributor(distributor_id INT NOT NULL, distributor_name VARCHAR(75) NOT NULL, PRIMARY KEY(distributor_id));")
    print(f"\tdistributor{ts}")
except Exception as err:
    print(f"\tdistributor{tf}{err}")

#creates a table to hold the LAST MONTH'S sales
try:
    cursor.execute("""CREATE OR REPLACE TABLE sales
                        (distributor_id INT NOT NULL, 
                        merlot INT NOT NULL, 
                        cabernet INT NOT NULL, 
                        chablis INT NOT NULL, 
                        chardonnay INT NOT NULL, 
                        CONSTRAINT fk_distributor_id 
                        FOREIGN KEY(distributor_id) 
                        REFERENCES distributor(distributor_id), 
                        PRIMARY KEY(distributor_id));""")
    print(f"\tsales{ts}")
except Exception as err:
    print(f"\tsales{tf}{err}")


#creates a table with a list of supplies
try:
    cursor.execute("""CREATE OR REPLACE TABLE supply
                        (supply_id INT NOT NULL, 
                        supply_name VARCHAR(75) NOT NULL, 
                        supply_price DOUBLE, 
                        vendor_id INT NOT NULL, 
                        PRIMARY KEY(supply_id), 
                        CONSTRAINT fk_supply_vendor_id 
                        FOREIGN KEY(vendor_id) 
                        REFERENCES vendor(vendor_id));""")
    print(f"\tsupply{ts}")
except Exception as err:
    print(f"\tsupply{tf}{err}")

#creates a table for supply orders
try:
    cursor.execute("""CREATE OR REPLACE TABLE supply_order
                        (order_date DATE NOT NULL, 
                        promised_date DATE NOT NULL, 
                        actual_date DATE, 
                        order_price DOUBLE NOT NULL, 
                        vendor_id INT NOT NULL, 
                        PRIMARY KEY(order_date), 
                        CONSTRAINT fk_order_vendor_id 
                        FOREIGN KEY(vendor_id) 
                        REFERENCES vendor(vendor_id));""")
    print(f"\tsupply_orders{ts}")
except Exception as err:
    print(f"\tsupply_orders{tf}{err}")

#time to start filling the tables
print("\nFilling SQL tables with values from bacchus.json:")

#fills the vendor table from the JSON file
try:
    i = 0
    while i < len(bacchus["vendor"]):
        vendor_id = bacchus["vendor"][i]["vendor_id"]
        vendor_name = bacchus["vendor"][i]["vendor_name"]
        cursor.execute(f"INSERT INTO vendor(vendor_id, vendor_name) VALUES('{vendor_id}', '{vendor_name}');")
        i += 1
    print(f"\tvendor{ds}")
except Exception as err:
    print(f"\tvendor{df}{err}")

#fills the employee table from the JSON file
try:
    i = 0
    while i < len(bacchus["employee"]):
        employee_id = bacchus["employee"][i]["employee_id"]
        employee_first_name = bacchus["employee"][i]["employee_first_name"]
        employee_last_name = bacchus["employee"][i]["employee_last_name"]
        employee_role = bacchus["employee"][i]["employee_role"]

        q1_hours = bacchus["employee"][i]["q1_hours"]
        q2_hours = bacchus["employee"][i]["q2_hours"]
        q3_hours = bacchus["employee"][i]["q3_hours"]
        q4_hours = bacchus["employee"][i]["q4_hours"]

        cursor.execute(f"INSERT INTO employee(employee_id, employee_first_name, employee_last_name, employee_role, q1_hours, q2_hours, q3_hours, q4_hours) VALUES('{employee_id}', '{employee_first_name}', '{employee_last_name}', '{employee_role}', '{q1_hours}', '{q2_hours}', '{q3_hours}', '{q4_hours}');")
        i += 1
    print(f"\temployee{ds}")
except Exception as err:
    print(f"\temployee{df}{err}")

#fills the distributor table from the JSON file
try:
    i = 0
    while i < len(bacchus["distributor"]):
        distributor_id = bacchus["distributor"][i]["distributor_id"]
        distributor_name = bacchus["distributor"][i]["distributor_name"]
        cursor.execute(f"INSERT INTO distributor(distributor_id, distributor_name) VALUES('{distributor_id}', '{distributor_name}');")
        i += 1
    print(f"\tdistributor{ds}")
except Exception as err:
    print(f"\tdistributor{df}{err}")

#fills the sales table from the JSON file
try:
    i = 0
    while i < len(bacchus["sales"]):
        distributor_id = bacchus["sales"][i]["distributor_id"]
        merlot = bacchus["sales"][i]["merlot"]
        cabernet = bacchus["sales"][i]["cabernet"]
        chablis = bacchus["sales"][i]["chablis"]
        chardonnay = bacchus["sales"][i]["chardonnay"]
        cursor.execute(f"INSERT INTO sales(distributor_id, merlot, cabernet, chablis, chardonnay) VALUES('{distributor_id}', '{merlot}', '{cabernet}', '{chablis}', '{chardonnay}');")
        i += 1
    print(f"\tsales{ds}")
except Exception as err:
    print(f"\tsales{df}{err}")

#fills the supply table from the JSON file
try:
    i = 0
    while i < len(bacchus["supply"]):
        supply_id = bacchus["supply"][i]["supply_id"]
        supply_name = bacchus["supply"][i]["supply_name"]
        supply_price = bacchus["supply"][i]["supply_price"]
        vendor_id = bacchus["supply"][i]["vendor_id"]
        cursor.execute(f"INSERT INTO supply(supply_id, supply_name, supply_price, vendor_id) VALUES('{supply_id}', '{supply_name}', '{supply_price}', '{vendor_id}');")
        i += 1
    print(f"\tsupply{ds}")
except Exception as err:
    print(f"\tsupply{df}{err}")

#fills the supply order table from the JSON file
try:
    i = 0
    while i < len(bacchus["supply_order"]):
        order_date = bacchus["supply_order"][i]["order_date"]
        order_date = bacchus["supply_order"][i]["order_date"]
        promised_date = bacchus["supply_order"][i]["promised_date"]
        actual_date = bacchus["supply_order"][i]["actual_date"]
        order_price = bacchus["supply_order"][i]["order_price"]
        vendor_id = bacchus["supply_order"][i]["vendor_id"]
        cursor.execute(f"INSERT INTO supply_order(order_date, promised_date, actual_date, order_price, vendor_id) VALUES('{order_date}', '{promised_date}', '{actual_date}', '{order_price}', '{vendor_id}');")
        i += 1
    print(f"\tsupply_order{ds}")
except Exception as err:
    print(f"\tsupply_order{df}{err}")

################################# CREATING VIEWS ###########################################

print("\nCreating views:")

#creates a view of overdue supply shipments that is easier to work with later on
try:
    cursor.execute(f"""
                    CREATE OR REPLACE VIEW supply_overdue AS 
                    SELECT order_date, promised_date, actual_date, vendor_name 
                    FROM supply_order 
                    INNER JOIN vendor ON supply_order.vendor_id = vendor.vendor_id
                    WHERE actual_date > promised_date;
                    """)
    print(f"\tsupply_overdue{vs}")
except Exception as err:
    print(f"\tsupply_overdue{vf}{err}")

#creates a view of the totals of wine sold by distributor
try:
    cursor.execute(f"""CREATE OR REPLACE VIEW sales_by_distributor AS 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay) AS total, ROUND(SUM(merlot + cabernet + chablis + chardonnay) / 4, 2) AS average
                            FROM sales
                            WHERE sales.distributor_id =1
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay) AS total, ROUND(SUM(merlot + cabernet + chablis + chardonnay) / 4, 2) AS average
                            FROM sales
                            WHERE sales.distributor_id =2
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay) AS total, ROUND(SUM(merlot + cabernet + chablis + chardonnay) / 4, 2) AS average
                            FROM sales
                            WHERE sales.distributor_id =3
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay) AS total, ROUND(SUM(merlot + cabernet + chablis + chardonnay) / 4, 2) AS average
                            FROM sales
                            WHERE sales.distributor_id =4
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay) AS total, ROUND(SUM(merlot + cabernet + chablis + chardonnay) / 4, 2) AS average
                            FROM sales
                            WHERE sales.distributor_id =5
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay) AS total, ROUND(SUM(merlot + cabernet + chablis + chardonnay) / 4, 2) AS average
                            FROM sales
                            WHERE sales.distributor_id =6
                    """)
    print(f"\tsales_by_distributor{vs}")
except Exception as err:
    print(f"\tsales_by_distributor{vf}{err}")

#creates a view of all sales statistics
try:
    cursor.execute(f"""
                    CREATE OR REPLACE VIEW sales_all AS
                    SELECT distributor_name, merlot, cabernet, chablis, chardonnay, total, average
                    FROM sales
                    INNER JOIN distributor ON sales.distributor_id = distributor.distributor_id
                    INNER JOIN sales_by_distributor ON sales.distributor_id = sales_by_distributor.distributor_id    
                    UNION
                        SELECT 'total' AS distributor_name, SUM(merlot), SUM(cabernet), SUM(chablis), SUM(chardonnay), SUM(total) AS total, average
                        FROM sales
                        INNER JOIN sales_by_distributor on sales.distributor_id = sales_by_distributor.distributor_id
                    UNION
                        SELECT 'average' AS distributor_name, ROUND(AVG(merlot), 2), ROUND(AVG(cabernet), 2), ROUND(AVG(chablis), 2), ROUND(AVG(chardonnay), 2), ROUND(AVG(total), 2) AS average, ''
                        FROM sales
                        INNER JOIN sales_by_distributor on sales.distributor_id = sales_by_distributor.distributor_id
                    ;
                    """)
    print(f"\tsales_all{vs}")
except Exception as err:
    print(f"\tsales_all{vf}{err}")

#creates a view of each employees yearly total and quarterly average hours
try:
    cursor.execute(f"""CREATE OR REPLACE VIEW employee_hours_total_average AS 
                            SELECT
                                employee_id,
                                SUM(q1_hours + q2_hours + q3_hours + q4_hours) AS total,
                                ROUND(SUM(q1_hours + q2_hours + q3_hours + q4_hours) / 4, 2) AS average
                            FROM employee
                            WHERE employee_id =1
                        UNION ALL 
                            SELECT
                                employee_id,
                                SUM(q1_hours + q2_hours + q3_hours + q4_hours) AS total,
                                ROUND(SUM(q1_hours + q2_hours + q3_hours + q4_hours) / 4, 2) AS average
                                FROM employee
                            WHERE employee_id =2
                        UNION ALL 
                            SELECT
                                employee_id,
                                SUM(q1_hours + q2_hours + q3_hours + q4_hours) AS total,
                                ROUND(SUM(q1_hours + q2_hours + q3_hours + q4_hours) / 4, 2) AS average
                                FROM employee
                            WHERE employee_id =3
                        UNION ALL 
                            SELECT
                                employee_id,
                                SUM(q1_hours + q2_hours + q3_hours + q4_hours) AS total,
                                ROUND(SUM(q1_hours + q2_hours + q3_hours + q4_hours) / 4, 2) AS average
                            FROM employee
                            WHERE employee_id =4
                        UNION ALL 
                            SELECT
                                employee_id,
                                SUM(q1_hours + q2_hours + q3_hours + q4_hours) AS total,
                                ROUND(SUM(q1_hours + q2_hours + q3_hours + q4_hours) / 4, 2) AS average
                            FROM employee
                            WHERE employee_id =5
                        UNION ALL 
                            SELECT
                                employee_id,
                                SUM(q1_hours + q2_hours + q3_hours + q4_hours) AS total,
                                ROUND(SUM(q1_hours + q2_hours + q3_hours + q4_hours) / 4, 2) AS average
                            FROM employee
                            WHERE employee_id =6;
                    """)
    print(f"\temployee_hours_total_average{vs}")
except Exception as err:
    print(f"\temployee_hours_total_average{vf}{err}")

#creates a view of a bunch of employee statistics
try:
    cursor.execute(f"""
                CREATE OR REPLACE VIEW employee_all AS
                SELECT employee_last_name, employee_first_name, employee_role, q1_hours, q2_hours, q3_hours, q4_hours, total, average
                FROM employee a
                INNER JOIN employee_hours_total_average b ON a.employee_id = b.employee_id
                UNION
                    SELECT 'total', null, null, SUM(q1_hours), SUM(q2_hours), SUM(q3_hours), SUM(q4_hours), SUM(total), SUM(average)
                    FROM employee_hours_total_average a
                    INNER JOIN employee b ON a.employee_id = b.employee_id
                UNION
                    SELECT 'average', null, null, ROUND(AVG(q1_hours), 2), ROUND(AVG(q2_hours), 2), ROUND(AVG(q3_hours), 2), ROUND(AVG(q4_hours), 2), ROUND(AVG(total), 2), ROUND(AVG(average), 2)
                    FROM employee_hours_total_average a
                    INNER JOIN employee b ON a.employee_id = b.employee_id
                ;
                """)
    print(f"\temployee_all{vs}")        
except Exception as err:
    print(f"\temployee_all{vf}{err}")

#creates a view of a bunch of supply statistics
try:
    cursor.execute(f"""
                CREATE OR REPLACE VIEW supply_all AS 
                   SELECT vendor_name, order_date, promised_date, actual_date, order_price
                   FROM supply_order
                   INNER JOIN vendor ON supply_order.vendor_id = vendor.vendor_id
                UNION
                    SELECT 'total', null, null, NULL, SUM(order_price)
                    FROM supply_order
                UNION
                    SELECT 'average', null, null, null, ROUND(AVG(order_price), 2)
                    FROM supply_order
                ;
                """)
    print(f"\tsupply_all{vs}")
except Exception as err:
    print(f"\tsupply_all{vf}{err}")

############################################################################################

#commits and closes connections
db.commit()
print(f"\nBacchus Install completed in {round((time.time() - startTime), 2)} seconds.\n")