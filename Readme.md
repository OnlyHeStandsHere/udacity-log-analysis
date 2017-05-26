# Udacity FSND Log Analysis

### Project generates some simple text format reports from and SQL database

#### To get started:

##### This project uses python 3

Views must first be created in the news database by either running the script

`/sql/create-views.sql`

with the following command 

`psql -d news -f create-views.sql`


or by manually executing the create view scripts located in 

`/sql/views`

if the manual approach is taken, `article-views.sql` must be created first as it is a dependancy
for other views. 

sample and generated reports will be saved in

`/reports`

##### Database Connection
To connect to your appropriate database in /app/main.py edit the data base connection string

`connection = psycopg2.connect("dbname=news user=user password=password")`

with your appropriate database credentials

to run this project clone the directory and run

`/app/main.py`

`python3 main.py`

You will then be prompted in the terminal to generate your desired reports. 

## CREATE VIEW SCRIPTS
This project relies on database views These views are available in /sql/views as well as below
``` sql
 CREATE VIEW article_views AS
   SELECT COUNT(id) AS ViewCount,
          SPLIT_PART(path, '/', 3) AS slug  
     FROM Log
    WHERE method = 'GET'
          AND status = '200 OK'
 GROUP BY path
   HAVING LENGTH(SPLIT_PART(path, '/', 3)) > 1
```
