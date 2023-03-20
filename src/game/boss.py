import obj
from game.alive import ObjAlive
from game.image import SpriteSheet
from game.cam import Cam
from game.stand import StandEnemy
from game.tile import TileCollision, RECT
import pygame as pg


ANIMS = {
	"standLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,True),
		),
		False
	),
	"standRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0),
		),
		False
	),
	"runLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,True,DUR=8),
			obj.sprite.Frame(1,0,True,DUR=8),
			obj.sprite.Frame(2,0,True,DUR=8),
			obj.sprite.Frame(3,0,True,DUR=8)
		),
	),
	"runRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,DUR=8),
			obj.sprite.Frame(1,0,DUR=8),
			obj.sprite.Frame(2,0,DUR=8),
			obj.sprite.Frame(3,0,DUR=8)
		),
	)
}

HIT_OFFSET_H = 8
HIT_OFFSET_V = 0
HIT_BOX_W = 16
HIT_BOX_H = 32

HIT_CNT_MAX = 8 # par o se queda invisible

H_VEL = 1

ATTACK_COOLDOWN = 64

PLAYER_HASH = 0
PLAYER_OFFSET = 32

STAND_OFFSET_H = 10
STAND_OFFSET_V = 42

class BasicBoss(
	ObjAlive,
	obj.ObjStaticRW,
	obj.sprite.ObjAnim,
	obj.ObjUpdate
):
	GRP_FILE = "game/data/basic_bosses.json"
	UPDT_POS = 2
	DRAW_LAYER = 9

	def __init__(
		self,
		HASH,
		FATHR_HASH,
		life,
		maxLife,
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
			HIT_OFFSET_V,
			HIT_BOX_W,
			HIT_BOX_H
		)
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		obj.sprite.ObjAnim.__init__(self, HASH, FATHR_HASH, self._sprtSht, 0, 0)

		self.anim = ANIMS["runLeft"]
		self._hitCnt = 0
		self._facingRight = False
		self._player = obj.getGroup("Player")[PLAYER_HASH]

		self._attackCnt = 0

		self._stand = None

	def update(self):
		if self._hitCnt == 0:
			if self.life <= 0:
				self.save()
				self.close()
				return

			if self._facingRight:
				for tls in obj.getGroup(TileCollision):
					x, y = self.hitBox.bottomleft
					tl = tls[y-1,x-1]

					if tl.form == RECT:
						self._facingRight = False
						break

				if self._facingRight:
					if self._player.hitBox.center[0]-PLAYER_OFFSET > self.hitBox.center[0]:
						self.pos.x += H_VEL

					elif self._player.hitBox.center[0]-PLAYER_OFFSET < self.hitBox.center[0]:
						self.pos.x -= H_VEL

				if self._attackCnt == 0:
					if self.hitBox.center[0]-16 <= self._player.hitBox.center[0]-PLAYER_OFFSET < self.hitBox.center[0]+16:
						self._attackCnt = ATTACK_COOLDOWN
						self._stand = StandEnemy(hash(self), 11, "basicRight", self.pos.x-STAND_OFFSET_H, self.pos.y-STAND_OFFSET_V)
				else:
					self._attackCnt -= 1
				

			else:
				for tls in obj.getGroup(TileCollision):
					x, y = self.hitBox.bottomright
					tl = tls[y-1,x]

					if tl.form == RECT:
						self._facingRight = True
						break

				if not self._facingRight:
					if self._player.hitBox.center[0] < self.hitBox.center[0]-PLAYER_OFFSET:
						self.pos.x -= H_VEL

					elif self._player.hitBox.center[0] > self.hitBox.center[0]-PLAYER_OFFSET:
						self.pos.x += H_VEL
				
				if self._attackCnt == 0:
					if self.hitBox.center[0]-PLAYER_OFFSET-16 <= self._player.hitBox.center[0] < self.hitBox.center[0]-PLAYER_OFFSET+16:
						self._attackCnt = ATTACK_COOLDOWN
						self._stand = StandEnemy(hash(self), 11, "basicLeft", self.pos.x-32-STAND_OFFSET_H, self.pos.y-STAND_OFFSET_V)
				else:
					self._attackCnt -= 1


	def draw(self):
		if self._facingRight:
			if self._player.hitBox.center[0]-PLAYER_OFFSET != self.hitBox.center[0]:
				if self.anim != ANIMS["runRight"]:
					self.anim = ANIMS["runRight"]
			else:
				if self.anim != ANIMS["standRight"]:
					self.anim = ANIMS["standRight"]

		else:
			if self._player.hitBox.center[0] != self.hitBox.center[0]-PLAYER_OFFSET:
				if self.anim != ANIMS["runLeft"]:
					self.anim = ANIMS["runLeft"]
			else:
				if self.anim != ANIMS["standLeft"]:
					self.anim = ANIMS["standLeft"]

		ObjAlive.draw(self)

		if self._hitCnt != 0:
			self.image.set_alpha(255 if self._hitCnt%4 >= 2 else 0)
			self._hitCnt -= 1
		else:
			obj.sprite.ObjAnim.draw(self)	

		obj.ObjDraw.draw(self)


	@property
	def active(self):
		return self._active

	@active.setter
	def active(self, value):
		if self._stand:
			self._stand.active = value

		self._active = value

	def close(self):
		if self._stand and self._stand.active:
			self._stand.close()

		self._sprtSht.leave()
		obj.Obj.close(self)

	def attack(self, dmg):
		if self._hitCnt == 0:
			self._hitCnt = HIT_CNT_MAX
			self.life -= dmg

	def save(self):
		self._save(
			life = self.life,
			maxLife = self.maxLife,
			sprtShtHash=hash(self._sprtSht),
			camHash=hash(self._cam),
			x=self.pos.x,
			y=self.pos.y
		)

try:
	obj.getGroup(BasicBoss)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(BasicBoss))
