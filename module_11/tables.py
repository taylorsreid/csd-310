'''
Red Team
    James Brown
    Joshua Frazier
    Christopher McCracken
    Taylor Reid
7/11/2022
Module 11.1
'''

from connect import db, cursor

def update():

     #creates a view of overdue supply shipments that is easier to work with later on
    cursor.execute(f"""
                    CREATE OR REPLACE VIEW supply_overdue AS 
                    SELECT order_date, promised_delivery_date, actual_delivery_date, vendor_name 
                    FROM supply_order 
                    INNER JOIN vendor ON supply_order.vendor_id = vendor.vendor_id
                    WHERE actual_delivery_date > promised_delivery_date;
                    """)

############################################################################################

    #fixing a prior mistake and changing some data types around
    cursor.execute(f"""
                    ALTER TABLE sales 
                    CHANGE merlot merlot INT(75) NOT NULL, 
                    CHANGE cabernet cabernet INT(75) NOT NULL, 
                    CHANGE chablis chablis INT(75) NOT NULL, 
                    CHANGE chardonnay chardonnay INT(75) NOT NULL;
                    """)

    #
    try:
        cursor.execute(f"""
                        ALTER TABLE sales
                        ADD total int NOT NULL;
                        """)
    except:
        pass

    #
    cursor.execute(f"""
                    UPDATE sales
                    SET total = merlot + cabernet + chablis + chardonnay;
                    """)

    #after the update, create a new view
    cursor.execute(f"""
                    CREATE OR REPLACE VIEW sales_all AS 
                    SELECT distributor_name, merlot, cabernet, chablis, chardonnay, total
                    FROM sales
                    INNER JOIN distributor ON sales.distributor_id = distributor.distributor_id
                    """)

############################################################################################

    #
    try:
        cursor.execute(f"""
                        ALTER TABLE employee
                        ADD total int NOT NULL;
                        """)
    except:
        pass
    cursor.execute(f"""
                    UPDATE employee
                    SET total = q1_hours + q2_hours + q3_hours + q4_hours;
                    """)

    db.commit()

update()