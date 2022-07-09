# Bacchus Group Project - Red Team

Before being able to run our Python scripts, you will need to run the following commands in MySQL since I am unable to create a database without privileges:

CREATE USER 'bacchus_user'@'localhost' IDENTIFIED BY 'winesnob';

CREATE DATABASE bacchus;

GRANT ALL PRIVILEGES ON bacchus.* TO 'bacchus_user'@'localhost';