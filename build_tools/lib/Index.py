import os
import yaml

from Page import Page

class Index(Page):
    def __init__(self, dirpath, dirnames, filenames):
        super(Index, self).__init__(dirpath, dirnames, filenames)
        self._template = self._env.get_template('_index.html')

    def get_meta(self):
        index_meta = os.path.join(self.dirpath, 'index.yml')

        with open(index_meta, 'r') as file:
            meta = yaml.load(file.read())

        return meta

    def get_context(self):
        return self.get_meta()
