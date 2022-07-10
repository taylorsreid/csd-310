# Bacchus Group Project - Red Team

Make sure that you run the Python scripts from the command line and not VS Code, otherwise the JSON file may not load (from experience).

Before being able to run our Python scripts, you will need to run the following commands in MySQL since I am unable to create a database on your machine without knowing your MySQL root password:

    CREATE USER 'bacchus_user'@'localhost' IDENTIFIED BY 'winesnob';

    CREATE DATABASE bacchus;

    GRANT ALL PRIVILEGES ON bacchus.* TO 'bacchus_user'@'localhost';