import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite

# Create a list of words to ignore
ignorewords= set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])

class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getentryid(self, table, field, value, createnew=True):
        return None

    # Index an individual page
    def addtoindex(self, url, soup):
        print 'Indexing %s' % url

    # Extract the text from an HTML page (no tag)
    def gettextonly(self, soup):
        v = soup.Starting
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()


    # Separate the words by any non-whitespace character
    def separatewords(self, text):
        splitter = re.compile('\\w*')
        return [s.lower() for s in splitter.split(text) if s != '']

    # Return true if this url is already indexed
    def isindexed(self, url):
        return False

    # Add a link between two pages
    def addlinkref(self, urlForm, urlTo, linkText):
        pass

    # Starting with a list of pages, do a breadth
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page, soup)

                links = soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)

                self.dbcommit()
            pages = newpages

    # Create the database tables
    def createindextables(self):
        self.con.excute('create table urllist(url)')
        self.con.excute('create table wordlist(word)')
        self.con.excute('create table wordlocation(urlid, wordid, location)')
        self.con.excute('create table link(fromid integer, toid integer)')
        self.con.excute('create table linkwords(wordid, linkid)')
        self.con.excute('create index wordidx on wordlist(word)')
        self.con.excute('create index urlidx on urllist(url)')
        self.con.excute('create index wordurlidx on wordlocation(wordid)')
        self.con.excute('create index urltoidx on link(toid)')
        self.con.excute('create index urlfromidx on link(fromid)')
        self.dbcommit()

pagelist = ['http://fuzhii.com']
spider = crawler('searchindex.db')
spider.createindextables()
# spider.crawl(pagelist)