import obj
from game.alive import ObjAlive
from game.image import SpriteSheet
from game.cam import Cam
from game.stand import StandEnemy
from game.tile import TileCollision, RECT
from game.powerup import PowerUp
from game.interact import Portal
import pygame as pg
import math as m
from random import shuffle


BB_ANIMS = {
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

BB_HIT_OFFSET_H = 8
BB_HIT_OFFSET_V = 0
BB_HIT_BOX_W = 16
BB_HIT_BOX_H = 32

BB_HIT_CNT_MAX = 8 # par o se queda invisible

BB_H_VEL = 1

BB_ATTACK_COOLDOWN = 64

BB_PLAYER_HASH = 0
BB_PLAYER_OFFSET = 32

BB_STAND_OFFSET_H = 10
BB_STAND_OFFSET_V = 42

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
		standSprtShtHash,
		camHash,
		attackRight,
		attackLeft,
		x,
		y,
		powerupHash
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
			BB_HIT_OFFSET_H,
			BB_HIT_OFFSET_V,
			BB_HIT_BOX_W,
			BB_HIT_BOX_H
		)
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		obj.sprite.ObjAnim.__init__(self, HASH, FATHR_HASH, self._sprtSht, 0, 0)

		self.anim = BB_ANIMS["runLeft"]
		self._hitCnt = 0
		self._facingRight = False
		self._player = obj.getGroup("Player")[BB_PLAYER_HASH]

		self._attackCnt = 0

		self._attackRight = attackRight
		self._attackLeft = attackLeft
		self._standSprtShtHash = standSprtShtHash

		self._stand = None
		self.slash1_sound = pg.mixer.Sound('game/sounds/slashBoss.ogg')

		self._powerupHash = powerupHash
		


	def update(self):
		if self._hitCnt == 0:
			if self.life <= 0:				
				self.save()
				self.close()
				if powerupHash:
					obj.load(PowerUp, powerupHash, HASH)
				return

			if self._facingRight:
				for tls in obj.getGroup(TileCollision):
					x, y = self.hitBox.bottomleft
					tl = tls[y-1,x-1]

					if tl.form == RECT:
						self._facingRight = False
						break

				if self._facingRight:
					if self._player.hitBox.center[0]-BB_PLAYER_OFFSET > self.hitBox.center[0]:
						self.pos.x += BB_H_VEL

					elif self._player.hitBox.center[0]-BB_PLAYER_OFFSET < self.hitBox.center[0]:
						self.pos.x -= BB_H_VEL

				if self._attackCnt == 0:
					if self.hitBox.center[0]-16 <= self._player.hitBox.center[0]-BB_PLAYER_OFFSET < self.hitBox.center[0]+16:
						self._attackCnt = BB_ATTACK_COOLDOWN
						self._stand = StandEnemy(hash(self), self._standSprtShtHash, self._attackRight, self.pos.x-BB_STAND_OFFSET_H, self.pos.y-BB_STAND_OFFSET_V)
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
					if self._player.hitBox.center[0] < self.hitBox.center[0]-BB_PLAYER_OFFSET:
						self.pos.x -= BB_H_VEL

					elif self._player.hitBox.center[0] > self.hitBox.center[0]-BB_PLAYER_OFFSET:
						self.pos.x += BB_H_VEL
				
				if self._attackCnt == 0:
					if self.hitBox.center[0]-BB_PLAYER_OFFSET-16 <= self._player.hitBox.center[0] < self.hitBox.center[0]-BB_PLAYER_OFFSET+16:
						self._attackCnt = BB_ATTACK_COOLDOWN
						self._stand = StandEnemy(hash(self), self._standSprtShtHash, self._attackLeft, self.pos.x-32-BB_STAND_OFFSET_H, self.pos.y-BB_STAND_OFFSET_V)
				else:
					self._attackCnt -= 1


	def draw(self):
		if self._facingRight:
			if self._player.hitBox.center[0]-BB_PLAYER_OFFSET != self.hitBox.center[0]:
				if self.anim != BB_ANIMS["runRight"]:
					self.anim = BB_ANIMS["runRight"]
			else:
				if self.anim != BB_ANIMS["standRight"]:
					self.anim = BB_ANIMS["standRight"]

		else:
			if self._player.hitBox.center[0] != self.hitBox.center[0]-BB_PLAYER_OFFSET:
				if self.anim != BB_ANIMS["runLeft"]:
					self.anim = BB_ANIMS["runLeft"]
			else:
				if self.anim != BB_ANIMS["standLeft"]:
					self.anim = BB_ANIMS["standLeft"]

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
			self._hitCnt = BB_HIT_CNT_MAX
			self.life -= dmg
			self.slash1_sound.play()

	def save(self):
		self._save(
			life = self.life,
			maxLife = self.maxLife,
			sprtShtHash=hash(self._sprtSht),
			camHash=hash(self._cam),
			x=self.pos.x,
			y=self.pos.y,
			attackRight=self._attackRight,
			attackLeft=self._attackLeft,
			standSprtShtHash=self._standSprtShtHash,
			powerupHash=self._powerupHash
		)

