import sqlite3
import datetime
import requests
import bs4
import random
import os
import time
import re #Нужен для поиска текста на сайте

#Создать список игнорируемых
ignorewords=['the','of','to','and','a','in','is','it']

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
        self.DBname = dbFileName
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

        self.curs = self.conection.cursor()

        # 1. Таблица wordlist -----------------------------------------------------
        # Удалить таблицу wordlist из БД
        sqlDropWordlist = """DROP TABLE   IF EXISTS    wordlist;  """
        print(sqlDropWordlist)
        self.curs.execute(sqlDropWordlist)

        # Сформировать SQL запрос
        sqlCreateWordlist = """
            CREATE TABLE   IF NOT EXISTS   wordlist (
        	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
        	    word TEXT   NOT NULL, -- слово
        	    isFiltred INTEGER     -- флаг фильтрации
            );
        """
        print(sqlCreateWordlist)
        self.curs.execute(sqlCreateWordlist)

        # 2. Таблица urllist -------------------------------------------------------
        sqlDropURLlist = """DROP TABLE   IF EXISTS    urllist;  """
        print(sqlDropURLlist)
        self.curs.execute(sqlDropURLlist)

        sqlCreateURLlist = """
            CREATE TABLE   IF NOT EXISTS   urllist (
        	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
        	    url TEXT -- адрес
            );
        """
        print(sqlCreateURLlist)
        self.curs.execute(sqlCreateURLlist)

        # 3. Таблица wordlocation ----------------------------------------------------
        sqlDropWordLocation = """DROP TABLE   IF EXISTS    wordlocation;  """
        print(sqlDropWordLocation)
        self.curs.execute(sqlDropWordLocation)

        sqlCreateWordLocation = """
                   CREATE TABLE   IF NOT EXISTS   wordlocation (
               	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
               	    fk_wordid INTEGER,     -- привязка слова к номеру
               	    fk_urlid INTEGER,     -- привязка номера url к слову
               	    location INTEGER     -- привязка слова к номеру
                   );
               """
        print(sqlCreateWordLocation)
        self.curs.execute(sqlCreateWordLocation)

        # 4. Таблица linkbeetwenurl --------------------------------------------------
        sqlDropLinkBeetwenURL = """DROP TABLE   IF EXISTS    linkbeetwenurl;  """
        print(sqlDropLinkBeetwenURL)
        self.curs.execute(sqlDropLinkBeetwenURL)

        sqlCreateLinkBeetwenURL = """
                   CREATE TABLE   IF NOT EXISTS   linkbeetwenurl (
               	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
               	    fk_fromurl_id INTEGER,     -- привязка слова к номеру
               	    fk_tourl_id INTEGER     -- привязка слова к номеру
                   );
               """
        print(sqlCreateLinkBeetwenURL)
        self.curs.execute(sqlCreateLinkBeetwenURL)

        # 5. Таблица linkwords -------------------------------------------------------
        sqlDropLinkWords = """DROP TABLE   IF EXISTS    linkwords;  """
        print(sqlDropLinkWords)
        self.curs.execute(sqlDropLinkWords)

        sqlCreateLinkWords = """
                   CREATE TABLE   IF NOT EXISTS   linkwords (
               	    rowid  INTEGER   PRIMARY KEY   AUTOINCREMENT, -- первичный ключ
               	    fk_wordid INTEGER,     -- привязка слова к номеру страницы в древе
               	    fk_linkid INTEGER     -- номер ссылки к крирпрму привязаны слова
                   );
               """
        print(sqlCreateLinkWords)
        self.curs.execute(sqlCreateLinkWords)
        pass

    # 6. Непосредственно сам метод сбора данных.
    # Начиная с заданного списка страниц, выполняет поиск в ширину
    # до заданной глубины, индексируя все встречающиеся по пути страницы
    def crawl(self, urlList, maxDepth=1):
        for currDepth in range(maxDepth):

            print("===========Глубина обхода ", currDepth, "=====================================")
            counter = 0  # счетчик обработанных страниц
            nextUrlSet = set()  # создание Множество(Set) следующих к обходу элементов

            # Вар.1. обход каждого url на текущей глубине
            # for url in  urlList:
            # шаг-1. Выбрать url-адрес для обработки

            # Вар.2. обход НЕСКОЛЬКИХ url на текущей глубине
            for num in range(5):

                # шаг-1. Выбрать url-адрес для обработки
                numUrl = random.randint(0, len(urlList) - 1)  # назначить номер элемента в списке urlList
                url = urlList[numUrl]  # получить url-адрес из списка
                print(numUrl)

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
                title = soup.find('title')
                print(" ", title)

                # шаг-4. Найти на странице блоки со скриптами и стилями оформления ('script', 'style')
                listUnwantedItems = ['script', 'style', 'http://www.facebook.com','https://www.facebook.com','http://twitter.com','https://twitter.com']
                for script in soup.find_all(listUnwantedItems):
                    script.decompose()  # очистить содержимое элемента и удалить его из дерева

                # шаг-5. Добавить содержимого страницы в Индекс
                self.addIndex(soup, url)
                self.getTextOnly(soup)

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
                            """if nextUrl.startswith('http://www.facebook.com') or \
                                    nextUrl.startswith('https://www.facebook.com'):
                                continue
                            elif nextUrl.startswith('http://twitter.com') or \
                                    nextUrl.startswith('https://twitter.com'):
                                continue"""
                            print("Ссылка    подходящая ", nextUrl)
                            nextUrlSet.add(nextUrl)


                            self.curs.execute(f"SELECT * FROM urllist WHERE url = ?", (nextUrl,))
                            self.curs.execute("INSERT INTO urllist (url) VALUES(?)", (nextUrl,))
                            self.conection.commit()

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
        """ try:
            self.curs.execute("BEGIN)")
            # проверить, присутсвует ли url в БД  (Таблица urllist в БД)
            isIndexed = self.curs.execute(f"SELECT * FROM urllist WHERE url = ?", (nextUrl,))
        except:
        """
            # проверить, присутсвуют инф о найденных словах по адресу url (Таблица wordlocation в БД)
        return False

    # 1. Индексирование одной страницы
    def addIndex(self, soup, url):
        print("      addIndex")
        if self.isIndexed(url): return
        print('Индексируется ' + url)

        # Получить список слов
        text = self.getTextOnly(soup)
        words = self.separateWords(text)

        #Полкучить идентификатор URL
        urlid = self.getEntryId('urllist', 'url', url)

        # Связать каждое слово с этим URL
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getEntryId('wordlist', 'word', word)
            self.conection.execute("INSERT INTO wordlocation (fk_urlid,fk_wordid,location) values (%d,%d,%d)" % (urlid, wordid, i))

        # проверить, была ли проиндексирован данных url   - isIndexed
        # если не был, то
        #   получить тестовое содержимое страницы - getTextOnly
        #   получить список отдельных слов        - separateWords
        #   Для каждого найденного слова currentword в списке wordList[]
        #     получить id_слова для currentword   -  getEntryId(‘Таблица wordlist в БД’, ‘столбец word’, ‘currentword ’)
        #     внести данные id_слова + id_url + положение_слова в таблицу wordLocation

    # 2. Разбиение текста на слова
    def getTextOnly(self, soup): #text = html_doc in function "def getTextOnly(html_doc)"
        v=soup.get_text()
        if v==None:
            c=soup.contents
            resulttext=''
            for t in c:
                subtext=self.getTextOnly(t)
                resulttext+=subtext+'\n'
            return resulttext
        else:
            return v.strip()




    # 3. Разбиение текста на слова
    def separateWords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    # 4. Проиндексирован ли URL
    def isIndexed(self,url):
        u = self.conection.execute("SELECT rowid FROM urllist WHERE url='%s'" % url).fetchone()
        if u != None:
            # Проверяем, что страница посещалась
            v = self.conection.execute('SELECT * FROM wordlocation WHERE fk_urlid=%d' % u[0]).fetchone()
            if v != None: return True
        return False

        # проверить, присутствует ли url в БД  (Таблица urllist в БД)
        # проверить, присутствует ли инф о найденных словах по адресу url (Таблица wordlocation в БД)

    # 5. Добавление ссылки с одной страницы на другую
    def addLinkRef(urlFrom, urlTo, linkText):
        # добавить инф. в таблицу БД  linkbeetwenurl
        # добавить инф. в таблицу БД  linkwords
        pass

    # 8. Вспомогательная функция для получения идентификатора и
    # добавления записи, если такой еще нет
    def getEntryId(self, tableName, fieldName, value,createnew=True):
        cur = self.conection.execute("SELECT rowid FROM %s WHERE %s='%s'" % (tableName, fieldName, value))
        res = cur.fetchone()
        if res == None:
            cur = self.conection.execute("INSERT INTO %s (%s) VALUES ('%s')" % (tableName, fieldName, value))
            return cur.lastrowid
        else:
            return res[0]
        pass

    # конец класса


# ---------------------------------------------------
def main():
    cwd = os.getcwd()
    dBname = cwd + '/LR1_2.db'
    myCrawler = Crawler(dBname)
    myCrawler.initDB()

    ulrList = list()
    ulrList.append("https://habr.com/")
    ulrList.append("https://fincult.info/")
    ulrList.append("https://finance.rambler.ru/")

    # Запуск кравлера и замер времени его работы
    start_time = time.time()
    myCrawler.crawl(ulrList, 2)
    print("--- %s seconds ---" % (time.time() - start_time))

    pass


# ---------------------------------------------------
main()
