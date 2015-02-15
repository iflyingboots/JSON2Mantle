#!/usr/bin/env python3

import json
import sys
import re
import argparse
import os
import time
from renderer import TemplateRenderer

from pprint import pprint


class JSON2Mantle(object):

    def __init__(self):
        self.class_prefix = ''
        self.class_suffix = 'Model'
        self.current_class = None
        self.properties = {
            'h': {},
            'm': {},
        }
        self.meta_data = {
            'year': time.strftime('%Y', time.gmtime()),
            'created_at': time.strftime('%m/%d/%y', time.gmtime()),
            'author': 'Xin Wang',
        }

    def make_class_name(self, name):
        """Generates Objective-C style class name.
        Format: PREFIX + ClassName + Suffix
        """
        assert len(name) != 0
        return self.class_prefix + name[0].upper() + name[1:] + self.class_suffix

    def _format_property(self, name, storage, nstype):
        """Generates proper variable name, according to types.
        """
        name = name if storage == 'assign' else '*%s' % (name,)
        return '@property (nonatomic, %s) %s %s;' % (storage, nstype, name)

    def _convert_name_style(self, name):
        """Converts `var_name` to `varName` style.
        """
        candidates = re.findall(r'(_\w)', name)
        if not candidates:
            return name
        new_name = re.sub(r'_(\w)', lambda x: x.group(1).upper(), name)
        self.set_alias_property(name, new_name)
        return new_name

    def set_alias_property(self, name, new_name):
        self.properties['m'].setdefault(self.current_class, {})
        self.properties['m'][self.current_class][new_name] = name

    def get_template_data(self):
        """Generates template variables by using extracted properties.
        """
        render_h = {}
        render_m = {}

        # header file
        for model_name, properties in self.properties['h'].items():

            joined_properties = '\n'.join(properties)

            render_h[model_name] = {
                'file_name': model_name,
                'properties': joined_properties,
                'created_at': self.meta_data['created_at'],
                'author': self.meta_data['author'],
                'year': self.meta_data['year'],
            }

        # implementation file
        for model_name, properties in self.properties['m'].items():

            # output: @"postTime": @"post_time",
            joined_properties = '\n            '.join(
                map(lambda x: '@"{}": @"{}",'.format(x[0], x[1]),
                    properties.items())
            )

            render_m[model_name] = {
                'file_name': model_name,
                'property_alias': joined_properties,
                'created_at': self.meta_data['created_at'],
                'author': self.meta_data['author'],
                'year': self.meta_data['year'],
            }

        return (render_h, render_m)

    def extract_properties(self, dict_data, class_name):
        result = []
        sub_model = {}
        self.current_class = class_name
        for name, value in dict_data.items():
            name = self._convert_name_style(name)
            if isinstance(value, dict):
                new_class_name = self.make_class_name(name)
                sub_model = self.extract_properties(value, new_class_name)
                string = self._format_property(name, 'strong', new_class_name)
            elif isinstance(value, list):
                new_class_name = self.make_class_name(name)
                sub_model = self.extract_properties(
                    value[0], new_class_name)
                string = self._format_property(name, 'strong', 'NSArray')
            elif isinstance(value, str):
                string = self._format_property(name, 'copy', 'NSString')
            elif isinstance(value, int):
                string = self._format_property(name, 'assign', 'NSInteger')
            elif isinstance(value, bool):
                string = self._format_property(name, 'assign', 'BOOL')
            else:
                raise ValueError

            result.append(string)

        results = {class_name: result}
        results.update(sub_model)
        return results

    def generate_properties(self, dict_data, class_name):
        """Generates properties by given JSON, supporting nested structure.
        """
        self.properties['h'] = self.extract_properties(dict_data, class_name)



def main():

    parser = argparse.ArgumentParser(
        description='Generate Mantle models by a given JSON file.')
    parser.add_argument('json_file', help='the JSON file to be parsed')
    parser.add_argument(
        'output_dir', help='output directory for generated Objective-C files')
    parser.add_argument('--prefix', help='class prefix of Objective-C files')
    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        try:
            os.mkdir(args.output_dir)
        except IOError:
            print(
                'Error: could not create directory {}'.format(args.output_dir))
            exit()

    try:
        dict_data = json.loads(open(args.json_file).read())
    except IOError as e:
        print('Error: no such file {}'.format(args.json_file))
        exit()

    j2m = JSON2Mantle()

    j2m.class_prefix = args.prefix if args.prefix else ''

    file_basename = os.path.basename(args.json_file)
    class_name = j2m.make_class_name(file_basename.split('.')[0])
    j2m.generate_properties(dict_data, class_name)

    render_h, render_m = j2m.get_template_data()

    template_renderer = TemplateRenderer(render_h, render_m, args.output_dir)
    template_renderer.render()

if __name__ == '__main__':
    main()
