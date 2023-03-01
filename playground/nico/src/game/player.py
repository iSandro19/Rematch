import obj
import pygame as pg
from game.cam import Cam


"""
ANIMS = {
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
			obj.draw.Frame(0,0,False,True,8),
			obj.draw.Frame(1,0,False,True,8),
			obj.draw.Frame(2,0,False,True,8),
			obj.draw.Frame(1,0,False,True,8),
		)
	),
	"runLeft": obj.draw.Animation(
		(
			obj.draw.Frame(0,0,DUR=8),
			obj.draw.Frame(1,0,DUR=8),
			obj.draw.Frame(2,0,DUR=8),
			obj.draw.Frame(1,0,DUR=8),
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
	pg.image.load("game/images/CV3.png"),
	16,
	32,
	(255,0,0)
)

HITBOX_W = 16
HITBOX_H = 32

IMG_W = 16
IMG_H = 32

class Player(obj.ObjState, obj.ObjPhysic):

	# Actions

	def __init__(self, INST_ID, x, y):
		pos = pg.Rect(x, y, HITBOX_W, HITBOX_H)
		rect = pg.Rect()
		obj.ObjState.__init__(self, INST_ID)
		obj.ObjPhysic.__init__(self, INST_ID, None, rect, REF_POINT, pos, acc, vel)
		self.image = pg.Surface("standing.bmp")
		self.rect = self.image.get_rect()


	def goRight(self): ...

	def goLeft(self): ...

	def stop(self): ...


	# States

	def _jumping

	def _standing(self): ...

	def _walking(self): ...

"""

class Test(obj.ObjDynamic, obj.ObjUpdate):
	UPDT_POS=0
	def __init__(self, FATHR_HASH):
		obj.ObjDynamic.__init__(self, FATHR_HASH)
		self._cam = obj.getGroup(Cam)[0]

	def update(self):
		if(pg.key.get_pressed()[pg.K_a]):
			self._cam.move_ip(-1,0)

		if(pg.key.get_pressed()[pg.K_d]):
			self._cam.move_ip(1,0)

		if(pg.key.get_pressed()[pg.K_w]):
			self._cam.move_ip(0,-1)

		if(pg.key.get_pressed()[pg.K_s]):
			self._cam.move_ip(0,1)

try:
	obj.getGroup(Test)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Test))

