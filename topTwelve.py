import sqlite3 as sql

def topWord(dbName):
    connection = sql.connect(dbName)
    cursor = connection.cursor()
    cursor.execute(
    '''
    SELECT linkWord.fk_wordId, COUNT(*) AS word_count, wordList.word
    FROM linkWord
    LEFT JOIN wordList ON fk_wordId = wordId
    GROUP BY fk_wordId
    ORDER BY word_count DESC
    LIMIT 20;
    '''
    )
    result = cursor.fetchall()

    for i in result:
        print(i)

def topUrl(dbName):
    connection = sql.connect(dbName)
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT wordLocation.fk_urlId, COUNT(*) AS url_usage_count, urlList.url
        FROM wordLocation
        LEFT JOIN urlList ON fk_urlId= urlId
        GROUP BY fk_urlId
        ORDER BY url_usage_count DESC
        LIMIT 20;
        '''
    )
    result = cursor.fetchall()

    for i in result:
        print(i)