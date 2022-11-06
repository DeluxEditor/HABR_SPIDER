import os
import time
import pandas as pd
import plotly_express as px
import crawler
import metrics

cwd = os.getcwd()
DBname = cwd + '/LR1_2.db'

ignorewords = ['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it']

myCrawler = crawler.Crawler(DBname, ignorewords)
myCrawler.initDB()

ulrList = list()
ulrList.append("https://habr.com/")
ulrList.append("https://finance.rambler.ru/")

# Запуск кравлера и замер времени его работы
start_time = time.time()
myCrawler.crawl(ulrList, 2)
print("--- %s seconds ---" % (time.time() - start_time))

worddf = pd.DataFrame(metrics.wordMetrics)
urldf = pd.DataFrame(metrics.urlMetrics)

wordGraf = px.line(worddf, title = 'Количество добавленных слов за обход',  labels={'index':'Номер обхода','value':'Слова'})
urlGraf = px.line(urldf, title = 'Количество добавленных ссылок за обход',  labels={'index':'Номер обхода','value':'Ссылки'})

wordGraf.show()
urlGraf.show()