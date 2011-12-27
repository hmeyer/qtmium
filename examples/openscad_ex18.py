def thing(type):
	type = type % 4
	if type == 0:
		return Sphere(30)
	elif type == 1:
		return Box(60, center = True)
	elif type == 2:
		return Cylinder(h=50, r=30, center=True)
	else: 
		o = [ Box(45, center = True) ]
		for i in range(3):
			o.append( Box(50, center=True).rotate([X_axis, Y_axis, Z_axis][i], 45) )
		return Union( o )

result = Union(
	[thing(1+x+y).translate(x*100-150,y*100-150,0)
		for x in range(4) for y in range(4)]
	)
