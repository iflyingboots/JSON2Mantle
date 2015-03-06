import re
"""
Objective-C templates
"""


def header(data):
    """Generates header file to import
    Output:
        #import "XYZUserInfo.h"
    """
    if not data['transform']:
        return None
    return '#import "{}.h"'.format(data['class_name'])


def property(data):
    """Generates variable data, according to name, type, storage.
    Output:
        @property (nonatomic, copy) NSString *testString;
    """
    name = data['name'] if data[
        'storage'] == 'assign' else '*{}'.format(data['name'])
    return '@property (nonatomic, {}) {} {};'.format(data['storage'], data['class_name'], name)


def alias(data):
    """Generates Mantle alias
    Output:
        @"postTime": @"post_time",
    """
    if data['name'] == data['original_name']:
        return None
    name = data['name']
    candidates = re.findall(r'(_\w)', name)
    if not candidates:
        return None
    new_name = re.sub(r'_(\w)', lambda x: x.group(1).upper(), name)
    return '@"{}": @"{}",'.format(new_name, name)


def transformer(data):
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
    string = "+ (NSValueTransformer *){}JSONTransformer\n{{\n    return [NSValueTransformer mtl_JSON{}TransformerWithModelClass:{}.class];\n}}\n".format(
        data['name'], data['transform']['type'], data['transform']['class'])
    return string
