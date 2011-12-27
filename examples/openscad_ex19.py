def interp(x, listx, listy):
	if (x < listx[0]) or (x > listx[-1]): return None
	if x == listx[0]: return listy[0]
	if x == listx[-1]: return listy[-1]
	i = 0
	while ((i+1) < len(listx)) and (x > listx[i+1]):
		i += 1
	r = (x - listx[i]) * 1.0 / (listx[i+1] - listx[i])
	return listy[i] * (1-r) + listy[i+1] * r
	
result = Union([
	Cylinder(r1=6,r2=2,h=3*interp(x,
			[-200,-50,-20,80,150],[5,20,18,25,2])).translate(x,0,-30)
				for x in  range(-100,105,5)
	])
	
