# Лист с метриками
wordMetrics = []
urlMetrics = []


def metricsInsert(self):
    # Сбор количества слов и ссылок в БД
    countWord = self.cursor.execute('SELECT COUNT(wordId) FROM wordList;')
    wordMetrics.append(countWord.fetchone())

    countUrl = self.cursor.execute('SELECT COUNT(urlId) FROM urlList;')
    urlMetrics.append(countUrl.fetchone())
