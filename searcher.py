import sqlite3 as sql
import searchRequest
import os


class Searcher:
    def __init__(self, dbName):
        self.connection = sql.connect(dbName)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def request_search(self, request):
        searchRequest.db_process_request(self, request)

    #

    #

    #


def main():
    dbname = os.getcwd() + "/LR1_2.db"
    request = "рамблер часов"

    searcher = Searcher(dbname)
    searcher.request_search(request)


main()
