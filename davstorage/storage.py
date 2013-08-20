from __future__ import unicode_literals
import requests
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from davstorage.utils import trim_trailing_slash


class DavStorage(Storage):
    def __init__(self, internal_url=None, external_url=None):
        if internal_url is None and external_url is None:
            internal_url = settings.DAVSTORAGE_PRIVATE_URL
            external_url = settings.DAVSTORAGE_PUBLIC_URL
        self._internal_url = trim_trailing_slash(internal_url)
        self._external_url = trim_trailing_slash(external_url)

    def exists(self, name):
        url = self.internal_url(name)
        response = requests.head(url)
        return response.status_code == 200

    def delete(self, name):
        url = self.internal_url(name)
        requests.delete(url)

    def size(self, name):
        url = self.internal_url(name)
        response = requests.head(url, headers={'accept-encoding': None})
        content_length = response.headers.get('content-length')
        try:
            return int(content_length)
        except (TypeError, ValueError):
            return None

    def url(self, name):
        return '%s/%s' % (self._external_url, name)

    def internal_url(self, name):
        return '%s/%s' % (self._internal_url, name)

    def _open(self, name, mode='rb'):
        url = self.internal_url(name)
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        return File(response.raw, name)

    def _save(self, name, content):
        url = self.internal_url(name)
        requests.put(url, data=content)
        return name
