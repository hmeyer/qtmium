#
# Parametric bushing
# derived from OpenSCAD script from http://www.thingiverse.com/thing:8697
# 
# There are two methods generate_compact and generate_verbose, both 
# create exactly identical solids, but they represent different styles
# of python programming. 
# generate_compact demonstrates functional programming style
# generate_verbose demostrates more traditional procedural programming style
# that is easier to read
#

def generate_compact(height, radius, hole_r, border, recess, num_support):
	a = (
		(
			Cylinder(r=radius+border, h=1) +
			Cylinder(h=2, r1=radius+border, r2=radius).translate(0,0,1) +
			Cylinder(h=height-6, r=radius).translate(0,0,3) +
			Cylinder(h=3, r1=radius, r2=radius-border).translate(0,0,height-3)
		) -
		Cylinder(r=radius-(border*2), h=height+border).translate(0,0,-1)
	)
	
	b = Cylinder(r=hole_r+border*2, h=height) 
	for i in range(num_support):
		b += (Box((radius-border)*2-0.6, border*2, height)
				.translate(-radius+border+0.4,-border,0)
				.rotate(Z_axis,i*180/num_support))
		

	c= (
		Cylinder(r=hole_r,h=height+2) + 
		Cylinder(r=radius-2*border, h=recess)
	).translate(0,0,-1)

	return ( a+ b - c)

def generate_verbose(height, radius, hole_r, border, recess, num_support):
  outer_rings = (
    Cylinder(r=radius+border, h=1) +
    Cylinder(h=2, r1=radius+border, r2=radius).translate(0,0,1) +
    Cylinder(h=height-6, r=radius).translate(0,0,3) +
    Cylinder(h=3, r1=radius, r2=radius-border).translate(0,0,height-3)
  ) - Cylinder(r=radius-(border*2), h=height+border).translate(0,0,-1)

  shafts = []
  for i in range(num_support):
    b = Box((radius-border)*2-0.6, border*2, height) \
          .translate(-radius+border+0.4,-border,0) \
          .rotate(Z_axis,i*180/num_support)
    shafts.append( b )
  central_ring = Cylinder(r=hole_r+border*2, h=height)

  central_hole = Cylinder(r=hole_r,h=height+2)
  recess = Cylinder(r=radius-2*border, h=recess)

  return (outer_rings + Union(shafts) + central_ring) - \
    (central_hole + recess).translate(0,0,-1)

bushing = generate_compact(16, 75.0/2, 4.5, 1.56,5,3)

result = bushing
