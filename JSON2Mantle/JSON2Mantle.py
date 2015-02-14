#!/usr/bin/env python3

import json
import sys
import re
import argparse
import os

from pprint import pprint

class JSON2Mantle(object):

    def __init__(self):
        self.class_prefix = ''

    def set_class_prefix(self, prefix):
        self.class_prefix = prefix

    def _format_property(self, name, storage, nstype):
        name = name if storage == 'assign' else '*%s' % (name,)
        return '@property (nonatomic, %s) %s %s;' % (storage, nstype, name)


    def _convert_name_style(self, name):
        """Convert var_name to varName
        """
        return re.sub(r'_(\w)', lambda x: x.group(1).upper(), name)


    def generate_properties(self, dict_data, name):
        result = []
        sub_model = {}
        for key, value in dict_data.items():
            key = self._convert_name_style(key)
            t = type(value)
            if t == dict:
                sub_model = self.generate_properties(value, key)
                class_name = self.class_prefix + key[0].upper() + key[1:]
                string = self._format_property(key, 'strong', class_name)
            elif t == list:
                sub_model = self.generate_properties(value[0], key)
                string = self._format_property(key, 'strong', 'NSArray')
            elif t == str:
                string = self._format_property(key, 'copy', 'NSString')
            elif t == int:
                string = self._format_property(key, 'assign', 'NSInteger')
            elif t == bool:
                string = self._format_property(key, 'assign', 'BOOL')
            else:
                raise ValueError

            result.append(string)

        results = {name: result}
        results.update(sub_model)
        return results

def setup():
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
        print('Error: could not create directory {}'.format(args.output_dir))
        exit()

    try:
        dict_data = json.loads(open(args.json_file).read())
    except IOError as e:
        print('Error: no such file {}'.format(args.json_file))
        exit()

    return args

def main():

    args = setup()

    filename = args.json_file.split('.')[0]

    j2m = JSON2Mantle()
    j2m.set_class_prefix(args.prefix)
    name_properties = j2m.generate_properties(dict_data, filename)
    pprint(name_properties)

if __name__ == '__main__':
    main()
