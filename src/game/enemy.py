import obj
from game.image import SpriteSheet
from game.cam import Cam
from game.alive import ObjAlive
from game.tile import TileCollision, VOID, RECT
from game.player import Player
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

HIT_CNT_MAX = 16 # par o se queda invisible

H_VEL = 1

class Ficha(
	ObjAlive,
	obj.ObjStaticR,
	obj.sprite.ObjAnim,
	obj.ObjUpdate
):

	@abstractmethod
	def __init__(
		self,
		HASH,
		FATHR_HASH,
		life,
		maxLife,
		dmg,
		sprtShtHash,
		camHash,
		x,
		y
	):

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
		self._dmg = dmg

	def update(self):
		if self._hitCnt == 0:
			if self.life <= 0:
				self.close()
				return

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

		for player in obj.getGroup(Player):
			if player.hitBox.colliderect(self.hitBox):
				player.attack(self._dmg)

	def draw(self):
		if self._facingRight:
			if self.anim != ANIMS["runRight"]:
				self.anim = ANIMS["runRight"]

		else:
			if self.anim != ANIMS["runLeft"]:
				self.anim = ANIMS["runLeft"]

		ObjAlive.draw(self)

		if self._hitCnt != 0:
			self.image.set_alpha(255 if self._hitCnt%4 >= 2 else 0)
			self._hitCnt -= 1
		else:
			obj.sprite.ObjAnim.draw(self)	

		obj.ObjDraw.draw(self)

	def close(self):
		self._sprtSht.leave()
		obj.Obj.close(self)

	def attack(self, dmg):
		self._hitCnt = HIT_CNT_MAX
		self.life -= dmg
		

PEON_LIFE = 1
PEON_DMG = 1
PEON_SPRT_SHT = 4

class Peon(Ficha):
	GRP_FILE = "game/data/peones.json"
	UPDT_POS = 2
	DRAW_LAYER = 9

	def __init__(self, HASH, FATHR_HASH, life, camHash, x, y):
		Ficha.__init__(
			self,
			HASH,
			FATHR_HASH,
			life,
			PEON_LIFE,
			PEON_DMG,
			PEON_SPRT_SHT,
			camHash,
			x,
			y
		)

try:
	obj.getGroup(Peon)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Peon))


ALFIL_LIFE = 2
ALFIL_DMG = 2
ALFIL_SPRT_SHT = 4

class Alfil(Ficha):
	GRP_FILE = "game/data/alfiles.json"
	UPDT_POS = 2
	DRAW_LAYER = 9

	def __init__(self, HASH, FATHR_HASH, life, camHash, x, y):
		Ficha.__init__(
			self,
			HASH,
			FATHR_HASH,
			life,
			ALFIL_LIFE,
			ALFIL_DMG,
			ALFIL_SPRT_SHT,
			camHash,
			x,
			y
		)

try:
	obj.getGroup(Alfil)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Alfil))


CABALLO_LIFE = 2
CABALLO_DMG = 3
CABALLO_SPRT_SHT = 4

class Caballo(Ficha):
	GRP_FILE = "game/data/caballos.json"
	UPDT_POS = 2
	DRAW_LAYER = 9

	def __init__(self, HASH, FATHR_HASH, life, camHash, x, y):
		Ficha.__init__(
			self,
			HASH,
			FATHR_HASH,
			life,
			CABALLO_LIFE,
			CABALLO_DMG,
			CABALLO_SPRT_SHT,
			camHash,
			x,
			y
		)

try:
	obj.getGroup(Caballo)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Caballo))


TORRE_LIFE = 2
TORRE_DMG = 3
TORRE_SPRT_SHT = 4

class Torre(Ficha):
	GRP_FILE = "game/data/torres.json"
	UPDT_POS = 2
	DRAW_LAYER = 9

	def __init__(self, HASH, FATHR_HASH, life, camHash, x, y):
		Ficha.__init__(
			self,
			HASH,
			FATHR_HASH,
			life,
			TORRE_LIFE,
			TORRE_DMG,
			TORRE_SPRT_SHT,
			camHash,
			x,
			y
		)

try:
	obj.getGroup(Torre)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Torre))
