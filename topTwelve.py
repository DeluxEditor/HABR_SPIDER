import sqlite3 as sql
import os

cwd = os.getcwd()
DBname = cwd + '/LR1_2.db'
top_twelve = open("top-twelve.txt", "a")


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

    top_twelve.write('Top 20 words\n')

    for i in result:
        top_twelve.write(str(i)+'\n')

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

    top_twelve.write('Top 20 urls\n')

    for i in result:
        top_twelve.write(str(i)+'\n')


print(f'ТОП 20 слов запись\n')
topWord(DBname)
topUrl(DBname)
