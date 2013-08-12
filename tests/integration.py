from __future__ import unicode_literals
import os
import shutil
from unittest import TestCase
from django.core.files.base import ContentFile
from davstorage.storage import DavStorage

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

INTERNAL_URL = 'http://vagrant:vagrant@localhost:9000/'
EXTERNAL_URL = 'http://localhost:9000/'


def clean_data_dir():
    shutil.rmtree(DATA_DIR, ignore_errors=True)
    os.mkdir(DATA_DIR)


def save_in_data_dir(name, content):
    path = os.path.join(DATA_DIR, name)
    with open(path, 'wb') as f:
        f.write(content)


class IntegrationStorageTest(TestCase):
    """Test storage on real server"""

    def setUp(self):
        clean_data_dir()
        self.storage = DavStorage(INTERNAL_URL, EXTERNAL_URL)
        self.content = ContentFile(b'Hello, world!', 'hello.txt')

    def assertFileExist(self, name):
        path = os.path.join(DATA_DIR, name)
        msg = 'File %s does not exist' % name
        self.assertTrue(os.path.exists(path), msg)

    def assertFileDoesNotExist(self, name):
        path = os.path.join(DATA_DIR, name)
        msg = 'File %s exist, but should not' % name
        self.assertFalse(os.path.exists(path), msg)

    def test_file_does_not_exist(self):
        self.assertFalse(self.storage.exists('hello.txt'))

    def test_file_upload(self):
        self.storage.save('hello.txt', self.content)
        self.assertFileExist('hello.txt')

    def test_uploaded_file_exists(self):
        save_in_data_dir('hello.txt', b'Hello, world!')
        self.assertTrue(self.storage.exists('hello.txt'))

    def test_delete_file(self):
        save_in_data_dir('hello.txt', b'Hello, world!')
        self.storage.delete('hello.txt')
        self.assertFileDoesNotExist('hello.txt')

    def test_open_file(self):
        save_in_data_dir('hello.txt', b'Hello, world!')
        f = self.storage.open('hello.txt')
        content = f.read()
        self.assertEqual(content, b'Hello, world!')

    def test_url(self):
        url = self.storage.url('hello.txt')
        self.assertEqual(url, "%s/hello.txt" % EXTERNAL_URL)

    def test_size(self):
        content = b'Hello, world!'
        save_in_data_dir('hello.txt', content)
        size = len(content)
        self.assertEqual(size, self.storage.size('hello.txt'))

    def test_listdir_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.storage.listdir('stuff')