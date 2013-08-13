from unittest import TestCase
from davstorage.utils import trim_trailing_slash


class TrimTrailingSlashTest(TestCase):
    def test_url_without_slash(self):
        url = 'http://example.com'
        self.assertEqual(url, trim_trailing_slash(url))

    def test_url_with_trailing_slash(self):
        url = 'http://example.com/'
        self.assertEqual(url[:-1], trim_trailing_slash(url))
