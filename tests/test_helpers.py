import os
import sys
import shutil
import tempfile

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
test_dir = os.path.abspath(os.path.dirname(__file__))
tools_dir = os.path.join(
    test_dir,
    '..',
    'build_tools')

sys.path.append(os.path.join(tools_dir, 'lib'))

from pages import Page, Index, Pattern
from helpers import Pages, DocsBuilder

class TestPages(object):
    def setup_method(self):
        fixtures_dir = os.path.join(test_dir, 'fixtures')

        Page.docs_root = os.path.join(test_dir, 'fixtures')
        Page.templates_root = os.path.join(repo_root, 'docs_src', 'templates')

        self.pages = Pages(fixtures_dir)
        for dirpath, dirnames, filenames in os.walk(fixtures_dir):
            self.pages.add(dirpath, dirnames, filenames)
        self.all_pages = self.pages.all()

    def test_pages_stored_are_correct(self):
        assert len(self.all_pages.items()) == 3
        assert 'pattern' in self.all_pages
        assert 'index' in self.all_pages
        assert 'index/pattern_2' in self.all_pages

    def test_pages_are_the_right_classes(self):
        assert isinstance(self.all_pages['pattern'], Pattern)
        assert isinstance(self.all_pages['index'], Index)
        assert isinstance(self.all_pages['index/pattern_2'], Pattern)

    def test_breadcrumb_is_correct_for_depth_of_one(self):
        breadcrumb = self.pages.breadcrumb('pattern')

        assert breadcrumb == [{
            'title' : 'Save and continue button',
            'href' : 'pattern'
        }]

    def test_breadcrumb_is_correct_for_depth_of_two(self):
        breadcrumb = self.pages.breadcrumb('index/pattern_2')

        assert breadcrumb == [
            {
                'title' : 'Digital Marketplace frontend toolkit',
                'href' : 'index'
            },
            {
                'title' : 'Save and continue secondary action button',
                'href' : 'index/pattern_2'
            }
        ]

    def test_breadcrumb_is_correct_with_base_url_specified(self):
        breadcrumb = self.pages.breadcrumb('index/pattern_2', prefix='https://user.github.com/patterns/')

        assert breadcrumb == [
            {
                'title' : 'Digital Marketplace frontend toolkit',
                'href' : 'https://user.github.com/patterns/index'
            },
            {
                'title' : 'Save and continue secondary action button',
                'href' : 'https://user.github.com/patterns/index/pattern_2'
            }
        ]


class TestDocsBuilder(object):
    def setup_method(self):
        self.builder = DocsBuilder(os.path.join(test_dir, 'fixtures'))
        self.temp_dir = tempfile.mkdtemp()
        self.builder.build(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir)

    def test_all_pages_are_built(self):
        assert os.path.exists(os.path.join(self.temp_dir, 'index', 'index.html'))
        assert os.path.exists(os.path.join(self.temp_dir, 'pattern', 'index.html'))
        assert os.path.exists(os.path.join(self.temp_dir, 'index', 'pattern_2', 'index.html'))

