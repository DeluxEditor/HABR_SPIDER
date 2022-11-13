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

    def request_search(self, dbname, request):
        if request == '':
            exitcode = -1
            description = "Request error: empty request was found"
            return exitcode, description

        urlids, worids, exitcode, description = searchRequest.db_process_request(self, request)
        if exitcode != 0:
            return exitcode, description

        pageSort.location_score(urlids)
        pageSort.distance_score(urlids)
        pageSort.frequency_score(urlids)
        # Это надо будет переписать
        pageRank.calculatepagerank(dbname)
        pageRank.pagerankscore(dbname, urlids)

        return 0, ''


def main():
    dbname = os.getcwd() + "/LR1_2.db"
    request = "rambler рамблер"

    searcher = Searcher(dbname)
    exitcode, description = searcher.request_search(dbname,request)
    print (f"Search request finished with exitcode {exitcode}: {description}")
    exit(exitcode)

main()
