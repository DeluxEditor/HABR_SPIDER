def createDB(self):
    sql_create_urlList = """
        CREATE TABLE IF NOT EXISTS urlList (
	        urlId INTEGER PRIMARY KEY AUTOINCREMENT, 
	        url TEXT
        );
    """

    sql_create_wordList = """
        CREATE TABLE IF NOT EXISTS wordList (
            wordId INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            isFiltred INTEGER	-- Следует ли проиндексированное слово фильтровать при выдаче пользователю (???)
        );
     """

    sql_create_wordLocation = """
        CREATE TABLE IF NOT EXISTS wordLocation (
            wordLocationId INTEGER PRIMARY KEY AUTOINCREMENT, 
            fk_wordId INTEGER,
            fk_urlId INTEGER,
            location INTEGER,
            FOREIGN KEY (fk_wordId) REFERENCES wordList (wordId),
            FOREIGN KEY (fk_urlId) REFERENCES urlList (urlId)
        );
    """

    sql_create_linkBeetwenURL = """
        CREATE TABLE IF NOT EXISTS linkBetweenURL (
            linkId INTEGER PRIMARY KEY AUTOINCREMENT, 
            fk_From_UrlId INTEGER,
            fk_To_UrlId INTEGER,
            FOREIGN KEY (fk_From_UrlId) REFERENCES urlList (urlId),
            FOREIGN KEY (fk_To_UrlId) REFERENCES urlList (urlId)
        );
    """

    sql_create_linkWord = """
        CREATE TABLE IF NOT EXISTS linkWord (
            linkWordId INTEGER PRIMARY KEY AUTOINCREMENT,
            fk_wordId INTEGER,
            fk_linkId INTEGER,
            FOREIGN KEY (fk_wordId)  REFERENCES wordList (wordId),
            FOREIGN KEY (fk_linkId)  REFERENCES linkBetweenURL (linkId)
        );
    """

    self.cursor.execute('DROP TABLE IF EXISTS urlList;')
    self.cursor.execute('DROP TABLE IF EXISTS wordList;')
    self.cursor.execute('DROP TABLE IF EXISTS wordLocation;')
    self.cursor.execute('DROP TABLE IF EXISTS linkBetweenURL;')
    self.cursor.execute('DROP TABLE IF EXISTS linkWord;')

    self.cursor.execute(sql_create_urlList)
    self.cursor.execute(sql_create_wordList)
    self.cursor.execute(sql_create_wordLocation)
    self.cursor.execute(sql_create_linkBeetwenURL)
    self.cursor.execute(sql_create_linkWord)