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

    def breadcrumb(self, path, prefix=''):
        breadcrumb = []
        hierarchy = path.split('/')

        for idx, step in enumerate(hierarchy):
            current_steps = hierarchy[0:(idx + 1)]
            current_path = os.path.join(*current_steps)
            page = self._pages[current_path]
            breadcrumb.append({
                'title' : page.get_context()['title'],
                'href' : '{}{}'.format(prefix, current_path)
            })

        return breadcrumb
            
