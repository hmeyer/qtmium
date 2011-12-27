m = Text('M',
		fontpath='/usr/share/fonts/truetype/freefont/FreeSans.ttf', # Give full path on your system
		height=25,
		thickness=20).translate(0,-12.5,5)
textbox = (Box(30,30,20, center = True).translate(0,0,12)
	 - m
	)

result = Sphere(20) - textbox
