l = []

for i in [[0, 0, 0],
		[10, 20, 300],
		[200, 40, 57],
		[20, 88, 57]
	]:
	l.append( Box(100, 20, 20, center = True)
		.rotate(X_axis, i[0])
		.rotate(Y_axis, i[1])
		.rotate(Z_axis, i[2])
		)
		
result = l[0]
for i  in l[1:]: result *= i

