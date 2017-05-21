/***********************************************************

     Author: Jesse Maitland
       Date: 2017-05-20
       Type: Create View
Description: Returns the number of article views
   Criteria: To be counted, the record must have method = get, and stats = 200 ok

***********************************************************/

CREATE VIEW article_views AS

  SELECT COUNT(id) AS ViewCount,
         SPLIT_PART(path, '/', 3) AS slug  -- removes the /article/ to allow for join to slug in article
    FROM Log
   WHERE method = 'GET'
         AND status = '200 OK'
GROUP BY path
  HAVING LENGTH(SPLIT_PART(path, '/', 3)) > 1 -- eliminates any groups that don't have a valid path


