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
			for i in range(3):
				v = [rx, rz, ry]
				ax = [X_axis, Y_axis, Z_axis][i]
				b+= (
					Cylinder(r=r,h=v[(i+2)%3],center=True)
					.translate(v[i]*x,v[(i+1)%3]*y,0)
					.rotate(ax, 90)
				)
	return b
	
result = roundedBox( 10,20,30, r=3)