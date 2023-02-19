import obj


anims = {
	"standRight": obj.draw.Animation(
		(
			obj.draw.Frame(0,0,False,True),
		),
		False
	),
	"standLeft": obj.draw.Animation(
		(
			obj.draw.Frame(0,0),
		),
		False
	),
	"runRight": obj.draw.Animation(
		(
			obj.draw.Frame(0,0,8,False,True),
			obj.draw.Frame(1,0,8,False,True),
			obj.draw.Frame(2,0,8,False,True),
			obj.draw.Frame(1,0,8,False,True),
		)
	),
	"runLeft": obj.draw.Animation(
		(
			obj.draw.Frame(0,0,8),
			obj.draw.Frame(1,0,8),
			obj.draw.Frame(2,0,8),
			obj.draw.Frame(1,0,8),
		)
	),
	"jumpRight": obj.draw.Animation(
		(
			obj.draw.Frame(3,0,False,True),
		),
		False
	),
	"jumpLeft": obj.draw.Animation(
		(
			obj.draw.Frame(3,0),
		),
		False
	)
}

TestAnim.SPRTS = obj.draw.SpriteSheet(
	pg.image.load("obj/images/CV3.png"),
	16,
	32,
	(255,0,0)
)



class Player(obj.ObjState, obj.ObjPhysic):

	# Actions

	def __init__(self):
		self.image = pg.Surface("standing.bmp")
		self.rect = self.image.get_rect()


	def goRight(self): ...

	def goLeft(self): ...

	def stop(self): ...


	# States

	def _standing(self): ...

	def _walking(self): ...