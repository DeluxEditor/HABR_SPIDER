DROP TABLE IF EXISTS urlList;
DROP TABLE IF EXISTS wordList;
DROP TABLE IF EXISTS wordLocation;
DROP TABLE IF EXISTS linkBetweenURL;
DROP TABLE IF EXISTS linkWord;


-- Проиндексированные URL
CREATE TABLE IF NOT EXISTS urlList (
	urlId INTEGER PRIMARY KEY AUTOINCREMENT, 
	url TEXT
);

-- Все проиндексированные слова на страницах
CREATE TABLE IF NOT EXISTS wordList (
    wordId INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    isFiltred INTEGER	-- Следует ли проиндексированное слово фильтровать при выдаче пользователю (???)
);

-- Места вхождения слов в документы (???)
CREATE TABLE IF NOT EXISTS wordLocation (
    wordLocationId INTEGER PRIMARY KEY AUTOINCREMENT, 
    fk_wordId INTEGER,
    fk_urlId INTEGER,
    location INTEGER,
	FOREIGN KEY (fk_wordId) REFERENCES wordList (wordId),
	FOREIGN KEY (fk_urlId) REFERENCES urlList (urlId)
);

-- id двух URL, связанных между собой ссылкой
CREATE TABLE IF NOT EXISTS linkBetweenURL (
    linkId INTEGER PRIMARY KEY AUTOINCREMENT, 
    fk_From_UrlId INTEGER,
    fk_To_UrlId INTEGER,
	FOREIGN KEY (fk_From_UrlId) REFERENCES urlList (urlId),
	FOREIGN KEY (fk_To_UrlId) REFERENCES urlList (urlId)
);

-- Слова, составляющие ссылку
CREATE TABLE IF NOT EXISTS linkWord (
    linkWordId INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_wordId INTEGER,
    fk_linkId INTEGER,
	FOREIGN KEY (fk_wordId)  REFERENCES wordList (wordId),
	FOREIGN KEY (fk_linkId)  REFERENCES linkBetweenURL (linkId)
);