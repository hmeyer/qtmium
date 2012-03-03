# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.solid import Solid

class Cylinder(Solid):
  
  def __init__(self, r=None, radius=None, r1=None, r2=None, diameter=None, d=None, d1=None, d2=None, height=None, 
    h=None, pie=360, center=False):
    if diameter: d = diameter
    if d: r = d *0.5
    if d1: r1 = d1*0.5
    if d2: r2 = d2*0.5
    if radius: r=radius
    if height: h=height
    if r1 != r2:
      self.instance = BRepPrimAPI_MakeCone(r1, r2, h, pie*math.pi/180)
      Solid.__init__(self, self.instance.Shape(), center=center)
    else:
      if not r: r = r1 = r2
      self.instance = BRepPrimAPI_MakeCylinder(r, h, pie*math.pi/180)
      Solid.__init__(self, self.instance.Shape(), center=center)

