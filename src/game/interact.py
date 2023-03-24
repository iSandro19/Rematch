import obj
from game.alive import ObjAlive
from game.image import Surface, SpriteSheet
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


PORTAL_SPRITE_SHEET_HASH = 31

ANIM = obj.sprite.Animation(
	(
		obj.sprite.Frame(0,0,True,DUR=4),
		obj.sprite.Frame(1,0,True,DUR=4),
		obj.sprite.Frame(2,0,True,DUR=4),
		obj.sprite.Frame(3,0,True,DUR=4)
	)
)

class Portal(obj.ObjStaticR, obj.physic.ObjRelative, obj.sprite.ObjAnim):
	GRP_FILE = "game/data/portals.json"
	DRAW_LAYER = 8

	def __init__(self, HASH, FATHR_HASH, camHash, x, y):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)

		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[PORTAL_SPRITE_SHEET_HASH]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet, PORTAL_SPRITE_SHEET_HASH, HASH)

		self._cam = obj.getGroup(Cam)[camHash]

		obj.sprite.ObjAnim.__init__(self, HASH, FATHR_HASH, self._sprtSht, 0, 0)

		obj.physic.ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			self._sprtSht.clip.w,
			self._sprtSht.clip.h,
			self._cam,
			pg.math.Vector2(x, y)
		)

		self.anim = ANIM

		self.beat = False

	def draw(self):
		obj.sprite.ObjAnim.draw(self)
		obj.physic.ObjRelative.draw(self)
		obj.ObjDraw.draw(self)

	@property
	def active(self):
		return self._active

	@active.setter
	def active(self, value):
		self._active = value and self.beat

	def close(self):
		self._sprtSht.leave()
		obj.Obj.close(self)

try:
	obj.getGroup(Portal)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Portal))
