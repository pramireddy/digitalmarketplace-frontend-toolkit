import os
import sys
import shutil

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
docs_data_dir = os.path.join(repo_root, 'docs_src', 'docs')
docs_dir = os.path.join(repo_root, 'docs')

sys.path.append(os.path.join('build_tools', 'lib'))

from helpers import DocsBuilder

if __name__ == '__main__':
    shutil.rmtree(docs_dir)
    os.mkdir(docs_dir)
    builder = DocsBuilder(docs_data_dir)
    builder.build(os.path.join(repo_root, 'docs'))
