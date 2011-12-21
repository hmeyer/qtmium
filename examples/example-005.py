#
# Caterpillar Chain Wheel
# derived from OpenSCAD script from http://www.thingiverse.com/thing:8877
#


width=7
edge=6
radio=93.5/2
drill = 3.5

holes = []

disc = Cylinder(radius=radio, height=width)

for i in range(edge):
  holes.append(
    Cylinder(radius=radio, height=width*2)
      .translate(0, radio*2-radio/4.5, 0)
      .rotate(Z_axis, i*360/edge)
  )
  holes.append(
    Cylinder(radius=radio/3, height=width*2)
      .translate(radio/5.5, radio*1.075, 0)
      .rotate(Z_axis, i*360/edge)
  )
  holes.append(
    Cylinder(radius=radio/3, height=width*2)
      .translate(-radio/5.5, radio*1.075, 0)
      .rotate(Z_axis, i*360/edge)
  )

for i in range(4):
  holes.append(
    Cylinder(radius=drill/2, height=2*width, center=True)
      .translate(
        0.75*(radio-5)*math.cos(2*math.pi/4*i),
        0.75*(radio-5)*math.sin(2*math.pi/4*i),
        0)
    )

#star_wheel = disc - reduce(lambda x,y: x+y, holes)
star_wheel = disc
for x in holes:
	star_wheel -= x

x = Cylinder(radius=21.5/2, height=20).translate(0,0,10) + \
    Cylinder(radius=4.2, height=30, center=True)
x.translate(0,0,3)

result = star_wheel - x

