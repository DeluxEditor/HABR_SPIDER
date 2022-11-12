import sqlite3 as sql
import os
import searchRequest
import pageSort


class Searcher:
    def __init__(self, dbName):
        self.connection = sql.connect(dbName)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def request_search(self, request):
        if request == '':
            exitcode = -1
            description = "Request error: empty request was found"
            return exitcode, description

        urlids, worids, exitcode, description = searchRequest.db_process_request(self, request)
        if exitcode != 0:
            return exitcode,description

        pageSort.location_score(urlids)
        pageSort.distance_score(urlids)

        return 0, ''


def main():
    dbname = os.getcwd() + "/LR1_2.db"
    request = "Рамблер начало"

    searcher = Searcher(dbname)
    exitcode, description = searcher.request_search(request)
    print (f"Search request finished with exitcode {exitcode}: {description}")
    exit(exitcode)

main()
