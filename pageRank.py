import sqlite3 as sql


# Создает БД с высчитанным pagerank для всех найденных пауком страниц
def calculatepagerank(dbname, iterations=5):
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
    cursor.execute('CREATE INDEX IF NOT EXISTS wordidx       ON wordlist(word)')
    cursor.execute('CREATE INDEX IF NOT EXISTS urlidx        ON urllist(url)')
    cursor.execute('CREATE INDEX IF NOT EXISTS wordurlidx    ON wordlocation(fk_wordId)')
    cursor.execute('CREATE INDEX IF NOT EXISTS urltoidx      ON linkbetweenurl(fk_To_UrlId)')
    cursor.execute('CREATE INDEX IF NOT EXISTS urlfromidx    ON linkbetweenurl(fk_From_UrlId)')
    cursor.execute("DROP INDEX   IF EXISTS rankurlididx;")
    cursor.execute('CREATE INDEX IF NOT EXISTS rankurlididx  ON pagerank(urlid)')
    cursor.execute("REINDEX wordidx;")
    cursor.execute("REINDEX urlidx;")
    cursor.execute("REINDEX wordurlidx;")
    cursor.execute("REINDEX urltoidx;")
    cursor.execute("REINDEX urlfromidx;")
    cursor.execute("REINDEX rankurlididx;")

    # Изначально задаем каждому URL ранг = 1.0
    cursor.execute('INSERT INTO pagerank (urlid, score) SELECT rowid, 1.0 FROM urllist')
    connection.commit()

    for i in range(iterations):
        print(f"Составление pagerank database. Итерация {i+1}")
        for (urlid, ) in cursor.execute('SELECT urlId FROM urlList'):
            pr = 0.15
            for (linker,) in cursor.execute(
                    f'SELECT DISTINCT fk_From_UrlId FROM linkBetweenURL WHERE fk_To_UrlId={urlid}'):
                # Находим ранг ссылающейся страницы
                linkingpr = cursor.execute(
                    f'SELECT score FROM pagerank WHERE urlid={linker}').fetchone()[0]
                # Находим общее число ссылок на ссылающейся странице
                linkingcount = cursor.execute(
                    f'SELECT count(*) FROM linkBetweenURL WHERE fk_From_UrlId={linker}').fetchone()[0]
                pr += 0.85 * (linkingpr / linkingcount)
    cursor.execute(f'UPDATE pagerank SET score={pr} WHERE urlid={urlid}')
    connection.commit()


# Принимает значение pagerank из БД, нормализует и возвращает метрику
def pagerankscore(dbname, urlids):
    connection = sql.connect(dbname)
    cursor = connection.cursor()
    # Это надо переписать более понятным образом
    pageranks = dict([(combination[0], cursor.execute(
        f'SELECT score FROM pagerank WHERE urlid={combination[0]}').fetchone()[0]) for combination in urlids])
    maxrank = max(pageranks.values())   # Код нормализации переписать, когда разнесем эти функции
    normalizedscores = dict([(url, float(score) / maxrank) for (url, score) in pageranks.items()])
    print(f"\nМетрика pagerank: \n{normalizedscores}\n")
    return normalizedscores
