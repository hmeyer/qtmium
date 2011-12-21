
def dragon(k,s):
  if k < 1:
    return Sphere(r=.2*s).translate(x=s) + \
      Cylinder(r=.2*s, h=s).rotate(Y_axis,90) + \
      Sphere(r=.2*s)
  else:
    c = pow(complex(1, -1), k)
    return dragon(k-1,s) +\
      dragon(k-1,s).rotate(Z_axis, 90).translate(x=c.real,y=c.imag)

print 'This is going to take a while...'
result = dragon(8,1)

