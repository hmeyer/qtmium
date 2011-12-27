


def blk1():
	return Box(65, 28, 28 , center = True)



def chop():
	m =Text('M',
		fontpath='/usr/share/fonts/truetype/freefont/FreeSans.ttf', # Give full path on your system
		height=25,
		thickness=20).translate(0,-12.5,17)
	return m.translate(-16) + m.translate(16)
		
		
result = blk1()

c = chop()
for alpha in [0, 90, 180, 270]:
	result -= c.rotate(X_axis,alpha)
