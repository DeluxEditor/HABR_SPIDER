import sqlite3
import bs4
import random
import datetime
import requests
import createDB
import addToIndex
import metrics


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

    def crawl(self, urlList, maxDepth=1):
        for currDepth in range(maxDepth):
            print("===========Глубина обхода ", currDepth, "===========")
            counter = 0
            nextUrlSet = set()

            # Вар.1. обход каждого url на текущей глубине
            # for url in  urlList:

            # Вар.2. обход НЕСКОЛЬКИХ url на текущей глубине
            for url in urlList:

                numUrl = random.randint(0, len(urlList) - 1)
                url = urlList[numUrl]
                print(numUrl)

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

                listUnwantedItems = ['script', 'style', 'http://www.facebook.com','https://www.facebook.com',
                                     'http://twitter.com','https://twitter.com']
                for script in soup.find_all(listUnwantedItems):
                    script.decompose()

                self.addIndex(soup, url)

                linksOnCurrentPage = soup.find_all('a')

                for tagA in linksOnCurrentPage:
                    if not ('href' in tagA.attrs):
                        continue
                    else:
                        nextUrl = tagA.attrs['href']
                        if nextUrl[0:4] == 'http' and not self.isIndexed(nextUrl):
                            print("Ссылка    подходящая ", nextUrl)

                            nextUrlSet.add(nextUrl)
                            self.cursor.execute(f"SELECT * FROM urlList WHERE url = ?", (nextUrl,))
                            self.cursor.execute("INSERT INTO urlList (url) VALUES(?)", (nextUrl,))
                            self.conection.commit()

                            metrics.metricsInsert(self)

                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # добавить инф о ссылке в БД  -  addLinkRef(  url,  nextUrl)
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            linkText = self.getTextOnly(nextUrl)
                            self.addLinkRef(url, nextUrl, linkText)

                        else:
                            print("Ссылка не подходящая ", nextUrl)
                            pass

            urlList = list(nextUrlSet)