#!/usr/bin/env python

from distutils.core import setup

setup(name='qtmium',
      version='0.1',
      description='Solid modelling environment',
      author='Henning Meyer',
      author_email='tutmann@gmail.com',
      url='http://hmeyer.github.com/qtmium/',
      packages=['qtmium', 'qtmium.primitives'],
      package_dir={'qtmium':'src/qtmium'}, 
     )
