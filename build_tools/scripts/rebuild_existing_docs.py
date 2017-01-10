import os
import yaml
import pprint

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
existing_docs = os.path.join(repo_root, 'pages_builder', 'pages')
pp = pprint.PrettyPrinter(indent=2)
props_to_ignore = ['assetPath']
prop_mapping = {
    'pageTitle' : 'title',
    'pageDescription': 'description',
    'grid': 'grid'
}

def get_data_from_file(path):
    data = {}
    with open(path, 'r') as file:
        contents = yaml.load(file.read())
    return contents


def render_examples_as_files(data, newpath):
    # write file for each example
        examples_dir = os.path.join(newpath, 'examples')
        if not os.path.exists(examples_dir):
            os.mkdir(examples_dir)
        
        for idx, example in enumerate(data['examples']):
            with open(os.path.join(examples_dir, 'example_{}.html'.format(idx + 1)), 'w') as file:
                file.write(pp.pformat(example))

def organise_data(data):
    for prop_to_ignore in props_to_ignore:
        if prop_to_ignore in data.keys():
            del data[prop_to_ignore]

    for prop_key in prop_mapping.keys():
        if prop_key in data.keys():
            data[prop_mapping[prop_key]] = data[prop_key]
            del data[prop_key]
    return data

if __name__ == '__main__':
    for dirpath, dirnames, filenames in os.walk(existing_docs):
        newpath = dirpath.replace(existing_docs, os.path.join(repo_root, 'docs_src', 'docs'))
        if newpath != existing_docs:
            if not os.path.exists(newpath):
                os.mkdir(newpath)
                print('{} created'.format(newpath))

            if len(filenames) > 0:
                for file in filenames:
                    if file == 'README.md':
                        continue
                    pattern_dir_path = os.path.join(newpath, file.replace('.yml', ''))
                    if not os.path.exists(pattern_dir_path):
                        print('creating new pattern at {}'.format(pattern_dir_path))
                        os.mkdir(pattern_dir_path)
                    data = get_data_from_file(os.path.join(dirpath, file))
                    if 'examples' in data:
                        print('Rendering {} example files for {}'.format(len(data['examples']), pattern_dir_path))
                        render_examples_as_files(data, pattern_dir_path)
                        del data['examples']

                    data = organise_data(data)
                    # write the rest to a pattern.yml file
                    with open(os.path.join(pattern_dir_path, 'pattern.yml'), 'w') as file:
                        print('Creating a pattern.yml file for {}'.format(pattern_dir_path))
                        file.write(yaml.dump(data, default_flow_style=False))
                        
