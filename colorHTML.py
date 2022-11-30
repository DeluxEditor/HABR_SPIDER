import requests
import bs4
import addToIndex
import re

def create_Marked_File(markedHTMLFilename, url, QueryList):
    # Получение текста страницы
    html_doc = requests.get(url).text
    soup = bs4.BeautifulSoup(html_doc, "html.parser")

    for script in soup.find_all('script', 'style'):
        script.decompose()

    Text = addToIndex.getTextOnly(soup)

    # Приобразование текста к нижнему регистру
    Text = Text.lower()
    QueryList = QueryList.split(' ')
    print(QueryList)
    for i in range(0, len(QueryList)):
        QueryList[i] = QueryList[i].lower()


    # Получения текста страницы с знаками переноса строк и препинания. Прием с использованием регулярных выражений
    wordList = re.compile("[\\w]+|[\\n.,!?:—]").findall(Text)
    print(wordList)

    # Получить html-код с маркировкой искомых слов
    htmlCode = getMarkedHTML(wordList, QueryList)

    # сохранить html-код в файл с указанным именем
    file = open(markedHTMLFilename, 'w', encoding="utf-8")
    file.write(htmlCode)
    file.close()


def getMarkedHTML(wordList, queryList):
    text = []
    i = 0
    htmlCodebegin = "<!DOCTYPE html><html><head></head><body>"
    for word in wordList:
        if word in queryList:
            text.append(f'<span style="background-color:red;">{word}</span>')
        else:
            text.append(str(word))
        i += 1
    htmlCodetext = htmlCodebegin + str(" ".join(map(str, text)))
    htmlCode = htmlCodetext+"</body></html>"
    return htmlCode
