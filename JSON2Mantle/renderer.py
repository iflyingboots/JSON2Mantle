"""
JSON2Mantle

Renderer
"""
import re
import os

class TemplateRenderer(object):
    """Template Renderer
    """

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
        """Renders template file with given data
        """
        for model in ('h', 'm'):
            for class_name, prop in self.properties[model].items():
                filename = '{}.{}'.format(class_name, model)
                output_file = os.path.join(self.output_dir, filename)
                output_doc = self.templates[model]

                for name, value in prop.items():
                    placeholder = '{{%s}}' % (name,)
                    output_doc = output_doc.replace(placeholder, value)

                # clean up
                output_doc = re.sub(r'{{.*?}}', '', output_doc)

                with open(output_file, 'w') as output:
                    output.write(output_doc)
