/***********************************************************

     Author: Jesse Maitland
       Date: 2017-05-20
       Type: Create View
Description: Ranks authors by article views ordered by most popular on top
  Dependant: articles_view

***********************************************************/
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
         CAST(cte.name AS CHAR(30))                    AS name,
         'Views -- ' || cte.Article_Views              AS article_views
    FROM cte
ORDER BY cte.Article_Views DESC;

