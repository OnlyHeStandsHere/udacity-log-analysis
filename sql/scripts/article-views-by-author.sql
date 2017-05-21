  SELECT a.name,
         SUM(av.viewcount) AS AuthorArticleViews
    FROM authors a
         INNER JOIN articles at ON at.author = a.id
         INNER JOIN article_views av ON av.slug = at.slug
GROUP BY a.name
ORDER BY AuthorArticleViews DESC


