def roundedBox(x,y=None,z=None, r=3):
	if not y: y = x
	if not z: z = (x+y)*.5
	rx = x - 2*r
	ry = y - 2*r
	rz = z - 2*r

	b = Box(rx,ry,z, center=True)
	b += Box(x,ry,rz, center=True)
	b += Box(rx,y,rz, center=True)

	for x in [-rx*.5,rx*.5]:
		for y in [-ry*.5,ry*.5]:
			for z in [-rz*.5,rz*.5]:
				b+= Sphere(r).translate(x,y,z)
	for x in [-.5,.5]:
		for y in [-.5,.5]:
			for v in [[rx, rz, ry, X_axis],
				[rz, ry, rx, Y_axis],
				[ry, rx, rz, Z_axis]]:
				b+= (
					Cylinder(r=r,h=v[2],center=True)
					.translate(v[0]*x,v[1]*y,0)
					.rotate(v[3], 90)
				)
	return b
	
result = roundedBox( 10,20,30, r=3)