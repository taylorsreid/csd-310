# bacchus

Before being able to run our Python scripts, you will need to run the following commands in MySQL:

CREATE USER 'bacchus_user'@'localhost' IDENTIFIED BY 'winesnob';

CREATE DATABASE bacchus;

GRANT ALL PRIVILEGES ON bacchus.* TO 'bacchus_user'@'localhost';