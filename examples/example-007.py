result = Cylinder(radius=1, height=8, center=True).translate(x=4) + \
  Cylinder(radius=1, height=8, center=True).translate(x=-4)\
    .scale(0.5) + \
  Box(2,2,2, center=True)

