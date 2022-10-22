import os
import time
import crawler

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

cwd = os.getcwd()
DBname = cwd + '/LR1_2.db'

ignorewords = ['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it']

myCrawler = crawler.Crawler(DBname, ignorewords)
myCrawler.initDB()

ulrList = list()
ulrList.append("https://habr.com/")
ulrList.append("https://fincult.info/")
ulrList.append("https://finance.rambler.ru/")

# Запуск кравлера и замер времени его работы
start_time = time.time()
myCrawler.crawl(ulrList, 2)
print("--- %s seconds ---" % (time.time() - start_time))
