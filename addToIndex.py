import re
import textOnly
import isIndexed
import sqlite3


def addIndex(self, soup, url):
    if isIndexed.isIndexed(self, url): return
    print('Индексируется ' + url)

    text = textOnly.getTextOnly(self, soup)  # Получить список слов
    words = separateWords(text)
    urlid = getEntryId(self, 'urlId', 'urlList', 'url', url)  # Получить идентификатор URL

    # Связать каждое слово с этим URL
    for i in range(len(words)):
        word = words[i]
        if word in self.ignorewords: continue
        wordid = getEntryId(self, 'wordId', 'wordList', 'word', word)
        self.conection.execute(
            "INSERT INTO wordlocation (fk_urlid,fk_wordid,location) values (%d,%d,%d)" % (urlid, wordid, i))
        self.conection.execute(
            "INSERT INTO linkWord (fk_wordId, fk_linkId) values (%d,%d)" % (wordid,urlid) )

    # проверить, была ли проиндексирован данных url   - isIndexed
    # если не был, то
    #   получить тестовое содержимое страницы - getTextOnly
    #   получить список отдельных слов        - separateWords
    #   Для каждого найденного слова currentword в списке wordList[]
    #     получить id_слова для currentword   -  getEntryId(‘Таблица wordlist в БД’, ‘столбец word’, ‘currentword ’)
    #     внести данные id_слова + id_url + положение_слова в таблицу wordLocation


def separateWords(text):
    text = re.sub(r"\',\(,\),\", [@|$|#|%|&]"," ", text)
    splitter = re.compile(str(text))
    return [ s.lower() for s in re.split(r'\W+',str(splitter)) if s!='']


def getEntryId(self, rowName, tableName, fieldName, value, createnew=True):
    try:
        cur = self.conection.execute("SELECT %s FROM %s WHERE %s='%s'" % (rowName, tableName, fieldName, value))
        res = cur.fetchone()
        if res == None:
            cur = self.conection.execute("INSERT INTO %s (%s) VALUES ('%s')" % (tableName, fieldName, value))
            return cur.lastrowid
        else:
            return res[0]
    except sqlite3.OperationalError:
        return 0