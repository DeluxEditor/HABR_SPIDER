import os
import time
import pandas as pd
import plotly_express as px
import crawler
import metrics
import topTwelve

cwd = os.getcwd()
DBname = cwd + '/LR1_2.db'

ignorewords = ['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it',
               'и', 'но', 'а', 'как', 'также', 'тоже', 'притом', 'в',
               'зато', 'потому что', 'так как', 'чтобы', 'на', 'не', 'с', 'о', 'по'
               ]

myCrawler = crawler.Crawler(DBname, ignorewords)
myCrawler.initDB()

ulrList = list()
ulrList.append("https://habr.com/")
ulrList.append("https://finuch.ru/")
ulrList.append("https://finance.rambler.ru/")

# Запуск кравлера и замер времени его работы
start_time = time.time()
myCrawler.crawl(ulrList, 2)
print("--- %s seconds ---" % (time.time() - start_time))

worddf = pd.DataFrame(metrics.wordMetrics)
urldf = pd.DataFrame(metrics.urlMetrics)

wordGraf = px.line(worddf, title='Количество добавленных слов за обход',
                   labels={'index': 'Номер обхода', 'value': 'Слова'})
urlGraf = px.line(urldf, title='Количество добавленных ссылок за обход',
                  labels={'index': 'Номер обхода', 'value': 'Ссылки'})

wordGraf.show()
urlGraf.show()

print("\nЗапись топ 20 слов и ссылок в файл...")
logfilename = open("top-twelve.txt", "a")
topTwelve.topWord(DBname, logfilename)
topTwelve.topUrl(DBname, logfilename)
