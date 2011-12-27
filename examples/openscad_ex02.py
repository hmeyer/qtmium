
result = (
		(
			(
				Box(30, center = True) + 
				Box(15, 15, 50, center = True).translate(0, 0, -25)
			) -
			(
				Box(50, 10, 10, center = True) +
				Box(10, 50, 10, center = True) +
				Box(10, 10, 50, center = True)
			)
		) * 
		Cylinder(h = 50, r1 = 20, r2 = 5, center = True).translate(0, 0, 5)
	)