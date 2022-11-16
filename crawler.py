import sqlite3
import bs4
import datetime
import requests
import createDB
import addToIndex
import metrics
import textOnly
import isIndexed

listUnwantedItems = ['script', 'style', 'http://www.facebook.com','https://www.facebook.com',
                                     'http://twitter.com','https://twitter.com']

class Crawler:
    def __init__(self, dbFileName, blackList):
        self.conection = sqlite3.connect(dbFileName)
        self.cursor = self.conection.cursor()
        self.ignorewords = blackList

    def __del__(self):
        self.conection.commit()
        self.conection.close()

    initDB = createDB.createDB
    addIndex = addToIndex.addIndex
    isIndexed = isIndexed.isIndexed
    getTextOnly = textOnly.getTextOnly

    def addLinkRef(self, urlFrom, urlTo):
        try:
            self.cursor.execute(f"SELECT urlId FROM urlList WHERE url = '{urlFrom}'")
            idFrom = self.cursor.fetchone()[0]
            self.cursor.execute(f"SELECT urlId FROM urlList WHERE url = '{str(urlTo)}'")
            idTo = self.cursor.fetchone()[0]
            if idTo != None and idFrom != idTo:
                self.cursor.execute(f"INSERT INTO linkBetweenURL (fk_From_urlId, fk_To_urlId) VALUES ('{idFrom}', '{idTo}')")
            self.conection.commit()
        except:
            pass



    def crawl(self, urlList, maxDepth=1):
        for currDepth in range(maxDepth):
            print("===========Глубина обхода ", currDepth, "===========")
            counter = 0
            nextUrlSet = set()

            for url in urlList[:]:
                counter += 1
                curentTime = datetime.datetime.now().time()

                try:
                    print("{}/{} {} Попытка открыть {} ...".format(counter, len(urlList), curentTime, url))
                    html_doc = requests.get(url).text
                except Exception as e:
                    print(e)
                    continue

                soup = bs4.BeautifulSoup(html_doc, "html.parser")
                title = soup.find('title')
                print(" ", title)

                for script in soup.find_all(listUnwantedItems):
                    script.decompose()

                self.addIndex(soup, url)

                linksOnCurrentPage = soup.find_all('a')

                metrics.metricsInsert(self)

                for tagA in linksOnCurrentPage:
                    if not ('href' in tagA.attrs):
                        continue
                    else:
                        nextUrl = tagA.attrs['href']
                        if nextUrl[0:4] == 'http' and not isIndexed.isIndexed(self, nextUrl)\
                                and nextUrl[-4:] != 'epub' and nextUrl[-3:] != 'pdf':
                            # print("Ссылка    подходящая ", nextUrl)
                            nextUrlSet.add(nextUrl)
                            # self.cursor.execute("INSERT INTO urlList (url) VALUES(?)", (nextUrl,))
                            # Добавление связи этой свежей ссылки c текущей в linkBetweenURL

                        else:
                            # print("Ссылка не подходящая ", nextUrl)
                            pass
                    self.addLinkRef(url, nextUrl)
            urlList = list(nextUrlSet)
