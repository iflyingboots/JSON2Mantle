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
    result = '#import "{}.h"'.format(name)
    return result


def property_tpl(data):
    """Generates variable data, according to name, type, storage.
    Output:
        @property (nonatomic, copy) NSString *testString;
    """
    name = data['name'] if data[
        'storage'] == 'assign' else '*{}'.format(data['name'])
    result = '@property (nonatomic, {}) {} {};'.format(
        data['storage'],
        data['class_name'],
        name)
    return result


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

    /**
     * Converts '{}' property from '{}' class type.
     *
     * @return NSValueTransformer
     */
    + (NSValueTransformer *)articleJSONTransformer
    {
        return [NSValueTransformer
            mtl_JSONArrayTransformerWithModelClass:XYZArticleModel.class];
    }

    """
    if not data['transform']:
        return None
    string = """
/**
 * Converts '{property}' property from '{class_name}' class.
 *
 * @return NSValueTransformer
 */
+ (NSValueTransformer *){property}JSONTransformer
{{
    return [NSValueTransformer mtl_JSON{type}TransformerWithModelClass:{class_name}.class];
}}""".format(
        property=data['name'],
        type=data['transform']['type'],
        class_name=data['transform']['class'],
    )
    return string
