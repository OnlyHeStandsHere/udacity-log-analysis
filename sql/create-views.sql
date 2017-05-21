/***********************************************************

     Author: Jesse Maitland
       Date: 2017-05-20
       Type: Create View
Description: Creates all necessary views for
   Criteria: To be counted, the record must have method = get, and stats = 200 ok

***********************************************************/


CREATE VIEW article_views AS

  SELECT COUNT(id) AS ViewCount,
         SPLIT_PART(path, '/', 3) AS slug  -- removes the /article/ to allow for join to slug in article
    FROM Log
   WHERE method = 'GET'
         AND status = '200 OK'
GROUP BY path
  HAVING LENGTH(SPLIT_PART(path, '/', 3)) > 1; -- eliminates any groups that don't have a valid path


CREATE VIEW author_rank AS

WITH cte AS (
    SELECT
      a.name,
      SUM(av.viewcount) AS Article_Views
    FROM authors a
      INNER JOIN articles at ON at.author = a.id
      INNER JOIN article_views av ON av.slug = at.slug
    GROUP BY a.name
)

  SELECT RANK() OVER (ORDER BY CTE.Article_Views DESC) AS Author_Rank,
         cte.name,
         cte.Article_Views
    FROM cte
ORDER BY cte.Article_Views DESC;


CREATE VIEW article_top3 AS

  SELECT a.Title  AS title,
         av.ViewCount AS views
    FROM Articles a
         INNER JOIN article_views av ON av.slug = a.slug
ORDER BY av.ViewCount DESC
   LIMIT 3;

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
SELECT percent_of_errors,
       request_date
  FROM percetange
 WHERE percent_of_errors > 1.0;
