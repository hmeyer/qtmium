#!/usr/bin/env python

from distutils.core import setup
import glob

import os

for i in os.listdir('ui'):
	(b,e) = os.path.splitext(i)
	if (e == '.ui'):
		o = os.path.join('ui',i)
		n = os.path.join('ui','Ui_'+b+'.py')
		os.system('pyuic4 -o ' + n + ' ' + o)

setup(name='qtmium',
      version='0.1',
      description='Solid modelling environment',
      author='Henning Meyer',
      author_email='tutmann@gmail.com',
      url='http://hmeyer.github.com/qtmium/',
      packages=['qtmium', 'qtmium.ui','qtmium.cadmium','qtmium.cadmium.primitives'],
      scripts= ["src/qtmium"],
      data_files= [("share/qtmium", glob.glob("examples/*"))],
      license="AGPLv3",
      long_description="""qtmium is a tool,
inspired by OpenSCAD built on top of PythonOCC and OCE,
to give simple programming interface to create solid models."""
        )
