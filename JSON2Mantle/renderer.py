#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os

class TemplateRenderer(object):

    def __init__(self, properties_h, properties_m, output_dir='output'):
        basepath = os.path.dirname(__file__)
        h_file = os.path.abspath(os.path.join(basepath, 'templates', 'model.h'))
        m_file = os.path.abspath(os.path.join(basepath, 'templates', 'model.m'))
        self.properties = {
            'h': properties_h,
            'm': properties_m,
        }
        self.templates = {
            'h': open(h_file).read(),
            'm': open(m_file).read(),
        }
        self.output_dir = output_dir

    def render(self):
        for model in ('h', 'm'):
            for class_name, prop in self.properties[model].items():
                output_file = '%s/%s.%s' % (self.output_dir, class_name, model)
                output_doc = self.templates[model]

                for name, value in prop.items():
                    placeholder = '{{%s}}' % (name,)
                    output_doc = output_doc.replace(placeholder, value)

                # clean up
                output_doc = re.sub(r'{{.*?}}', '', output_doc)

                with open(output_file, 'w') as fp:
                    fp.write(output_doc)


def main():
    pass

if __name__ == '__main__':
    main()
