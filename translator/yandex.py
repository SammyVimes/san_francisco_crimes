import sys
import urllib
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from xml.dom.minidom import parse, parseString

__author__ = 'Semyon'


def __getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def __translate(list_of_params):
    """Translate given text"""
    url = "https://translate.yandex.net/api/v1.5/tr/translate?%s"
    request = Request(url % urlencode(list_of_params),
                      headers={'User-Agent': 'Mozilla/5.0', 'Accept-Charset': 'utf-8'})
    res = urlopen(request).read()
    translated = parseString(res)
    text = translated.getElementsByTagName("text")
    if text:
        return __getText([child for t in text for child in t.childNodes])
    else:
        return ""


def translate(word, source, target):
    api_key = 'trnsl.1.1.20150901T103125Z.ecc0c763e46aec3d.77f242acc2ab601d1faf69c55692bd14ca6f416c'
    list_of_params = {'key': api_key,
                      'text': word,
                      'lang': target
                      }
    return __translate(list_of_params)
