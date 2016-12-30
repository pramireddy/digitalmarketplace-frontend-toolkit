"""Create page.

Usage:
    create_page.py <path> <type>

Options:
    -h --help:  Show this screen

"""

import os
import shutil
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)

    path = arguments['<path>']
    type = arguments['<type>']

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    docs_dir = os.path.join(repo_root, 'docs_src', 'docs')
    samples_dir = os.path.join(repo_root, 'build_tools', 'samples')

    # Force lowercase file names with hyphen separators
    relpath = os.path.relpath(path, docs_dir)
    relpath = relpath.lower().replace(' ', '-').replace('_', '-')
    path = os.path.abspath(os.path.join(docs_dir, relpath))

    sample_files = os.listdir(samples_dir)
    samples = { sample_file.split('.')[0] : sample_file for sample_file in sample_files } 
    if type not in samples:
        raise NameError('{} is not a valid type'.format(type))

    # Check for existing pages with that name
    path = os.path.abspath(path)
    if os.path.exists(path):
        existing_meta = os.path.join(path, samples[type])
        if len(os.listdir(path)):
            raise IOError('{} already exists and already has files in it'.format(path))

    else:
        os.mkdir(path)

    # Create necessary data for page
    shutil.copyfile(os.path.join(samples_dir, samples[type]), os.path.join(path, samples[type]))
    print('{} created'.format(path))

    if type == 'pattern':
        examples_dir = os.path.join(path, 'examples')
        os.mkdir(examples_dir)
        print('{} created'.format(examples_dir))
