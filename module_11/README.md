# Bacchus Group Project - Red Team

BEFORE BEGINNING DO THE FOLLOWING IF THIS IS YOUR FIRST TIME:

    IN MYSQL:

        CREATE USER IF NOT EXISTS 'bacchus_user'@'localhost' IDENTIFIED BY 'winesnob';

        GRANT ALL PRIVILEGES ON bacchus.* TO 'bacchus_user'@'localhost';

    IN YOUR OPERATING SYSTEMS COMMAND LINE:

        "python3 bacchus_install.py" from the command line to drop any outdated version of the database, recreate, and fill the database automatically.

        "pip install pandas" in the command line if you don't have pandas already.

        "python3 bacchus_reports.py" in the command line and view the reports :)