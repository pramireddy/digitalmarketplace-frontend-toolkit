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


class DocsBuilder(object):
    def __init__(self, src_root):
        self.src_root = src_root
        self.pages = Pages(src_root)
        self._add_pages()

    def _add_pages(self):
        for dirpath, dirnames, filenames in os.walk(self.src_root):
            self.pages.add(dirpath, dirnames, filenames)

    def log(self, message):
        print(message)

    def build(self, dst_root):
        for path, page in self.pages.all().items():
            abspath = os.path.abspath(os.path.join(dst_root, path))
            if not os.path.exists(abspath):
                os.mkdir(abspath)

            filepath = os.path.join(abspath, 'index.html')
            with open(filepath, 'w') as file:
                file.write(page.render())
                self.log('{} created'.format(filepath))
