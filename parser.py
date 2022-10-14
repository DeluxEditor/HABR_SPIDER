#import requests
#from bs4 import BeutifulSoup

import urllib2
from BeautifulSoup import *
from urlparse import urljoin

url = "http://habr.com/"
c=urllib2.urlopen(url)
contents=c.read( )
print (contents[0:50])

class crawler:
    #Spider initialization with database name
    def __init__(self,dbHABR):
        pass

    def __del__(self):
        pass

    def dbcommit(self):
        pass

    def getentryid(self,table,field,value,createnew=True):
        return None

    def addtoidex(self,url,soup):
        print ('Индексируется %s' % url)

    def gettextonly(self,soup):
        return None

    def separetewords(self, text):
        return None

    def isindexed(self, url):
        return False

    def addlinkref(self,urlForm,urlTo,linkText):
        pass

    def crawl(self,pages,depth=2):
        pass

    def createindextabels(self):
        pass



    def separatewords(self,text):
        return None

    def isindexed(self,url):
        return False

