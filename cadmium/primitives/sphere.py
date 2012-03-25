# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.solid import Solid

class Sphere(Solid):
  
  def __init__(self, r=None, radius=None, d=None, diameter=None, phi=360, center=False):

    if radius: r = radius
    if d: r = d/2.0
    if diameter: r = diameter/2.0
    self.instance = BRepPrimAPI_MakeSphere(r, phi*math.pi/180)
    Solid.__init__(self, self.instance.Shape(), center=center)
