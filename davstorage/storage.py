import requests
from django.core.files.storage import Storage


class DavStorage(Storage):
    def __init__(self, url, external_url):
        self.internal_url = url
        self.external_url = external_url

    def exists(self, name):
        url = '%s/%s' % (self.internal_url, name)
        response = requests.head(url)
        return response.status_code == 200

    def delete(self, name):
        url = '%s/%s' % (self.internal_url, name)
        requests.delete(url)

    def url(self, name):
        return '%s/%s' % (self.external_url, name)

    def size(self, name):
        url = '%s/%s' % (self.internal_url, name)
        response = requests.head(url, headers={'accept-encoding': None})
        return int(response.headers['content-length'])

    def _open(self, name, mode='rb'):
        url = '%s/%s' % (self.internal_url, name)
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        return response.raw

    def _save(self, name, content):
        url = '%s/%s' % (self.internal_url, name)
        requests.put(url, data=content)
        return name
