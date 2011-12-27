# 
# qtmium - Python environment for Solid Modelling
#

from cadmium.solid import Solid

class Union(Solid):
    def __init__(self, shapelist):
        t = shapelist[0]
        for x in shapelist[1:]:
            t += x
        Solid.__init__(self, t.shape)
