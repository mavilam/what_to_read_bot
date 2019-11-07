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

    def test_urls_are_up(self):
        for key, value in books_urls.items():
            http_code = self.request_url(value)
            if http_code != 200:
                print(value)
            self.assertEqual(http_code, 200)

    def test_laCasaDelLibro_same_structure(self):
        entries = self.get_entries(books_urls['Casa del libro|Juvenil'], 'html.parser', 'div', 'class', 'product__info')
        self.assertTrue(len(entries) > 0)
        entry = entries[0]
        title = entry.a
        self.assertTrue(title is not None)

    def test_Fnac_same_structure(self):
        entries = self.get_entries(books_urls['Fnac|Más vendidos'], 'html.parser', 'div', 'class', 'Article-infoContent')
        entry = entries[0]
        titles = entry.find('p', {'class': 'Article-descSub'}).findAll('a', limit=5)
        self.assertTrue(len(titles) > 0)

    def test_LaCentral_same_structure(self):
        entries = self.get_entries(books_urls['La Central|Más vendidos'], 'html.parser', 'ul', 'class', 'resultList')
        entry = entries[0]
        titles = entry.find_all('div', {'class': 'content'}, limit=5)
        self.assertTrue(len(titles) > 0)

    def test_Amazon_same_structure(self):
        entries = self.get_entries(books_urls['Amazon|Más vendidos'], 'html5lib', 'span', 'class', 'aok-inline-block zg-item')
        entry = entries[0]
        titles = entry.find_all('div', {'class': 'p13n-sc-truncate p13n-sc-line-clamp-1'}, limit=5)
        self.assertTrue(len(titles) > 0)

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
            entries = html.find_all(father_struct, {struct: class_name})
            return entries
        else:
            return []


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Scrapping)
    unittest.TextTestRunner(verbosity=2).run(suite)
