import sqlite3 as sql


# Создает БД с высчитанным pagerank для всех найденных пауком страниц
def calculatepagerank(dbname, iterations=5):
    global pr, urlid
    connection = sql.connect(dbname)
    cursor = connection.cursor()
    # стираем текущее содержимое таблицы PageRank
    cursor.execute('DROP TABLE IF EXISTS pagerank')
    cursor.execute("""CREATE TABLE  IF NOT EXISTS  pagerank (
                            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                            urlid INTEGER,
                            score REAL
                            );""")

    # Для некоторых столбцов в таблицах БД укажем команду создания объекта "INDEX" для ускорения поиска в БД
    cursor.execute("DROP INDEX   IF EXISTS wordidx;")
    cursor.execute("DROP INDEX   IF EXISTS urlidx;")
    cursor.execute("DROP INDEX   IF EXISTS wordurlidx;")
    cursor.execute("DROP INDEX   IF EXISTS urltoidx;")
    cursor.execute("DROP INDEX   IF EXISTS urlfromidx;")
    cursor.execute('CREATE INDEX IF NOT EXISTS wordidx       ON wordList(word)')
    cursor.execute('CREATE INDEX IF NOT EXISTS urlidx        ON urlList(url)')
    cursor.execute('CREATE INDEX IF NOT EXISTS wordurlidx    ON wordLocation(fk_wordId)')
    cursor.execute('CREATE INDEX IF NOT EXISTS urltoidx      ON linkBetweenURL(fk_To_UrlId)')
    cursor.execute('CREATE INDEX IF NOT EXISTS urlfromidx    ON linkBetweenURL(fk_From_UrlId)')
    cursor.execute("DROP INDEX   IF EXISTS rankurlididx;")
    cursor.execute('CREATE INDEX IF NOT EXISTS rankurlididx  ON pagerank(urlid)')
    cursor.execute("REINDEX wordidx;")
    cursor.execute("REINDEX urlidx;")
    cursor.execute("REINDEX wordurlidx;")
    cursor.execute("REINDEX urltoidx;")
    cursor.execute("REINDEX urlfromidx;")
    cursor.execute("REINDEX rankurlididx;")

    # Изначально задаем каждому URL ранг = 1.0
    cursor.execute('INSERT INTO pagerank (urlid, score) SELECT rowid, 1.0 FROM urlList')
    connection.commit()

    for i in range(iterations):
        print(f"Составление pagerank database. Итерация '{i+1}'")
        for (urlid, ) in connection.execute("SELECT urlId FROM urlList"):
            pr = 0.15
            links = cursor.execute(f"SELECT DISTINCT fk_From_urlId FROM linkBetweenURL WHERE fk_To_urlId='{urlid}'").fetchall()
            if links is not None:
                for (linker,) in links:
                    # Находим ранг ссылающейся страницы
                    linkingpr = connection.execute(f"SELECT score FROM pagerank WHERE urlid='{linker}'").fetchone()[0]
                    # Находим общее число ссылок на ссылающейся странице
                    linkingcount = connection.execute(f"SELECT count (*) FROM linkBetweenURL WHERE fk_From_UrlId='{linker}'").fetchone()[0]
                    pr += 0.85 * (linkingpr / linkingcount)
                    cursor.execute(f"UPDATE pagerank SET score='{pr}' WHERE urlid='{urlid}'")
                    connection.commit()
            else:
                continue


# Принимает значение pagerank из БД, нормализует и возвращает метрику
def pagerankscore(dbname, urlids):
    connection = sql.connect(dbname)
    cursor = connection.cursor()

    pageranks = dict()
    for urlid in urlids:
        pageranks[urlid[0]] = connection.execute(f"select score from pagerank where urlid= '{urlid[0]}'").fetchone()[0]

    maxrank = max(pageranks.values())   # Код нормализации переписать, когда разнесем эти функции

    # До исправлений return был в цикле и завершался после одного прохода
    # Соответственно имели только одну ссылку в pageRank вместо всех что послали методу на обработку
    # + было исправлено переопределение переменной-словаря каждый раз в цикле
    normalizedscores = dict()
    for (urlid, score) in pageranks.items():
        normalizedscores[urlid] = round(float(score) / maxrank, 4)
    print(f"\nМетрика pagerank: \n{normalizedscores}\n")
    return normalizedscores
