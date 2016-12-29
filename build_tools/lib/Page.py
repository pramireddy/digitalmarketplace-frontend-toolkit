import os
from jinja2 import Environment, FileSystemLoader

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class Page(object):
    docs_root = os.path.join(repo_root, 'docs_src', 'docs') 
    templates_root = os.path.join(repo_root, 'docs_src', 'templates')

    def __init__(self, dirpath, dirnames, filenames):
        self._env = Environment(
            loader=FileSystemLoader([
                self.templates_root,
                self.docs_root
            ]),
            extensions=['jinja2.ext.with_']
        )
        self.dirpath = dirpath
        self.dirnames = dirnames
        self.filenames = filenames

    def set_env(self, env):
        self._env = env

    def set_template(self, template):
        self._template = self._env.get_template(template)

    def render(self):
        return self._template.render(self.get_context())
