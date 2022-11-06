SELECT linkWord.fk_wordId, COUNT(*) AS word_count, wordList.word

FROM linkWord

LEFT JOIN wordList ON fk_wordId = wordId

GROUP BY fk_wordId

ORDER BY word_count DESC
LIMIT 20;



SELECT wordLocation.fk_urlId, COUNT(*) AS url_usage_count, urlList.url

FROM wordLocation

LEFT JOIN urlList ON fk_urlId= urlId

GROUP BY fk_urlId

ORDER BY url_usage_count DESC
LIMIT 20;