# import-csv-to-mysql
This project is to export data from contact_list.csv file 
and insert the data to related tables of customer database.

0.Requirements:
 mysql 5.7
 python 3.7
 py-mysql which can be installed by command on mac: 
 pip3 install py-mysql

1. Create database and tables using the following command:
CREATE DATABASE customer;
CREATE TABLE contact (
id INT(11) NOT NULL AUTO_INCREMENT, title ENUM('Mr', 'Mrs', 'Miss', 'Ms', 'Dr'), first_name VARCHAR(64),
last_name VARCHAR(64),
company_name VARCHAR(64), date_of_birth DATETIME,
notes VARCHAR(255),
PRIMARY KEY(id)
);
CREATE TABLE address (
id INT(11) NOT NULL AUTO_INCREMENT, contact_id INT(11) NOT NULL,
street1 VARCHAR(100),
street2 VARCHAR(100),
suburb VARCHAR(64),
city VARCHAR(64),
post_code VARCHAR(16),
PRIMARY KEY(id)
);
CREATE TABLE phone (
id INT(11) NOT NULL AUTO_INCREMENT, contact_id INT(11) NOT NULL,
name VARCHAR(64),
content VARCHAR(64),
type ENUM('Home', 'Work', 'Mobile', 'Other'), PRIMARY KEY(id)
);

2.set the CHARACTER of the database and table as there is emoji in the notes column.
SET NAMES utf8mb4;
ALTER DATABASE customer CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
ALTER TABLE contact  CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Using the following command to verify the configuration:
mysql> SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';
+--------------------------+--------------------+
| Variable_name            | Value              |
+--------------------------+--------------------+
| character_set_client     | utf8mb4            |
| character_set_connection | utf8mb4            |
| character_set_database   | utf8mb4            |
| character_set_filesystem | binary             |
| character_set_results    | utf8mb4            |
| character_set_server     | latin1             |
| character_set_system     | utf8               |
| collation_connection     | utf8mb4_general_ci |
| collation_database       | utf8mb4_general_ci |
| collation_server         | latin1_swedish_ci  |
+--------------------------+--------------------+
10 rows in set (0.00 sec)

3. run the script to import the data to database:
   python3 import_csv_data.py
