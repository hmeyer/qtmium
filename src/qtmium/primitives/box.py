# 
# qtmium - Python library for Solid Modelling
#

from OCC.BRepPrimAPI import *

from qtmium.solid import Solid

class Box(Solid):
  
  def __init__(self, x=10, y=10, z=10, center=False):
    self.instance = BRepPrimAPI_MakeBox(x,y,z)
    Solid.__init__(self, self.instance.Shape(), center=center)
    
