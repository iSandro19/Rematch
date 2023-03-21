import obj
from game.alive import ObjAlive
from game.image import Surface
from game.cam import Cam
import pygame as pg


BB_SURF_HASH	= 13
BB_LIFE			= 2
BB_HIT_OFFSET_H	= 0
BB_HIT_OFFSET_V	= 0
BB_HIT_BOX_W	= 16
BB_HIT_BOX_H	= 16
BB_HIT_CNT_MAX	= 8

class BreakBlock(obj.ObjStaticR, ObjAlive):
	GRP_FILE = "game/data/break_blocks.json"
	DRAW_LAYER = 10

	def __init__(self, HASH, FATHR_HASH, camHash, x, y):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)

		try:
			self._surf = obj.getGroup(Surface)[BB_SURF_HASH]
			self._surf.watch()
		except obj.ObjNotFoundError:
			self._surf = obj.load(Surface, BB_SURF_HASH, FATHR_HASH)

		self._cam = obj.getGroup(Cam)[camHash]

		_, _, w, h = self._surf.image.get_rect()

		ObjAlive.__init__(
			self,
			HASH,
			FATHR_HASH,
			self._surf.image.copy(),
			w,
			h,
			self._cam,
			pg.math.Vector2(x, y),
			BB_LIFE,
			BB_LIFE,
			BB_HIT_OFFSET_H,
			BB_HIT_OFFSET_V,
			BB_HIT_BOX_W,
			BB_HIT_BOX_H
		)

		self._hitCnt = 0


	def draw(self):
		if self._hitCnt != 0:
			if self.life <= 0:
				self.close()
				return

			self.image.set_alpha(255 if self._hitCnt%4 <= 2 else 0)
			self._hitCnt -= 1

		ObjAlive.draw(self)
		obj.ObjDraw.draw(self)

	def attack(self, dmg):
		if self._hitCnt == 0:
			self._hitCnt = BB_HIT_CNT_MAX
			self.life -= dmg

	def close(self):
		self._surf.leave()
		obj.Obj.close(self)

try:
	obj.getGroup(BreakBlock)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(BreakBlock))
