def create_Marked_File(file_name, url_id, search_query):

    # Приобразование текста к нижнему регистру
    testText = testText.lower()

    for i in range(0, len(testQueryList)):
        testQueryList[i] = testQueryList[i].lower()

    # Получения текста страницы с знаками переноса строк и препинания. Прием с использованием регулярных выражений
    wordList = re.compile("[\\w]+|[\\n.,!?:—]").findall(testText)

    # Получить html-код с маркировкой искомых слов
    htmlCode = getMarkedHTML(wordList, testQueryList)
    print(htmlCode)

    # сохранить html-код в файл с указанным именем
    file = open(markedHTMLFilename, 'w', encoding="utf-8")
    file.write(htmlCode)
    file.close()


def getMarkedHTML(self, wordList, queryList):
    """Генерировть html-код с макркировкой указанных слов цветом
    wordList - список отдельных слов исходного текста
    queryList - список отдельных искомых слов,
    """

    # ... подробнее в файле примере
    return resultHTML


testText = """ Владимир Высоцкий — Песня о друге.
    Если друг оказался вдруг..."""
testQueryList = ["если", "он"]  # в нижнем регистре
markedHTMLFilename = "getMarkedHTML.html"

mySeacher.createMarkedHtmlFile(markedHTMLFilename, testText, testQueryList)

pass