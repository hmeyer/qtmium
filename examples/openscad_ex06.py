r = 10
dim = 100


def roundedBox(dim, r):
	rdim = dim - 2*r

	b = Box(rdim,rdim,dim, center=True)
	b += Box(dim,rdim,rdim, center=True)
	b += Box(rdim,dim,rdim, center=True)

	rdim2 = rdim/2.0
	for x in [-rdim2,rdim2]:
		for y in [-rdim2,rdim2]:
			for z in [-rdim2,rdim2]:
				b+= Sphere(r).translate(x,y,z)

	for x in [-rdim2,rdim2]:
		for y in [-rdim2,rdim2]:
			for ax in [X_axis, Y_axis, Z_axis]:
				b+= (
					Cylinder(r=r,h=rdim,center=True)
					.translate(x,y,0)
					.rotate(ax, 90)
				)
	return b
	
def digits():
	d = []
	dr = (dim/2.0-2*r)*0.9
	allpairs = [[
			[[0,0]],
			[[-.8,-1], [-.8,0], [-.8,1], [.8,-1], [.8,0], [.8,1]]
		],[
			[[-.6,-.6], [.6,.6]],
			[[-1,-1], [-1,1], [1,-1], [1,1], [0,0]]
		],[
			[[-1,-1], [0,0], [1,1]],
			[[-1,-1], [-1,1], [1,-1], [1,1]]
		]]
	for pair in list(enumerate( allpairs)):
		ax = [X_axis, Y_axis, Z_axis][pair[0]]
		for side in list(enumerate(pair[1])):
			shift = side[0]*2-1
			for c in side[1]:
				d.append( 
					Sphere(r)
					.translate(c[0]*dr, c[1]*dr, (dim+r)*.5*shift) 
					.rotate( ax, 90)
				)
	return Union(d)
	
result = roundedBox(dim, r) - digits()
