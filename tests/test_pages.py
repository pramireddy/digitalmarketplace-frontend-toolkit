import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
test_dir = os.path.abspath(os.path.dirname(__file__))
tools_dir = os.path.join(
    test_dir,
    '..',
    'build_tools')

sys.path.append(os.path.join(tools_dir, 'lib'))

from pages import Page, Index, Pattern

env = Environment(
    loader=FileSystemLoader([
        os.path.join(test_dir, 'fixtures'),
        os.path.join(repo_root, 'docs_src', 'templates'),
        os.path.join(repo_root, 'bower_components', 'govuk_template', 'views', 'layouts')]),
    extensions=['jinja2.ext.with_'])

class TestIndexPage(object):
    def test_page_renders_correctly(self):
        index = Index(os.path.join(test_dir, 'fixtures', 'index'), [], ['index.yml'])
        assert index.get_context()['title'] == 'Digital Marketplace frontend toolkit'

        template = env.get_template('index.html')

        index.set_env(env)
        index.set_template('index.html')
        assert index.render() == template.render(index.get_context())

class TestPatternPage(object):
    def setup_method(self):

        examples = []
        template_1 = env.get_template(os.path.join('pattern', 'examples', 'example_1.html'))
        examples.append({ 'html' : template_1.render() })
        template_2 = env.get_template(os.path.join('pattern', 'examples', 'example_2.html'))
        examples.append({ 'html' : template_2.render() })

        with open(os.path.join(test_dir, 'fixtures', 'pattern', 'examples', 'example_1.html'), 'r') as file:
            examples[0]['code'] = file.read()
        with open(os.path.join(test_dir, 'fixtures', 'pattern', 'examples', 'example_2.html'), 'r') as file:
            examples[1]['code'] = file.read()

        self.examples = examples
        Page.docs_root = os.path.join(test_dir, 'fixtures')
        self.pattern = Pattern(os.path.join(test_dir, 'fixtures', 'pattern'), ['examples'], ['pattern.yml'])
        self.pattern.set_env(env)

    def test_page_has_examples(self):
        assert self.pattern.get_examples() == self.examples

    def test_pages_renders_correctly(self):
        page_template = env.get_template('pattern.html')
        context = { 'asset_path' : 'assets/' }
        with open(os.path.join(test_dir, 'fixtures', 'pattern', 'pattern.yml'), 'r') as file:
            context.update(yaml.load(file))
        context['examples'] = self.examples
        
        assert self.pattern.render() == page_template.render(context)
