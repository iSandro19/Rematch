import obj
from game.image import Surface
from game.cam import Cam
import pygame as pg


class Cartel(obj.ObjStaticR, obj.physic.ObjRelative):
	GRP_FILE = "game/data/carteles.json"
	DRAW_LAYER = 6

	def __init__(self, HASH, FATHR_HASH, camHash, surfHash, x, y):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)

		try:
			self._surf = obj.getGroup(Surface)[surfHash]
			self._surf.watch()
		except obj.ObjNotFoundError:
			self._surf = obj.load(Surface, surfHash, HASH)

		self._cam = obj.getGroup(Cam)[camHash]

		_, _, w, h = self._surf.image.get_rect()

		obj.physic.ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			self._surf.image,
			w,
			h,
			self._cam,
			pg.math.Vector2(x, y)
		)

	def draw(self):
		obj.physic.ObjRelative.draw(self)
		obj.ObjDraw.draw(self)

	def close(self):
		self._surf.leave()
		obj.Obj.close(self)

try:
	obj.getGroup(Cartel)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Cartel))
