import os
import yaml

from Page import Page

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
