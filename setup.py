from setuptools import setup, find_packages
import sys
import os

version = '0.0.8'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    readme = f.read()


setup(
    name='JSON2Mantle',
    version=version,
    description='Generate Mantle models using JSON files',
    long_description=readme,
    author='Xin Wang',
    author_email='i@wangx.in',
    url='https://github.com/sutar/JSON2Mantle',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Objective C',
        'Topic :: Text Processing',
    ],
    keywords='mantle parser objective-c',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      # -*- Extra requirements: -*-
    ],
    entry_points={
      "console_scripts": [
          "json2mantle = json2mantle.cli:main",
      ]
    },
)
