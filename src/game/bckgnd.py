import obj
import pygame as pg
from game.image import Surface
from game.cam import Cam


class Bckgnd(obj.ObjStaticR, obj.physic.ObjRelative):
	GRP_FILE = "game/data/bckgnds.json"
	DRAW_LAYER = 1

	def __init__(self, HASH, FATHR_HASH, surfHash, camHash, x, y):

		try:
			self.surf = obj.getGroup(Surface)[surfHash]
			self.surf.watch()
		except obj.ObjNotFoundError:
			self.surf = obj.load(Surface, surfHash, HASH)

		cam = obj.getGroup(Cam)[camHash]


		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		obj.physic.ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			self.surf.image,
			self.surf.image.get_width(),
			self.surf.image.get_height(),
			cam,
			pg.math.Vector2(x, y)
		)

	def draw(self):
		obj.physic.ObjRelative.draw(self)
		obj.ObjDraw.draw(self)

	def close(self):
		self.surf.leave()
		obj.Obj.close(self)

try:
	obj.getGroup(Bckgnd)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Bckgnd))


class BckgndParallax(obj.ObjStaticR, obj.physic.ObjParallax):
	GRP_FILE = "game/data/bckgnds_par.json"
	DRAW_LAYER = 0

	def __init__(self, HASH, FATHR_HASH, surfHash, camHash, Z_OFFSET, x, y):

		try:
			self.surf = obj.getGroup(Surface)[surfHash]
			self.surf.watch()
		except obj.ObjNotFoundError:
			self.surf = obj.load(Surface, surfHash, HASH)

		cam = obj.getGroup(Cam)[camHash]

		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		obj.physic.ObjParallax.__init__(
			self,
			HASH,
			FATHR_HASH,
			self.surf.image,
			self.surf.image.get_width(),
			self.surf.image.get_height(),
			cam,
			pg.math.Vector2(x, y),
			float(Z_OFFSET)
		)

	def draw(self):
		obj.physic.ObjParallax.draw(self)
		obj.ObjDraw.draw(self)

	def close(self):
		self.surf.leave()
		obj.Obj.close(self)

try:
	obj.getGroup(BckgndParallax)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(BckgndParallax))
