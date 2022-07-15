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
from connect import db, cursor
import json

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
                        promised_delivery_date DATE NOT NULL, 
                        actual_delivery_date DATE, 
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
        promised_delivery_date = bacchus["supply_order"][i]["promised_delivery_date"]
        actual_delivery_date = bacchus["supply_order"][i]["actual_delivery_date"]
        order_price = bacchus["supply_order"][i]["order_price"]
        vendor_id = bacchus["supply_order"][i]["vendor_id"]
        cursor.execute(f"INSERT INTO supply_order(order_date, promised_delivery_date, actual_delivery_date, order_price, vendor_id) VALUES('{order_date}', '{promised_delivery_date}', '{actual_delivery_date}', '{order_price}', '{vendor_id}');")
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
                    SELECT order_date, promised_delivery_date, actual_delivery_date, vendor_name 
                    FROM supply_order 
                    INNER JOIN vendor ON supply_order.vendor_id = vendor.vendor_id
                    WHERE actual_delivery_date > promised_delivery_date;
                    """)
    print(f"\tsupply_overdue{vs}")
except Exception as err:
    print(f"\tsupply_overdue{vf}{err}")

#creates a view of the totals of wine sold by distributor that dynamically updates
#kind proud of this one :)
try:
    cursor.execute(f"""CREATE OR REPLACE VIEW sales_totals_by_distributor AS 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay) AS distributor_total
                            FROM sales
                            WHERE sales.distributor_id =1
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay)  AS distributor_total
                            FROM sales
                            WHERE sales.distributor_id =2
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay)  AS distributor_total
                            FROM sales
                            WHERE sales.distributor_id =3
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay)  AS distributor_total
                            FROM sales
                            WHERE sales.distributor_id =4
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay)  AS distributor_total
                            FROM sales
                            WHERE sales.distributor_id =5
                        UNION ALL 
                            SELECT sales.distributor_id, SUM(merlot + cabernet + chablis + chardonnay)  AS distributor_total
                            FROM sales
                            WHERE sales.distributor_id =6
                    """)
    print(f"\tsales_totals_by_distributor{vs}")
except Exception as err:
    print(f"\tsales_totals_by_distributor{vf}{err}")

#
try:
    cursor.execute(f"""
                    CREATE OR REPLACE VIEW sales_totals_by_wine AS 
                    SELECT SUM(merlot) AS merlot, SUM(cabernet) AS cabernet, SUM(chablis) AS chablis, SUM(chardonnay) AS chardonnay FROM sales;
                    """)
    print(f"\tsales_totals_by_wine{vs}")
except Exception as err:
    print(f"\tsales_totals_by_wine{vf}{err}")

#
try:
    cursor.execute(f"""
                CREATE OR REPLACE VIEW sales_all AS
                SELECT distributor_name, merlot, cabernet, chablis, chardonnay, distributor_total
                FROM sales
                INNER JOIN distributor ON sales.distributor_id = distributor.distributor_id
                INNER JOIN sales_totals_by_distributor on sales.distributor_id = sales_totals_by_distributor.distributor_id
                ORDER BY sales.distributor_id ASC;
                """)
    print(f"\tsales_all{vs}")
except Exception as err:
    print(f"\tsales_all{vf}{err}")

############################################################################################

#commits and closes connections
db.commit()
print("\nDone")