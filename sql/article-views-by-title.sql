/***********************************************************

     Author: Jesse Maitland
       Date: 2017-05-20
       Type: Ad-hoc
Description: Returns the top 3 articles by view by title

***********************************************************/

  SELECT a.Title  AS title,
         av.ViewCount AS views
    FROM Articles a
         INNER JOIN article_views av ON av.slug = a.slug
ORDER BY av.ViewCount DESC
   LIMIT 3