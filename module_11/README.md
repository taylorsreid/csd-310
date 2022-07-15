# Bacchus Group Project - Red Team

BEFORE BEGINNING:
    
    ---Always run all python scripts from the command line, not your IDE.  Running in VS Code has given odd results.
    
IN ADDITION:
    
    ---We decided to redo some of the database to make it run more smoothly.

    ---For best results and predictable behavior, we recommend recreating the database.

    ---bacchus_reports.py relies on the pandas library to show most of the reports.
       If you do not have pandas, the only report you will be able to view is the Overdue Supplies report.
       And only if you select "list" when prompted.
    
    Therefore, follow these steps:
        ---Run "CREATE OR REPLACE DATABASE bacchus;" as root in MySQL.
        ---Run "python3 bacchus_updates.py" refill the database properly.
        ---Run "pip install pandas" in the command line.
        ---Finally, run "python3 bacchus_reports.py" in the command line and view the reports :)