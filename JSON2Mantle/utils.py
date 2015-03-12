"""
JSON2Mantle

Utilities
"""

from __future__ import unicode_literals

import os
import pwd

mock_user_name = None

# only works with Python 2 on OS X
try:
    import objc
    import AddressBook as ab
except ImportError:
    print('Could not import OS X Address Book, using "uid" instead')
    try:
        mock_user_name = pwd.getpwuid(os.getuid())[0]
    except:
        mock_user_name = ''


# Note: following is adapted from https://gist.github.com/pklaus/1029870


def pythonize(objc_obj):
    if isinstance(objc_obj, objc.pyobjc_unicode):
        return unicode(objc_obj)
    elif isinstance(objc_obj, ab.NSDate):
        return objc_obj.description()
    elif isinstance(objc_obj, ab.NSCFDictionary):
        # implicitly assuming keys are strings...
        return {k.lower(): pythonize(objc_obj[k])
                for k in objc_obj.keys()}
    elif isinstance(objc_obj, ab.ABMultiValueCoreDataWrapper):
        return [pythonize(objc_obj.valueAtIndex_(index))
                for index in range(0, objc_obj.count())]


def ab_person_to_dict(person, skip=None):
    _default_skip_properties = frozenset(("com.apple.ABPersonMeProperty",
                                          "com.apple.ABImageData"))
    skip = _default_skip_properties if skip is None else frozenset(skip)
    props = person.allProperties()
    return {prop.lower(): pythonize(person.valueForProperty_(prop))
            for prop in props if prop not in skip}


def get_current_user_name():
    """Gets the current user's name from Address Book
    """
    # if fails to import AddressBook, returns empty name
    if mock_user_name:
        return mock_user_name
    address_book = ab.ABAddressBook.sharedAddressBook()
    try:
        me_unique = address_book.meUniqueId()
    except:
        me_unique = None
    people = address_book.people()
    all_contacts = [ab_person_to_dict(person) for person in people]

    user_name = ''
    for c in all_contacts:
        if c['uid'] == me_unique:
            try:
                user_name = '{} {}'.format(
                    c['firstphonetic'], c['lastphonetic'])
            except:
                user_name = ''

    return user_name
