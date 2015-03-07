#!/usr/bin/env python3
"""
JSON2Mantle

Generate Mantle models using JSON files.
"""
import json
import re
import argparse
import os
import time
import json2mantle.objc_template as objc_tpl
from json2mantle.renderer import TemplateRenderer

from pprint import pprint


class JSON2Mantle(object):

    def __init__(self):
        self.class_prefix = ''
        self.class_suffix = 'Model'
        self.properties = {}
        self.meta_data = {
            'year': time.strftime('%Y', time.gmtime()),
            'created_at': time.strftime('%m/%d/%y', time.gmtime()),
            'author': 'Xin Wang',
        }
        # TODO: finish the reserved words tuple
        self.reserved_words = ('class', 'id', 'super', 'description')

    def make_class_name(self, name):
        """Generates Objective-C style class name.
        Format: PREFIX + ClassName + Suffix
        """
        assert len(name) != 0
        return self.class_prefix + name[0].upper() + name[1:] + self.class_suffix

    def _convert_name_style(self, name):
        """Converts `var_name` to `varName` style.
        Moreover, rename those with reserved words
        """
        if name in self.reserved_words:
            new_name = 'model{}{}'.format(name[0].upper(), name[1:])
            return new_name
        candidates = re.findall(r'(_\w)', name)
        if not candidates:
            return name
        new_name = re.sub(r'_(\w)', lambda x: x.group(1).upper(), name)
        return new_name

    def get_template_data(self):
        """Generates template variables by using extracted properties.
        """
        render_h = {}
        render_m = {}

        for model_name, properties in self.properties.items():
            # header: properties
            joined_properties = '\n'.join(
                map(objc_tpl.property_tpl, properties))

            # header: extra headers
            joined_headers = '\n'.join(
                filter(None.__ne__, map(objc_tpl.header_tpl, properties)))

            # implementation: aliases
            joined_aliases = '\n            '.join(
                filter(None.__ne__, map(objc_tpl.alias_tpl, properties)))

            # implementation: transformers
            joined_transformers = '\n'.join(
                filter(None.__ne__, map(objc_tpl.transformer_tpl, properties)))

            render_h[model_name] = {
                'file_name': model_name,
                'properties': joined_properties,
                'created_at': self.meta_data['created_at'],
                'author': self.meta_data['author'],
                'year': self.meta_data['year'],
                'headers': joined_headers,
            }

            render_m[model_name] = {
                'file_name': model_name,
                'property_alias': joined_aliases,
                'created_at': self.meta_data['created_at'],
                'author': self.meta_data['author'],
                'year': self.meta_data['year'],
                'transformers': joined_transformers,
            }

        return (render_h, render_m)

    def trim_class_name(self, class_name):
        """If the class name is not with prefix, add it
        """
        if not class_name.startswith(self.class_prefix):
            class_name = self.make_class_name(class_name)
        # if no prefix, the first letter should be uppercase
        if self.class_prefix == '':
            class_name = class_name[0].upper() + class_name[1:]
        return class_name

    def extract_properties(self, dict_data, class_name):
        """Extracts properties from a dictionary.
        This method is a recursive one, making nested sub-dictionary merged.
        """
        # items: current properties
        items = []
        # results: key = class_name, value = items
        results = {}
        # sub_model: sub model to be merged
        sub_model = {}

        class_name = self.trim_class_name(class_name)
        print('Generating {}'.format(class_name))

        for original_name, value in dict_data.items():
            new_name = self._convert_name_style(original_name)

            if isinstance(value, dict):
                new_class_name = self.make_class_name(new_name)
                sub_model = self.extract_properties(value, new_class_name)
                results.update(sub_model)

                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'strong',
                    'class_name': new_class_name,
                    'transform': {
                        'type': 'Dictionary',
                        'class': new_class_name,
                    },
                }
            elif isinstance(value, list):
                new_class_name = self.make_class_name(new_name)
                sub_model = self.extract_properties(value[0], new_class_name)
                results.update(sub_model)
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'strong',
                    'class_name': 'NSArray',
                    'transform': {
                        'type': 'Array',
                        'class': new_class_name,
                    }
                }
            elif isinstance(value, str):
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'copy',
                    'class_name': 'NSString',
                    'transform': None,
                }
            elif isinstance(value, int):
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'assign',
                    'class_name': 'NSInteger',
                    'transform': None,
                }
            elif isinstance(value, bool):
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'assign',
                    'class_name': 'BOOL',
                    'transform': None,
                }
            else:
                raise ValueError

            items.append(item)

        results[class_name] = items
        # reduce
        results.update(sub_model)
        return results

    def generate_properties(self, dict_data, class_name):
        """Generates properties by given JSON, supporting nested structure.
        """
        if isinstance(dict_data, list):
            class_name = input(
                '"{}" is an array, give the items a name: '.format(
                class_name))
            # dict_data = {sub_class_name: dict_data}
            dict_data = dict_data[0]
        self.properties = self.extract_properties(dict_data, class_name)
        # pprint(self.properties.keys())


def init_args():
    parser = argparse.ArgumentParser(
        description='Generate Mantle models by a given JSON file.'
    )
    parser.add_argument('json_file',
                        help='the JSON file to be parsed')
    parser.add_argument('output_dir',
                        help='output directory for generated Objective-C files')
    parser.add_argument('--prefix',
                        help='class prefix of Objective-C files')
    parser.add_argument('--author',
                        help='author info')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        try:
            os.mkdir(args.output_dir)
        except IOError:
            print('Error: could not create directory {}'.format(
                args.output_dir
            ))
            exit()

    return args


def main():
    """ Main function
    """
    args = init_args()

    try:
        dict_data = json.loads(open(args.json_file).read())
    except IOError:
        print('Error: no such file {}'.format(args.json_file))
        exit()

    j2m = JSON2Mantle()

    # Gets meta data
    j2m.class_prefix = args.prefix if args.prefix else ''
    if args.author:
        j2m.meta_data['author'] = args.author

    # Get the file base name
    file_basename = os.path.basename(args.json_file)

    # Eliminating filename extension
    class_name = file_basename.split('.')[0]

    j2m.generate_properties(dict_data, class_name)

    # .h and .m data for rendering
    render_h, render_m = j2m.get_template_data()

    template_renderer = TemplateRenderer(render_h, render_m, args.output_dir)
    template_renderer.render()

if __name__ == '__main__':
    main()
