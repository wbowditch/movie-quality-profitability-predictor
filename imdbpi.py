#import imdbpie
#import wolframalpha

#client = wolframalpha.Client("P4373U-K839J4Y6VT")

#imdb = imdbpie.Imdb()
#imdb = imdbpie.Imdb(anonymize=True)

#obj = imdb.search_for_title("Star Wars: The Force Awakens")[0]
#title = imdb.get_title_by_id(obj['imdb_id'])
#print dir(title)
#
#id1 = person.imdb_id

#purs = imdb.get_person_by_id(id1)

#print purs.job

import sys
import urllib2
import urllib
import httplib
from xml.etree import ElementTree as etree

class wolfram(object):
    def __init__(self, appid):
        self.appid = appid
        self.base_url = 'http://api.wolframalpha.com/v2/query?'
        self.headers = {'User-Agent':None}

    def _get_xml(self, ip):
        url_params = {'input':ip, 'appid':self.appid}
        data = urllib.urlencode(url_params)
        req = urllib2.Request(self.base_url, data, self.headers)
        xml = urllib2.urlopen(req).read()
        return xml

    def _xmlparser(self, xml):
        data_dics = {}
        tree = etree.fromstring(xml)
        #retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            for item in [ef for ef in list(e) if ef.tag=='subpod']:
                for it in [i for i in list(item) if i.tag=='plaintext']:
                    if it.tag=='plaintext':
                        data_dics[e.get('title')] = it.text
        return data_dics

    def search(self, ip):
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        print result_dics
        #return result_dics
        #print result_dics
        print result_dics['Result']

if __name__ == "__main__":
    appid = sys.argv[1]
    query = sys.argv[2]
    w = wolfram(appid)
    w.search(query)