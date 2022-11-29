import sqlite3 as sql
import os
import searchRequest
import pageSort
import pageRank


class Searcher:
    def __init__(self, dbname):
        self.connection = sql.connect(dbname)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def resultlist_doing(self, pagescore):
        pagescore = dict(sorted(pagescore.items(), key=lambda item: item[1]))
        urllist = list()
        for key, value in pagescore.items():
            url = self.cursor.execute(
                f"SELECT url from urlList where urlId = '{key}'"
            ).fetchone()
            urllist.append(url)
        urllist.reverse()
        return urllist

    def request_search(self, dbname, request):
        if request == '':
            exitcode = -1
            description = "Request error: empty request was found"
            return exitcode, description

        urlids, worids, exitcode, description = searchRequest.db_process_request(self, request)
        if exitcode != 0:
            return exitcode, description

        locscore = pageSort.location_score(urlids)
        distscore = pageSort.distance_score(urlids)
        freqscore = pageSort.frequency_score(urlids)
        # Это надо будет переписать
        recalcpagerank = 0
        if recalcpagerank:
            pageRank.calculatepagerank(dbname)
        rankscore = pageRank.pagerankscore(dbname, urlids)

        overallscore = dict()
        for key in locscore.keys():
            overallscore[key] = locscore[key]
            overallscore[key] += 0.8 * rankscore[key]
            overallscore[key] += 0.6 * distscore[key]
            overallscore[key] += 0.4 * freqscore[key]
        overallscore = pageSort.score_normalization(overallscore)
        print(f"Итоговый рейтинг страниц: \n{overallscore}\n")

        return 0, '', self.resultlist_doing(overallscore)

    def bestpage_print(self, pagescore):
        pass


def main():
    dbname = os.getcwd() + "/LR1_2.db"
    request = "rambler рамблер"

    searcher = Searcher(dbname)
    exitcode, description, result = searcher.request_search(dbname, request)
    print(f"Результат выдачи: ")
    i = 0
    for url in result:
        i += 1
        print(f'{i}: {url}')

    print(f"Search request finished with exitcode {exitcode}: {description}")
    exit(exitcode)


main()
