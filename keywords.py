from selenium import webdriver
import time, random, sys
from bs4 import BeautifulSoup

class Keywords:

    def find_element_by_id(browser, id):
        try:
            return browser.find_element_by_id(id).get_attribute('innerHTML').encode("ascii", "xmlcharrefreplace")
        except Exception as e:
            #print str(e)
            sys.exc_clear()
            return None

    def find_elements_by_tag_name(browser, tag_name):
        try:
            #print "No of rows", len(browser.find_elements_by_tag_name(tag_name)[5:])
            #print browser.find_elements_by_tag_name(tag_name)[5].get_attribute('innerHTML').encode("ascii", "xmlcharrefreplace")
            return browser.find_elements_by_tag_name(tag_name)[5:]
        except Exception as e:
            print str(e)
            sys.exc_clear()
            return None

    def find_all(soup, tag_name, attributes):
        try:
            #print len(soup.find_all(tag_name, attributes))
            return soup.find_all(tag_name, attributes)
        except Exception as e:
            print str(e)
            sys.exc_clear()
            return None

    def find(soup, tag_name):
        try:
            #print len(soup.find_all(tag_name))
            return soup.find(tag_name)
        except Exception as e:
            print str(e)
            sys.exc_clear()
            return None

    def webdriver():
        print "Instantiating Browsers..."
        browsers = list()
        try:
            firefox = webdriver.Firefox()
            print "Creating Firefox driver"
            browsers.append(firefox)
        except Exception as e:
            print "failed... could not create firefox... skipping"
            sys.exc_clear()
        try:
            chrome = webdriver.Chrome()
            print "Creating Chrome driver"
            browsers.append(chrome)
        except Exception as e:
            print "failed... could not create chrome... skipping"
            sys.exc_clear()
        try:
            ie = webdriver.Ie()
            print "Creating IE driver"
            browsers.append(ie)
        except Exception as e:
            print "failed... could not create IE... skipping"
            sys.exc_clear()
        print "done... okay\n"
        return browsers
        
    if __name__ == "__main__":
        print "Initializing..."
        browsers = webdriver()
        topDomainIDs = [2]
        print "Domains: ", topDomainIDs
        subDomainIDs = range(25)
        print "SubDomains: ", subDomainIDs,"\n"
        for topDomainID in topDomainIDs:
            print "Current Domain:", topDomainID
            for subDomainID in subDomainIDs:
                rid = 0
                file = open('keywords-publications-citations-top'+str(topDomainID)+'-sub'+str(subDomainID)+'.csv', 'wb')
                file.write("#,Keyword,Publications,Citations\n")
                print "Current SubDomain:", subDomainID
                start = 1
                end = 100
                url = "http://academic.research.microsoft.com/RankList?entitytype=8&topDomainID={0}&subDomainID={1}&last=0&start={2}&end={3}".format(topDomainID, subDomainID, start, end)
                ranklistresult = None
                k = 0
                while ranklistresult == None:
                    browser  = random.choice(browsers)
                    browser.get(url)
                    ranklistresult = find_element_by_id(browser, "ctl00_MainContent_lblResultMessage")
                    if ranklistresult == None:
                        t = random.randrange(pow(2, k))*random.random()
                        print "Retrying in",t,"seconds"
                        time.sleep(t)
                        if k <= 10:
                            k = k + 1
                k = 0
                ranklistresult = int(ranklistresult[ranklistresult.index('of'):].replace('of ', '').replace(' results', '').replace(',', ''))
                print "Total:", ranklistresult
                ranklistresult = 1000
                while start <= ranklistresult:
                    url = "http://academic.research.microsoft.com/RankList?entitytype=8&topDomainID={0}&subDomainID={1}&last=0&start={2}&end={3}".format(topDomainID, subDomainID, start, end)
                    rows = None
                    while rows == None or rows == [] or rows == '':
                        browser  = random.choice(browsers)
                        browser.get(url)
                        rows = find_elements_by_tag_name(browser, 'tr')
                        if rows == None or rows == [] or rows == '':
                            t = random.randrange(pow(2, k))*random.random()
                            print "Retrying in",t,"seconds"
                            time.sleep(t)
                            if k <= 10:
                                k = k + 1
                    k = 0
                    for row in rows:
                        row = row.get_attribute('innerHTML').encode("ascii", "xmlcharrefreplace")
                        soup = BeautifulSoup(row)
                        keyword = str(find(soup, 'a').text)
                        publications = int(find_all(soup, 'td', {'class' : 'staticOrderCol'})[0].text)
                        citations = int(find_all(soup, 'td', {'class' : 'staticOrderCol'})[1].text)
                        rid = rid + 1
                        print rid, keyword, publications, citations
                        file.write("{0},{1},{2},{3}\n".format(rid, keyword, publications, citations))
                    start = start + 100
                    end = end + 100
                file.close()
        print "done... finished... okay"
        print "closing browsers"
        for browser in browsers:
            browser.close()
        print "see file output"
