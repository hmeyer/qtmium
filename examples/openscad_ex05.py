
result = (
	Cylinder(h = 50, r = 100) -
	Cylinder(h = 50, r = 80).translate(0, 0, 10) -
	Box(50, center = True).translate(100, 0, 35)
	)

for i in range(6):
	c = Cylinder(h = 200, r=10).translate(0,80,0)
	result += c.rotate(Z_axis, i*60)
	
result += Cylinder(h = 80, r1 = 120, r2 = 0).translate(0, 0, 200)

result = result.translate(0, 0, -120)
