class Box:
	x 		= 	0
	y 		= 	0
	direction 	= 	0
	speed 			=	0
	width 			= 	30
	height			=	30
	color 			=	(0,0,0)

	def __init__(self,X,Y,Width,Height,Direction,Speed):		
		self.x = X
		self.y = Y
		self.direction = Direction 
		self.speed = Speed
		self.width = Width
		self.height = Height