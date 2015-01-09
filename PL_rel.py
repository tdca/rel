'''
  rel.py is a tiny script to show the relationship between
programming languages with data from Wikipedia.

requires:
    requests
    lxml
'''
import requests
import StringIO
import marshal
from datetime import date
from lxml.html import etree

'''
    rel : {
        "Java" : {
            "name": "Java"
            "url": "http://..."
            "influenced": [...]
            "influenced-by": [...]
        }
    }
'''
rel = {}
waiting = set()
wiki_url = "http://en.wikipedia.com"
xpath_tpl = '//th[.="%s"]/../following-sibling::*[1]/td/a[@title]'

def parse(url):
    return etree.parse(StringIO.StringIO(requests.get(url).text))

def title(a):
    if not rel.has_key(a.attrib['title']):
        waiting.add((a.attrib['title'], wiki_url+a.attrib['href']))
    return a.attrib['title']

def find_by_xpath(xml, xpath, mapper = None):
    result = xml.xpath(xpath)
    if not result:
        return []
    return map(mapper, result)

def find_influenced(xml):
    return find_by_xpath(xml, xpath_tpl%("Influenced"), title)

def find_influenced_by(xml):
    return find_by_xpath(xml, xpath_tpl%("Influenced by"), title)

def plrel(pl_title, pl_url):
    wiki = parse(pl_url)
    rel[pl_title] = {
        "name": pl_title,
        "url": pl_url,
        "influenced": find_influenced(wiki),
        "influenced-by": find_influenced_by(wiki)
        }
    if((pl_title, pl_url) in waiting):
        waiting.remove((pl_title, pl_url))
    return rel[pl_title]

if __name__ == '__main__':
    plrel("Python (programming language)",
          'http://en.wikipedia.org/wiki/Python_%28programming_language%29')
    for i in range(3):
        for z in waiting.copy():
            print z
            apply(plrel, z)
    with open('REL-%s.dat'%(date.today().strftime("%b-%d-%Y")), "wb") as f:
        marshal.dump(rel, f)
