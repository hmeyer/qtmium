

b0 = Box(x=4, y=4, z=4, center=True)
b1 = Box(x=4, y=4, z=4, center=True).rotate(X_axis, 45)
b2 = Box(x=4, y=4, z=4, center=True).rotate(Y_axis, 45)
b3 = Box(x=4, y=4, z=4, center=True).rotate(Z_axis, 45)

result = b0 * b1 * b2 * b3
