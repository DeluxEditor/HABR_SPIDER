def isIndexed(self, url):
    u = self.conection.execute("SELECT rowid FROM urllist WHERE url='%s'" % url).fetchone()
    if u != None:
        # Проверяем, что страница посещалась
        v = self.conection.execute("SELECT * FROM wordlocation WHERE fk_urlid='%d'" % u[0]).fetchone()
        if v != None: return True
    return False