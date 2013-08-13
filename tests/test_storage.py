from __future__ import unicode_literals
from unittest import TestCase
from davstorage.storage import DavStorage


class DavStorageTest(TestCase):
    def setUp(self):
        self.storage = DavStorage('http://localhost', 'http://example.com')

    def test_url_simple(self):
        url = self.storage.url('hello.txt')
        self.assertEqual(url, 'http://example.com/hello.txt')
        internal_url = self.storage.internal_url('img.png')
        self.assertEqual(internal_url, 'http://localhost/img.png')

    def test_url_collection(self):
        url = self.storage.url('texts/hello.txt')
        self.assertEqual(url, 'http://example.com/texts/hello.txt')
        internal_url = self.storage.internal_url('pics/cat.jpg')
        self.assertEqual(internal_url, 'http://localhost/pics/cat.jpg')

    def test_url_no_double_slash(self):
        storage = DavStorage('http://localhost/', 'http://example.com/')
        url = storage.url('hello.txt')
        self.assertEqual(url, 'http://example.com/hello.txt')
        internal_url = storage.internal_url('img.png')
        self.assertEqual(internal_url, 'http://localhost/img.png')