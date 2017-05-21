  SELECT a.Title  AS title,
         av.ViewCount AS views
    FROM Articles a
         INNER JOIN article_views av ON av.slug = a.slug
ORDER BY av.ViewCount DESC
   LIMIT 3