def r_from_dia(d):
	return d / 2.0

def rotcy(rot, r, h): 
	return Cylinder(radius = r, height = h, center = True).rotate(rot, 90)


size = 50
hole = 25
	
cy_r = r_from_dia(hole)
cy_h = r_from_dia(size * 2.5)


result = (Sphere(r_from_dia(size)) - 
		rotcy(X_axis, cy_r, cy_h) -
		rotcy(Y_axis, cy_r, cy_h) -
		rotcy(Z_axis, cy_r, cy_h) )
