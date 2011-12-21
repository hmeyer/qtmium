
ring = (
  Cylinder(radius=6, height=2, center=True) - \
  Cylinder(radius=4, height=2, center=True)).rotate(Y_axis, 90)

gear = ring
spike = Box(1,1,5, center = True).translate(0,0,5*math.sqrt(2))

for a in range(8):
	gear +=  spike.rotate(X_axis, a * 45)
  
result = gear