try:
	obj.getGroup(BasicBoss)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(BasicBoss))


FB_ANIMS = {
	"flyLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,True,DUR=2),
			obj.sprite.Frame(1,0,True,DUR=2),
			obj.sprite.Frame(2,0,True,DUR=2),
			obj.sprite.Frame(3,0,True,DUR=2)
		),
	),
	"flyRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,DUR=2),
			obj.sprite.Frame(1,0,DUR=2),
			obj.sprite.Frame(2,0,DUR=2),
			obj.sprite.Frame(3,0,DUR=2)
		),
	)
}

FB_HIT_OFFSET_H = 8
FB_HIT_OFFSET_V = 8
FB_HIT_BOX_W = 16
FB_HIT_BOX_H = 40

FB_HIT_CNT_MAX = 8 # par o se queda invisible

FB_H_VEL = 1
FB_V_VEL = 1

FB_KNOCKBACK = 8

FB_ATTACK_COOLDOWN = 64

FB_PLAYER_HASH = 0
FB_PLAYER_OFFSET_H = 64
FB_PLAYER_OFFSET_V = 64

FB_STAND_OFFSET_H = 10
FB_STAND_OFFSET_V = -8

FB_ROOM_W = 16*16
FB_ROOM_H = 9*16

FB_STAND_VEL_H = 4
FB_STAND_VEL_V = 4

FB_DELAY_REDUCE_VEL = 16
FB_DELAY_MIN = 64

