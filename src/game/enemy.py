import obj
from game.image import SpriteSheet
from game.cam import Cam
from game.alive import ObjAlive
from game.tile import TileCollision, VOID, RECT
from abc import abstractmethod
import pygame as pg


ANIMS = {
	"runRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,True,DUR=8),
			obj.sprite.Frame(1,0,True,DUR=8),
			obj.sprite.Frame(2,0,True,DUR=8),
			obj.sprite.Frame(1,0,True,DUR=8)
		),
	),
	"runLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,DUR=8),
			obj.sprite.Frame(1,0,DUR=8),
			obj.sprite.Frame(2,0,DUR=8),
			obj.sprite.Frame(1,0,DUR=8)
		),
	)
}


HIT_OFFSET_H = 0
HIT_OFFSET_W = 0
HIT_BOX_W = 16
HIT_BOX_H = 32
HIT_CNT_MAX = 8 # par o se queda invisible
H_VEL = 1

class Ficha(
	ObjAlive,
	obj.ObjStaticR,
	obj.sprite.ObjAnim,
	obj.ObjUpdate
):

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, life, maxLife, sprtShtHash, camHash, x, y):

		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet, sprtShtHash, HASH)

		self._cam = obj.getGroup(Cam)[camHash]


		ObjAlive.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			self._sprtSht.clip.w,
			self._sprtSht.clip.h,
			self._cam,
			pg.math.Vector2(x, y),
			life,
			maxLife,
			HIT_OFFSET_H,
			HIT_OFFSET_W,
			HIT_BOX_W,
			HIT_BOX_H
		)
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		obj.sprite.ObjAnim.__init__(self, HASH, FATHR_HASH, self._sprtSht, 0, 0)

		self.anim = ANIMS["runRight"]
		self._hitCnt = 0
		self._facingRight = False

	def update(self):
		if self._hitCnt == 0:
			tlBellow = False

			if self._facingRight:
				for tls in obj.getGroup(TileCollision):

					x, y = self.hitBox.bottomright

					tl = tls[y-1,x]

					if tl.form == RECT:
						self._facingRight = False
						break

					tl = tls[y,x]

					if tl.form == RECT:
						tlBellow = True

				if not tlBellow:
					self._facingRight = False

			else:
				tlBellow = False

				for tls in obj.getGroup(TileCollision):

					x, y = self.hitBox.bottomleft

					tl = tls[y-1,x-1]

					if tl.form == RECT:
						self._facingRight = True
						break

					tl = tls[y,x-1]

					if tl.form == RECT:
						tlBellow = True

				if not tlBellow:
					self._facingRight = True

			self.pos.x += H_VEL if self._facingRight else -H_VEL

	def draw(self):
		if self._facingRight:
			if self.anim != ANIMS["runRight"]:
				self.anim = ANIMS["runRight"]

		else:
			if self.anim != ANIMS["runLeft"]:
				self.anim = ANIMS["runLeft"]

		ObjAlive.draw(self)
		obj.sprite.ObjAnim.draw(self)

		if self._hitCnt != 0:
			self.image.set_alpha(255 if self._hitCnt%2 else 0)
			self._hitCnt -= 1			

		obj.ObjDraw.draw(self)

	def close(self):
		self._sprtSht.leave()

	def attack(self, dmg):
		self._hitCnt = HIT_CNT_MAX
		self.life -= dmg
		

class Peon(Ficha):
	GRP_FILE = "game/data/peones.json"
	UPDT_POS = 2
	DRAW_LAYER = 9

	def __init__(self, HASH, FATHR_HASH, life, camHash, x, y):
		Ficha.__init__(self, HASH, FATHR_HASH, life, 5, 4, camHash, x, y)

try:
	obj.getGroup(Peon)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Peon))
