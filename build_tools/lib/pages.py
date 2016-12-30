import os
import yaml
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


class Pattern(Page):
    _template = None

    def __init__(self, dirpath, dirnames, filenames):
        super(Pattern, self).__init__(dirpath, dirnames, filenames)
        self._template = self._env.get_template('_pattern.html')

    def get_examples(self):
        examples = []
        examples_dir = os.path.join(self.dirpath, 'examples')

        for filename in os.listdir(examples_dir):
            example = {}
            entry = os.path.join(examples_dir, filename)
            if os.path.isfile(entry):
                with open(entry, 'r') as file:
                    example['code'] = file.read()

                template = self._env.get_template(os.path.relpath(entry, self.docs_root))
                example['html'] = template.render()
                examples.append(example)

        return examples

    def get_meta(self):
        pattern_meta = os.path.join(self.dirpath, 'pattern.yml')

        with open(pattern_meta, 'r') as file:
            meta = yaml.load(file.read())

        return meta

    def get_context(self):
        context = self.get_meta()
        context['examples'] = self.get_examples()
        return context
