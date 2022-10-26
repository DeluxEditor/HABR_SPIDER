def isIndexedURL(self, url):
    """ try:
        self.curs.execute("BEGIN)")
        # проверить, присутсвует ли url в БД  (Таблица urllist в БД)
        isIndexed = self.curs.execute(f"SELECT * FROM urllist WHERE url = ?", (nextUrl,))
    except:
    """
    # проверить, присутсвуют инф о найденных словах по адресу url (Таблица wordlocation в БД)
    pass


def isIndexed(self, url):
    u = self.conection.execute("SELECT rowid FROM urllist WHERE url='%s'" % url).fetchone()
    if u != None:
        # Проверяем, что страница посещалась
        v = self.conection.execute('SELECT * FROM wordlocation WHERE fk_urlid=%d' % u[0]).fetchone()
        if v != None: return True
    return False