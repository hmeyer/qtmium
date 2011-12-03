# 
# qtmium - Python library for Solid Modelling
#

import math
from OCC.BRepPrimAPI import *

from qtmium.solid import Solid

class Sphere(Solid):
  
  def __init__(self, r=None, radius=None, phi=360, center=False):

    if radius: r = radius
    self.instance = BRepPrimAPI_MakeSphere(r, phi*math.pi/180)
    Solid.__init__(self, self.instance.Shape(), center=center)
