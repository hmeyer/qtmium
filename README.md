qtmium is a Python programming environment for Solid Modelling

qtmium is based on Cadmium (Jayesh Salvi @jyro) and inspired by OpenSCAD (http://www.openscad.org/). It allows you to write python code to create primitive objects (Box, Cylinder, Sphere, etc.) and apply CSG operations (Addition, Subtraction, Intersection) on them to create advanced solid models. The primitives have support for affine transformations too (translation, rotation).

Screenshots and examples
------------------------
[http://hmeyer.github.com/qtmium/](http://hmeyer.github.com/qtmium/).

Typical Solid modelling code with qtmium
------------------------------------------
    box = Box(x=4, y=4, z=4).rotate(Z_axis, 30)
    cyl = Cylinder(radius=2, height=4).translate(-1,0,0)

    result = box + cyl

Getting qtmium
---------------------------

The easiest way to setup PythonOCC and OCE is to do it in Ubuntu (or Ubuntu VM). 
To install qtmium just do `sudo apt-add-repository ppa:hmeyer/3d;sudo apt-get update;sudo apt-get install qtmium`.

Installing from Github:

First grab the sources.
Install dependencies:

You will need Python Open Cascade - http://www.pythonocc.org/

sudo apt-get install python-qt4 pyqt4-dev-tools python-qscintilla2 python-argparse


There seems to be a bug that will produce an error message when you start qtmium the first time. 
Please run:
python setup.py install 

It will give you errors, ignore those; you can just start qtmium.py now.



Details
--------------------------
qtmium is inspired by the [OpenSCAD project](http://www.openscad.org/) and relying heavily on [Cadmium](http://http://jayesh3.github.com/cadmium/).

qtmium is a work in progress. Bug reports and patches are welcome.

