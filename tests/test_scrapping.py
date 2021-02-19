# -*- coding: utf-8 -*-

import unittest
from bs4 import BeautifulSoup
import requests
import json
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/'}

books_urls = {}
if os.path.exists('/app/static/book_sources.json'):
    with open('/app/static/book_sources.json') as json_data:
        books_urls = json.load(json_data)
else:
    with open('./static/book_sources.json') as json_data:
        books_urls = json.load(json_data)


class Scrapping(unittest.TestCase):
    
    def test_laCasaDelLibro_same_structure(self):
        entries = self.get_entries(books_urls['Casa del libro|Juvenil'], 'html.parser', 'div', 'class', 'col-lg-10 col-9')
        self.assertTrue(len(entries) > 0)
        entry = entries[0]
        title = entry.find('a', {'class': 'title'})
        self.assertTrue(title is not None)

    def test_Fnac_same_structure(self):
        entries = self.get_entries(books_urls['Fnac|Más vendidos'], 'html.parser', 'article', 'class', 'Article-itemGroup')
        entry = entries[0]
        titles = entry.find('div', {'class': 'Article-infoContent'}).findAll('a', limit=5)
        self.assertTrue(len(titles) > 0)

    def test_LaCentral_same_structure(self):
        entries = self.get_entries(books_urls['La Central|Más vendidos'], 'html.parser', 'ul', 'class', 'resultList')
        entry = entries[0]
        titles = entry.find_all('div', {'class': 'content'}, limit=5)
        self.assertTrue(len(titles) > 0)

    def test_Amazon_same_structure(self):
        entries = self.get_entries(books_urls['Amazon|Más vendidos'], 'html5lib', 'span', 'class', 'aok-inline-block zg-item')
        entry = entries[0]
        title = entry.find('img').get('alt')
        author = entry.find('span', {'class': 'a-size-small a-color-base'})
        self.assertTrue(title is not None)
        self.assertTrue(author is not None)

    @staticmethod
    def request_url(url):
        req = requests.get(url, headers=headers)

        status_code = req.status_code
        return status_code

    @staticmethod
    def get_entries(url, parser, father_struct, struct, class_name):
        req = requests.get(url, headers=headers)

        status_code = req.status_code
        if status_code == 200:
            html = BeautifulSoup(req.text, parser)
            entries = html.find_all(father_struct, {struct: class_name}, limit=5)
            return entries
        else:
            return []


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Scrapping)
    unittest.TextTestRunner(verbosity=2).run(suite)
