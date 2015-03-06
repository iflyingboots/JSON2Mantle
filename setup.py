from setuptools import setup, find_packages
import sys
import os

version = '0.0.1'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(name='JSON2Mantle',
      version=version,
      description='Generate Mantle models using JSON files',
      long_description=readme,
      author='Xin Wang',
      author_email='i@wangx.in',
      url='https://github.com/sutar/JSON2Mantle',
      license=license,
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
