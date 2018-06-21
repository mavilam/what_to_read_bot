# -*- coding: utf-8 -*-

import unittest
from bs4 import BeautifulSoup
import requests


class Scrapping(unittest.TestCase):
    url_lcdl = "https://www.casadellibro.com/libros-mas-vendidos/20?gclid=Cj0KCQjwz_TMBRD0ARIsADfk7hSKfsQ-Ec1IyAu1AdZBNz994EIF6EAyB6FVaTRgWzdsoNMT9rDw0nMaAvQdEALw_wcB"
    url_fiction = "https://www.fnac.es/n2433/Novela-de-Ciencia-Ficcion-y-Fantasy/Libros-mas-vendidos-Ciencia-Ficcion-y-Fantasy"
    url_nonfiction = "https://www.fnac.es/c19449/No-ficcion"
    url_laCentral = "https://www.lacentral.com/web/masvendidos/"

    def test_urls_are_up(self):
        self.assertEqual(self.request_url(self.url_lcdl), 200)
        self.assertEqual(self.request_url(self.url_fiction), 200)
        self.assertEqual(self.request_url(self.url_nonfiction), 200)
        self.assertEqual(self.request_url(self.url_laCentral), 200)

    def test_laCasaDelLibro_same_structure(self):
        entries = self.get_entries(self.url_lcdl, 'div', 'class', 'carousel-inner')
        entry = entries[0]
        titles = entry.find_all('a', {'class': 'title-link'}, limit=5)
        self.assertTrue(len(titles) > 0)

        entry = entries[1]
        titles = entry.find_all('a', {'class': 'title-link'}, limit=5)
        self.assertTrue(len(titles) > 0)

    @staticmethod
    def request_url(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/'}
        req = requests.get(url, headers=headers)

        status_code = req.status_code
        return status_code

    @staticmethod
    def get_entries(url, father_struct, struct, class_name):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/'}
        req = requests.get(url, headers=headers)

        status_code = req.status_code
        if status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            entries = html.find_all(father_struct, {struct: class_name})
            return entries
        else:
            return []


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Scrapping)
    unittest.TextTestRunner(verbosity=2).run(suite)