class FinalBoss(
	ObjAlive,
	obj.ObjStaticRW,
	obj.sprite.ObjAnim,
	obj.ObjUpdate
):
	GRP_FILE = "game/data/final_bosses.json"
	UPDT_POS = 1
	DRAW_LAYER = 9

	def __init__(
		self,
		HASH,
		FATHR_HASH,
		life,
		maxLife,
		sprtShtHash,
		standSprtShtHash,
		camHash,
		x,
		y,
		roomX,
		roomY
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
			FB_HIT_OFFSET_H,
			FB_HIT_OFFSET_V,
			FB_HIT_BOX_W,
			FB_HIT_BOX_H
		)
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		obj.sprite.ObjAnim.__init__(self, HASH, FATHR_HASH, self._sprtSht, 0, 0)

		self.anim = FB_ANIMS["flyLeft"]
		self._hitCnt = 0
		self._facingRight = False
		self._player = obj.getGroup("Player")[FB_PLAYER_HASH]

		self._attackCnt = 0

		self._standSprtShtHash = standSprtShtHash

		self._stand0 = None
		self._stand1 = None

		self._roomX = roomX
		self._roomY = roomY

		self._frmCnt = 0

		self._delay = 128

		self._seq = list(range(1,4))

		for p in obj.getGroup(Portal):
			p.active = False


	def _basicAttack(self):
		self._stand0 = StandEnemy(hash(self), self._standSprtShtHash, "basicRight", self._roomX-40+16*6, self._roomY+6-16*2)
		self._stand1 = StandEnemy(hash(self), self._standSprtShtHash, "basicLeft", self._roomX-40+16*10, self._roomY+6-16*2)

	def _rotatoryAttack(self):
		self._stand0 = StandEnemy(hash(self), self._standSprtShtHash, "rotatoryRight", self._roomX-40+16*4, self._roomY+6-16)
		self._stand1 = StandEnemy(hash(self), self._standSprtShtHash, "rotatoryLeft", self._roomX-40+16*12, self._roomY+6-16)

	def _lanceAttack(self):
		self._stand0 = StandEnemy(hash(self), self._standSprtShtHash, "lanceRight", self._roomX-40+32, self._roomY+6+16*3)
		self._stand1 = StandEnemy(hash(self), self._standSprtShtHash, "lanceLeft", self._roomX-40+224, self._roomY+6+16*3)

	def update(self):
		if self._hitCnt == 0:
			if self.life <= 0:
				self.save()
				self.close()

				for p in obj.getGroup(Portal):
					p.beat = True
					p.active = True
				return

			if self._facingRight and self.hitBox.center[0] > (self._roomX+FB_ROOM_W)//2:
				self._facingRight = False

			elif not self._facingRight and self.hitBox.center[0] < (self._roomX+FB_ROOM_W)//2:
				self._facingRight = True

			if self._facingRight:
				if self._player.hitBox.center[0]-FB_PLAYER_OFFSET_H > self.hitBox.center[0]:
					self.pos.x += FB_H_VEL

				elif self._player.hitBox.center[0]-FB_PLAYER_OFFSET_H < self.hitBox.center[0]:
					self.pos.x -= FB_H_VEL

			else:
				if not self._facingRight:
					if self._player.hitBox.center[0] < self.hitBox.center[0]-FB_PLAYER_OFFSET_H:
						self.pos.x -= FB_H_VEL

					elif self._player.hitBox.center[0] > self.hitBox.center[0]-FB_PLAYER_OFFSET_H:
						self.pos.x += FB_H_VEL

			if self._player.pos.y+FB_STAND_OFFSET_V < self.pos.y:
				self.pos.y -= FB_V_VEL

			elif self._player.pos.y+FB_STAND_OFFSET_V > self.pos.y:
				self.pos.y += FB_V_VEL


			if self._frmCnt == self._delay*self._seq[0]:
				self._lanceAttack()
			elif self._frmCnt == self._delay*self._seq[1]:
				self._basicAttack()
			elif self._frmCnt == self._delay*self._seq[2]:
				self._rotatoryAttack()

			if self._delay*self._seq[0] < self._frmCnt <= self._delay*self._seq[0]+20:
				self._stand0.pos.x += FB_STAND_VEL_H
				self._stand1.pos.x -= FB_STAND_VEL_H

			elif self._delay*self._seq[1] < self._frmCnt <= self._delay*self._seq[1]+20:
				self._stand0.pos.y += FB_STAND_VEL_V
				self._stand1.pos.y += FB_STAND_VEL_V

			if self._frmCnt <= self._delay*4:
				self._frmCnt += 1
			else:
				if self._delay > FB_DELAY_MIN:
					self._delay -= FB_DELAY_REDUCE_VEL

				shuffle(self._seq)
				self._frmCnt = 0


	def draw(self):
		if self._facingRight:
			if self.anim != FB_ANIMS["flyRight"]:
				self.anim = FB_ANIMS["flyRight"]

		else:
			if self.anim != FB_ANIMS["flyLeft"]:
				self.anim = FB_ANIMS["flyLeft"]

		ObjAlive.draw(self)

		if self._hitCnt != 0:
			self.image.set_alpha(255 if self._hitCnt%4 >= 2 else 0)
			self._hitCnt -= 1
		else:
			obj.sprite.ObjAnim.draw(self)	

		obj.ObjDraw.draw(self)

		if self._frmCnt in range(self._delay*self._seq[0]-8-30,self._delay*self._seq[0]-8,4):
			pg.draw.rect(self._BCKGND, (255,0,0), (self._roomX+16-self._cam.x,self._roomY+16*6-self._cam.y,16*14,32))

		elif self._frmCnt in range(self._delay*self._seq[1]-8-30,self._delay*self._seq[1]-8,4):
			pg.draw.rect(self._BCKGND, (255,0,0), (self._roomX+16*6-self._cam.x,self._roomY+16-self._cam.y,64,16*7))

		elif self._frmCnt in range(self._delay*self._seq[2]-8-30,self._delay*self._seq[2]-8,4):
			pg.draw.rect(self._BCKGND, (255,0,0), (self._roomX+16*3-self._cam.x,self._roomY+16*2-self._cam.y,16*3,32))
			pg.draw.rect(self._BCKGND, (255,0,0), (self._roomX+16*10-self._cam.x,self._roomY+16*2-self._cam.y,16*3,32))

	@property
	def active(self):
		return self._active

	@active.setter
	def active(self, value):
		if self._stand0:
			self._stand0.active = value

		if self._stand1:
			self._stand1.active = value

		self._active = value

	def close(self):
		if self._stand0 and self._stand0.active:
			self._stand0.close()

		if self._stand1 and self._stand1.active:
			self._stand1.close()

		self._sprtSht.leave()
		obj.Obj.close(self)

	def attack(self, dmg):
		if self._hitCnt == 0:
			self._hitCnt = FB_HIT_CNT_MAX
			self.life -= dmg

			if self._player.pos != self.pos:
				r = m.radians(self.pos.angle_to(self._player.pos))
				self.pos.x += round(m.cos(r)*FB_KNOCKBACK)
				self.pos.y += round(m.sin(r)*FB_KNOCKBACK)

	def save(self):
		self._save(
			life = self.life,
			maxLife = self.maxLife,
			sprtShtHash=hash(self._sprtSht),
			camHash=hash(self._cam),
			x=self.pos.x,
			y=self.pos.y,
			standSprtShtHash=self._standSprtShtHash,
			roomX=self._roomX,
			roomY=self._roomY
		)

"""
if self._attackCnt == 0:
	if self.hitBox.center[0]-16 <= self._player.hitBox.center[0]-FB_PLAYER_OFFSET < self.hitBox.center[0]+16:
		self._attackCnt = FB_ATTACK_COOLDOWN
		self._stand = StandEnemy(hash(self), self._standSprtShtHash, self._attackRight, self.pos.x-FB_STAND_OFFSET_H, self.pos.y-FB_STAND_OFFSET_V)
else:
	self._attackCnt -= 1

if self._attackCnt == 0:
	if self.hitBox.center[0]-FB_PLAYER_OFFSET-16 <= self._player.hitBox.center[0] < self.hitBox.center[0]-FB_PLAYER_OFFSET+16:
		self._attackCnt = FB_ATTACK_COOLDOWN
		self._stand = StandEnemy(hash(self), self._standSprtShtHash, self._attackLeft, self.pos.x-32-FB_STAND_OFFSET_H, self.pos.y-FB_STAND_OFFSET_V)
else:
	self._attackCnt -= 1
"""

try:
	obj.getGroup(FinalBoss)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(FinalBoss))
