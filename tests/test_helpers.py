import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
test_dir = os.path.abspath(os.path.dirname(__file__))
tools_dir = os.path.join(
    test_dir,
    '..',
    'build_tools')

sys.path.append(os.path.join(tools_dir, 'lib'))

from pages import Page, Index, Pattern
from helpers import Pages

class TestPages(object):
    def setup_method(self):
        fixtures_dir = os.path.join(test_dir, 'fixtures')
        self.pages = Pages(fixtures_dir)
        for dirpath, dirnames, filenames in os.walk(fixtures_dir):
            self.pages.add(dirpath, dirnames, filenames)
        self.all_pages = self.pages.all()

    def test_pages_stored_are_correct(self):
        assert len(self.all_pages.items()) == 2
        assert 'pattern' in self.all_pages
        assert 'index' in self.all_pages

    def test_pages_are_the_right_classes(self):
        assert isinstance(self.all_pages['pattern'], Pattern)
        assert isinstance(self.all_pages['index'], Index)

