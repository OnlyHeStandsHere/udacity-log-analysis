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

the `article_views` VIEW must be created first
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
All other views can then be created

Author Rank
``` sql
CREATE VIEW author_rank AS

WITH cte AS (
    SELECT a.name,
           SUM(av.viewcount) AS Article_Views
      FROM authors a
           INNER JOIN articles at ON at.author = a.id
           INNER JOIN article_views av ON av.slug = at.slug
  GROUP BY a.name
)

  SELECT RANK() OVER (ORDER BY CTE.Article_Views DESC) AS Author_Rank,
         CAST(cte.name AS CHAR(30))                    AS name,
         'Views -- ' || cte.Article_Views              AS article_views
    FROM cte
ORDER BY cte.Article_Views DESC;
```

Top 3
``` sql
CREATE VIEW article_top3 AS

  SELECT CAST(a.Title AS CHAR(40))  AS title,
         'Views -- '|| av.ViewCount AS views
    FROM Articles a
         INNER JOIN article_views av ON av.slug = a.slug
ORDER BY av.ViewCount DESC
   LIMIT 3

```

percentage of errors
``` sql
CREATE VIEW high_error_dates AS

-- get all the requests for each day
WITH requests AS
  (
      SELECT COUNT(id)          AS request_count,
             CAST(time AS DATE) AS request_date
        FROM log
    GROUP BY request_date
  ),

-- get all the errors for each day
errors AS
  (
      SELECT COUNT(id)          AS error_count,
             CAST(time AS DATE) AS error_date
        FROM log
       WHERE status LIKE '4%'
    GROUP BY error_date
  ),

-- calculate the error percentage using the defined formula
percetange AS
  (
    SELECT CAST( CAST(e.error_count AS FLOAT) /
                 CAST(r.request_count AS FLOAT) * 100 AS DECIMAL(6, 2))  -- float / decimal will preserve decimal places
     AS percent_of_errors,
     r.request_date
FROM requests r
     INNER JOIN errors e ON e.error_date = r.request_date
  )

-- return the table to the caller
SELECT CAST(percent_of_errors || '%'  AS CHAR(10)) AS percentage_of_errors,
       'Date -- '|| request_date                 AS request_date
  FROM percetange
 WHERE percent_of_errors > 1.0;
```