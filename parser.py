import sqlite3
import datetime
import requests
import bs4
import random

import re

"""for link in soup.find_all("a"):
    href = link.get("href", "")
    if "archive" in href:
        print("text: ", link.text, "\n ", "spurce: ", f"{url}{href[1:]}", "\n", sep="")
def request_page(url):
    proxies = {
        "http": "socks5h://127/0/0/1:9050",
        "https": "socks5h://127/0/0/1:9050",
    }
    return requests.get(url, proxies=proxies)"""

class Crawler:

    # 0. Конструктор Инициализация паука с параметрами БД
    def __init__(self, dbFileName):
        print("Конструктор")
        self.conection = sqlite3.connect(dbFileName)
        pass

    # 0. Деструктор
    def __del__(self):
        print("Деструктор")
        self.conection.commit()  # зафиксировать последние изменения
        self.conection.close()  # закрыть соединение
        pass

    # 7. Инициализация таблиц в БД
    def initDB(self):
        print("Создать пустые таблицы с необходимой структурой")

        curs = self.conection.cursor()

        # 1. Таблица wordlist -----------------------------------------------------
        # Удалить таблицу wordlist из БД
        sqlDropWordlist = """DROP TABLE   IF EXISTS    wordlist;  """
        print(sqlDropWordlist)
        curs.execute(sqlDropWordlist)

        # Сформировать SQL запрос
        sqlCreateWordlist = """
            CREATE TABLE   IF NOT EXISTS   wordlist (
        	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
        	    word TEXT   NOT NULL, -- слово
        	    isFiltred INTEGER     -- флаг фильтрации
            );
        """
        print(sqlCreateWordlist)
        curs.execute(sqlCreateWordlist)

        # 2. Таблица urllist -------------------------------------------------------
        sqlDropURLlist = """DROP TABLE   IF EXISTS    urllist;  """
        print(sqlDropURLlist)
        curs.execute(sqlDropURLlist)

        sqlCreateURLlist = """
            CREATE TABLE   IF NOT EXISTS   urllist (
        	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
        	    url TEXT -- адрес
            );
        """
        print(sqlCreateURLlist)
        curs.execute(sqlCreateURLlist)

        # 3. Таблица wordlocation ----------------------------------------------------
        sqlDropWordLocation = """DROP TABLE   IF EXISTS    wordlocation;  """
        print(sqlDropWordLocation)
        curs.execute(sqlDropWordLocation)

        sqlCreateWordLocation = """
                   CREATE TABLE   IF NOT EXISTS   wordlocation (
               	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
               	    fk_wordid INTEGER,     -- привязка слова к номеру
               	    fk_urlid INTEGER,     -- привязка номера url к слову
               	    location INTEGER     -- привязка слова к номеру
                   );
               """
        print(sqlCreateWordLocation)
        curs.execute(sqlCreateWordLocation)

        # 4. Таблица linkbeetwenurl --------------------------------------------------
        sqlDropLinkBeetwenURL = """DROP TABLE   IF EXISTS    linkbeetwenurl;  """
        print(sqlDropLinkBeetwenURL)
        curs.execute(sqlDropLinkBeetwenURL)

        sqlCreateLinkBeetwenURL = """
                   CREATE TABLE   IF NOT EXISTS   linkbeetwenurl (
               	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
               	    fk_fromurl_id INTEGER,     -- привязка слова к номеру
               	    fk_tourl_id INTEGER     -- привязка слова к номеру
                   );
               """
        print(sqlCreateLinkBeetwenURL)
        curs.execute(sqlCreateLinkBeetwenURL)

        # 5. Таблица linkwords -------------------------------------------------------
        sqlDropLinkWords = """DROP TABLE   IF EXISTS    linkwords;  """
        print(sqlDropLinkWords)
        curs.execute(sqlDropLinkWords)

        sqlCreateLinkWords = """
                   CREATE TABLE   IF NOT EXISTS   linkwords (
               	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
               	    fk_wordid INTEGER,     -- привязка слова к номеру страницы в древе
               	    fk_linkid INTEGER     -- номер ссылки к крирпрму привязаны слова
                   );
               """
        print(sqlCreateLinkWords)
        curs.execute(sqlCreateLinkWords)
        pass

    # 6. Непосредственно сам метод сбора данных.
    # Начиная с заданного списка страниц, выполняет поиск в ширину
    # до заданной глубины, индексируя все встречающиеся по пути страницы
    def crawl(self, urlList, maxDepth=1):

        for currDepth in range(0, maxDepth):

            print("===========Глубина обхода ", currDepth, "=====================================")
            counter = 0  # счетчик обработанных страниц
            nextUrlSet = set()  # создание Множество(Set) следующих к обходу элементов

            # Вар.1. обход каждого url на текущей глубине
            # for url in  urlList:
            # шаг-1. Выбрать url-адрес для обработки

            # Вар.2. обход НЕСКОЛЬКИХ url на текущей глубине
            for num in range(0, 5):

                # шаг-1. Выбрать url-адрес для обработки
                numUrl = random.randint(0, len(urlList) - 1)  # назначить номер элемента в списке urlList
                url = urlList[numUrl]  # получить url-адрес из списка

                counter += 1
                curentTime = datetime.datetime.now().time()

                try:
                    print("{}/{} {} Попытка открыть {} ...".format(counter, len(urlList), curentTime, url))
                    # шаг-2. Запрашивать HTML-код
                    html_doc = requests.get(url).text  # получить HTML код страницы

                except Exception as e:
                    # обработка исключений при ошибке запроса содержимого страницы
                    print(e)
                    continue  # перейти к следующему url

                # шаг-3. Разобрать HTML-код на составляющие
                soup = bs4.BeautifulSoup(html_doc, "html.parser")
                print(" ", soup.title.text)

                # шаг-4. Найти на странице блоки со скриптами и стилями оформления ('script', 'style')
                listUnwantedItems = ['script', 'style']
                for script in soup.find_all(listUnwantedItems):
                    script.decompose()  # очистить содержимое элемента и удалить его из дерева

                # шаг-5. Добавить содержимого страницы в Индекс
                self.addIndex(soup, url)

                # шаг-6. Извлечь с данный страницы инф о ссылка на внешние узлы = получить все тэги <a> = получить все ссылки

                # linksOnCurrentPage = получить все тэги <a>
                linksOnCurrentPage = soup.find_all('a')

                # Обработать каждую ссылку <a>
                for tagA in linksOnCurrentPage:

                    # Проверить начиличе атрибута 'href' у тега <a> (атрибуты находятся в структуре Cловарь Dictionary)
                    if ('href' in tagA.attrs):
                        # Проверка соответвия ссылок ВАШИМ требованиям
                        nextUrl = tagA.attrs['href']

                        # Выбор "подходящих" ссылок => если ссылка начинается с "http"
                        if nextUrl.startswith('http') or nextUrl.startswith('https'):
                            print("Ссылка    подходящая ",nextUrl)
                            nextUrlSet.add(nextUrl)

                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # добавить инф о ссылке в БД  -  addLinkRef(  url,  nextUrl)
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                        else:
                            print("Ссылка не подходящая ", nextUrl)
                            pass
                    else:
                        # атрибут href отсутствует
                        continue
                # конец цикла для обработки тега <a>

            # шаг-8. Добавить найденые ссылки на другие страницы в "Список очередных сслылок к обходу"
            urlList = list(nextUrlSet)
            # конец обработки всех URL на данной глубине

        pass

    # Проверить, содержится ли данный url в индексе
    #   urlList содержит указанный адрес
    #   wordlocation содержит слова с указанного url
    def isIndexedURL(self, url):
        # проверить, присутсвует ли url в БД  (Таблица urllist в БД)
        # проверить, присутсвуют инф о найденных словах по адресу url (Таблица wordlocation в БД)
        return False

    # 1. Индексирование одной страницы
    def addIndex(self, soup, url):
        print("      addIndex")
        # проверить, была ли проиндексирован данных url   - isIndexed
        # если не был, то
        #   получить тестовое содержимое страницы - getTextOnly
        #   получить список отдельных слов        - separateWords
        #   Для каждого найденного слова currentword в списке wordList[]
        #     получить id_слова для currentword   -  getEntryId(‘Таблица wordlist в БД’, ‘столбец word’, ‘currentword ’)
        #     внести данные id_слова + id_url + положение_слова в таблицу wordLocation

        pass

    # 2. Разбиение текста на слова
    def getTextOnly(text):
        return ""

    # 3. Разбиение текста на слова
    def separateWords(text):
        pass

    # 4. Проиндексирован ли URL
    def isIndexed(url):
        # проверить, присутствует ли url в БД  (Таблица urllist в БД)
        # проверить, присутствует ли инф о найденных словах по адресу url (Таблица wordlocation в БД)
        return False

    # 5. Добавление ссылки с одной страницы на другую
    def addLinkRef(urlFrom, urlTo, linkText):
        # добавить инф. в таблицу БД  linkbeetwenurl
        # добавить инф. в таблицу БД  linkwords
        pass

    # 8. Вспомогательная функция для получения идентификатора и
    # добавления записи, если такой еще нет
    def getEntryId(tableName, fieldName, value):
        return 1

    # конец класса


# ---------------------------------------------------
def main():
    myCrawler = Crawler("mySQLlite_DB_file.db")
    myCrawler.initDB()

    ulrList = list()
    ulrList.append("https://habr.com/")
    ulrList.append("https://fincult.info/")
    ulrList.append("https://club.dns-shop.ru/digest/")

    myCrawler.crawl(ulrList, 2)

    pass


# ---------------------------------------------------
main()
