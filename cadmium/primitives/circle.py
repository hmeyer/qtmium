import math
from OCC.Geom2d import Geom2d_Circle
from OCC.gp import gp_OX2d
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge2d

from cadmium.solid import Solid

class Circle(Solid):

  def __init__(self, r=None, radius=None, phi=360, center=False):

    if radius: r = radius
    C = Geom2d_Circle( gp_OX2d(), r )
    self.instance = BRepBuilderAPI_MakeEdge2d(C.Circ2d())
#    self.instance = BRepPrimAPI_MakeSphere(r, phi*math.pi/180)
    Solid.__init__(self, self.instance.Shape(), center=center)

