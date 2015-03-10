"""
JSON2Mantle

Objective-C templates
"""

import re

def header_tpl(data):
    """Generates header file to import
    Output:
        #import "XYZUserInfo.h"
    """
    if not data['transform']:
        return None
    if data['class_name'] == 'NSArray':
        name = data['transform']['class']
    else:
        name = data['class_name']
    return '#import "{}.h"'.format(name)


def property_tpl(data):
    """Generates variable data, according to name, type, storage.
    Output:
        @property (nonatomic, copy) NSString *testString;
    """
    name = data['name'] if data[
        'storage'] == 'assign' else '*{}'.format(data['name'])
    return '@property (nonatomic, {}) {} {};'.format(data['storage'], data['class_name'], name)


def alias_tpl(data):
    """Generates Mantle alias
    Output:
        @"postTime": @"post_time",
    """
    if data['name'] == data['original_name']:
        return None
    name = data['original_name']
    candidates = re.findall(r'(_\w)', name)
    if not candidates:
        new_name = data['name']
    else:
        new_name = re.sub(r'_(\w)', lambda x: x.group(1).upper(), name)
    return '@"{}": @"{}",'.format(new_name, name)


def transformer_tpl(data):
    """Generates Mantle transformer
    Output:

    + (NSValueTransformer *)articleJSONTransformer
    {
        return [NSValueTransformer
            mtl_JSONArrayTransformerWithModelClass:XYZArticleModel.class];
    }

    """
    if not data['transform']:
        return None
    string = "+ (NSValueTransformer *){}JSONTransformer\n{{\n    " \
    "return [NSValueTransformer mtl_JSON{}TransformerWithModelClass:{}.class]" \
    ";\n}}\n".format(
        data['name'], data['transform']['type'], data['transform']['class'])
    return string
