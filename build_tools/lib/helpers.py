import os
from collections import OrderedDict
from pages import Index, Pattern

class Pages(object):
    def __init__(self, root):
        self._pages = OrderedDict()
        self.root = root

    def add(self, dirpath, dirnames, filenames):
        relpath = os.path.relpath(dirpath, self.root)
        if 'pattern.yml' in filenames:
            self._pages[relpath] = Pattern(dirpath, dirnames, filenames)
        elif 'index.yml' in filenames:
            self._pages[relpath] = Index(dirpath, dirnames, filenames)

    def all(self):
        return self._pages
                
