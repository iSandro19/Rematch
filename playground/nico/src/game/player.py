import obj
import pygame as pg
from game.cam import Cam
from game.image import SpriteSheet
from game.control import Control
from game.tile import TileCollision, RECT


ANIMS = {
	"standRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,DUR=128),
			obj.sprite.Frame(1,0,DUR=4),
			obj.sprite.Frame(2,0,DUR=4),
			obj.sprite.Frame(3,0,DUR=4),
			obj.sprite.Frame(4,0,DUR=4),
			obj.sprite.Frame(5,0,DUR=4),
			obj.sprite.Frame(6,0,DUR=4),
			obj.sprite.Frame(7,0,DUR=4),
			obj.sprite.Frame(8,0,DUR=4),
			obj.sprite.Frame(9,0,DUR=4),
			obj.sprite.Frame(10,0,DUR=4),
			obj.sprite.Frame(11,0,DUR=4),
			obj.sprite.Frame(10,0,DUR=4),
			obj.sprite.Frame(9,0,DUR=4),
			obj.sprite.Frame(8,0,DUR=4),
			obj.sprite.Frame(7,0,DUR=4),
			obj.sprite.Frame(8,0,DUR=4),
			obj.sprite.Frame(9,0,DUR=4),
			obj.sprite.Frame(10,0,DUR=4),
			obj.sprite.Frame(11,0,DUR=4),
			obj.sprite.Frame(10,0,DUR=4),
			obj.sprite.Frame(9,0,DUR=4),
			obj.sprite.Frame(8,0,DUR=4),
			obj.sprite.Frame(7,0,DUR=4),
			obj.sprite.Frame(8,0,DUR=4),
			obj.sprite.Frame(9,0,DUR=4),
			obj.sprite.Frame(10,0,DUR=4),
			obj.sprite.Frame(11,0,DUR=4),
			obj.sprite.Frame(10,0,DUR=4),
			obj.sprite.Frame(9,0,DUR=4),
			obj.sprite.Frame(8,0,DUR=4),
			obj.sprite.Frame(7,0,DUR=4),
			obj.sprite.Frame(6,0,DUR=4),
			obj.sprite.Frame(5,0,DUR=4),
			obj.sprite.Frame(4,0,DUR=4),
			obj.sprite.Frame(3,0,DUR=4),
			obj.sprite.Frame(2,0,DUR=4),
			obj.sprite.Frame(1,0,DUR=4),
		),
	),
	"standLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,True,DUR=128),
			obj.sprite.Frame(1,0,True,DUR=4),
			obj.sprite.Frame(2,0,True,DUR=4),
			obj.sprite.Frame(3,0,True,DUR=4),
			obj.sprite.Frame(4,0,True,DUR=4),
			obj.sprite.Frame(5,0,True,DUR=4),
			obj.sprite.Frame(6,0,True,DUR=4),
			obj.sprite.Frame(7,0,True,DUR=4),
			obj.sprite.Frame(8,0,True,DUR=4),
			obj.sprite.Frame(9,0,True,DUR=4),
			obj.sprite.Frame(10,0,True,DUR=4),
			obj.sprite.Frame(11,0,True,DUR=4),
			obj.sprite.Frame(10,0,True,DUR=4),
			obj.sprite.Frame(9,0,True,DUR=4),
			obj.sprite.Frame(8,0,True,DUR=4),
			obj.sprite.Frame(7,0,True,DUR=4),
			obj.sprite.Frame(8,0,True,DUR=4),
			obj.sprite.Frame(9,0,True,DUR=4),
			obj.sprite.Frame(10,0,True,DUR=4),
			obj.sprite.Frame(11,0,True,DUR=4),
			obj.sprite.Frame(10,0,True,DUR=4),
			obj.sprite.Frame(9,0,True,DUR=4),
			obj.sprite.Frame(8,0,True,DUR=4),
			obj.sprite.Frame(7,0,True,DUR=4),
			obj.sprite.Frame(8,0,True,DUR=4),
			obj.sprite.Frame(9,0,True,DUR=4),
			obj.sprite.Frame(10,0,True,DUR=4),
			obj.sprite.Frame(11,0,True,DUR=4),
			obj.sprite.Frame(10,0,True,DUR=4),
			obj.sprite.Frame(9,0,True,DUR=4),
			obj.sprite.Frame(8,0,True,DUR=4),
			obj.sprite.Frame(7,0,True,DUR=4),
			obj.sprite.Frame(6,0,True,DUR=4),
			obj.sprite.Frame(5,0,True,DUR=4),
			obj.sprite.Frame(4,0,True,DUR=4),
			obj.sprite.Frame(3,0,True,DUR=4),
			obj.sprite.Frame(2,0,True,DUR=4),
			obj.sprite.Frame(1,0,True,DUR=4),
		)
	),
	"runRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,1,DUR=4),
			obj.sprite.Frame(1,1,DUR=4),
			obj.sprite.Frame(2,1,DUR=4),
			obj.sprite.Frame(3,1,DUR=4),
			obj.sprite.Frame(4,1,DUR=4),
			obj.sprite.Frame(5,1,DUR=4),
			obj.sprite.Frame(6,1,DUR=4),
			obj.sprite.Frame(7,1,DUR=4),
		)
	),
	"runLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,1,True,DUR=4),
			obj.sprite.Frame(1,1,True,DUR=4),
			obj.sprite.Frame(2,1,True,DUR=4),
			obj.sprite.Frame(3,1,True,DUR=4),
			obj.sprite.Frame(4,1,True,DUR=4),
			obj.sprite.Frame(5,1,True,DUR=4),
			obj.sprite.Frame(6,1,True,DUR=4),
			obj.sprite.Frame(7,1,True,DUR=4),
		)
	),
	"jumpRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(4,1),
		),
		False
	),
	"jumpLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(4,1,True),
		),
		False
	)
}

C_BOX_W = 8
C_BOX_H = 16

C_BOX_W_OFFSET = 4
C_BOX_H_OFFSET = 0

IMG_W = 16
IMG_H = 16

MAX_H_VEL = 2
MAX_V_VEL = 2

MAX_H_WJ_VEL = 1
MAX_V_WJ_VEL = 2

H_ACC = 0.2
V_ACC = 0.2

JUMP_VEL = 3

class Player(obj.physic.ObjPhysic, obj.ObjStaticRW, obj.sprite.ObjAnim): 
	GRP_FILE = "game/data/players.json"
	UPDT_POS = 1
	DRAW_LAYER = 0

	def __init__(
		self,
		HASH,
		FATHR_HASH,
		controlHash,
		sprtShtHash,
		camHash,
		x,
		y
	):
		self._control = obj.getGroup(Control)[controlHash]

		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet, sprtShtHash, HASH)

		self._cam = obj.getGroup(Cam)[camHash]

		obj.state.ObjState.__init__(self, HASH, FATHR_HASH)
		obj.physic.ObjPhysic.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			IMG_W,
			IMG_H,
			self._cam,
			pg.math.Vector2(x, y),
			C_BOX_W_OFFSET,
			C_BOX_H_OFFSET,
			C_BOX_W,
			C_BOX_H,
			pg.math.Vector2(0, 0),
			pg.math.Vector2(0, 0)
		)
		obj.sprite.ObjAnim.__init__(self, HASH, FATHR_HASH, self._sprtSht, x, y)
		obj.ObjStaticRW.__init__(self, HASH, FATHR_HASH)

		self.anim = ANIMS["standRight"]
		self._inGround = True
		self._facingRight = True


	def update(self):
		keys = pg.key.get_pressed()

		prevVel = self.vel.copy()
		prevAcc = self.acc.copy()
		prevPos = self.pos.copy()


		if keys[self._control["jump"]] and not self._inGround:
			for tls in obj.getGroup(TileCollision):
				if self._facingRight and keys[self._control["right"]] or not keys[self._control["left"]]:
					x, y = self.cBox.bottomright
					tl = tls[y-1,round(x+self.vel.x)]

					if tl.form == RECT:
						self._facingRight = False
						self.vel.x = -MAX_H_WJ_VEL
						self.vel.y = -MAX_V_WJ_VEL

				elif not self._facingRight and keys[self._control["left"]] or not keys[self._control["right"]]:
					x, y = self.cBox.bottomleft
					tl = tls[y-1,round(x-1-self.vel.x)]

					if tl.form == RECT:
						self._facingRight = True
						self.vel.x = MAX_H_WJ_VEL
						self.vel.y = -MAX_V_WJ_VEL

		if self._inGround:		
			if keys[self._control["jump"]]:
				self._inGround = False
				self.vel.y = -JUMP_VEL

		else:
			self.acc.y = V_ACC
			if prevVel.y < 0:
				if not keys[self._control["jump"]]:
					self.vel.y = 0

				elif prevVel.y > MAX_V_VEL:
					self.vel.y = MAX_V_VEL


		if prevVel.x == 0:
			if prevAcc.x == 0:
				if keys[self._control["right"]] and not keys[self._control["left"]]:
					self.acc.x = H_ACC
					
					self._facingRight = True

				elif keys[self._control["left"]] and not keys[self._control["right"]]:
					self.acc.x = -H_ACC
					self.acc.y = V_ACC
					self._facingRight = False

			else:
				self.acc.x = 0

		elif prevVel.x > 0:
			self._inGround = False
			self.acc.y = V_ACC
			if not keys[self._control["right"]] or keys[self._control["left"]]:
				if prevVel.x - H_ACC < 0:
					self.vel.x = 0
					self.acc.x = 0
				else:
					self.acc.x = -H_ACC

			else:
				if prevAcc.x > 0 and prevVel.x > MAX_H_VEL:
					self.acc.x = 0
					self.vel.x = MAX_H_VEL

				elif prevAcc.x < 0:
					self.acc.x = H_ACC

		else:
			self._inGround = False
			self.acc.y = V_ACC
			if not keys[self._control["left"]] or keys[self._control["right"]]:
				if prevVel.x + H_ACC > 0:
					self.vel.x = 0
					self.acc.x = 0
				else:
					self.acc.x = H_ACC

			else:
				if prevAcc.x < 0 and prevVel.x < -MAX_H_VEL:
					self.acc.x = 0
					self.vel.x = -MAX_H_VEL

				elif prevAcc.x > 0:
					self.acc.x = -H_ACC


		obj.physic.ObjPhysic.updateX(self)

		pg.draw.rect(self._BCKGND, (0,255,0), self.cBox.move(-self._cam.x,-self._cam.y), 1)

		if self.vel.x != 0 or self.acc.x == H_ACC or self.acc.x == -H_ACC:
			for tls in obj.getGroup(TileCollision):
				if self.vel.x > 0 or (self._facingRight and self.acc.x == H_ACC):
					x, y = self.cBox.topright
					tl = tls[y+4,x]
					pg.draw.rect(self._BCKGND, (255,0,0), (x-self._cam.x,y+4-self._cam.y,1,1))

					if tl.form == RECT:
						self.cBox.right = tl.rect.left
						self.pos.x = self.cBox.x - self._cBoxOffsetH
						self.vel.x = 0
						self.acc.x = 0

					else:
						x, y = self.cBox.bottomright
						tl = tls[y-1-4,x]
						pg.draw.rect(self._BCKGND, (255,0,0), (x-self._cam.x,y-1-4-self._cam.y,1,1))

						if tl.form == RECT:
							self.cBox.right = tl.rect.left
							self.pos.x = self.cBox.x - self._cBoxOffsetH
							self.vel.x = 0
							self.acc.x = 0

				elif self.vel.x < 0 or (not self._facingRight and self.acc.x == -H_ACC):
					x, y = self.cBox.topleft
					tl = tls[y+4,x-1]
					pg.draw.rect(self._BCKGND, (255,0,0), (x-1-self._cam.x,y+4-self._cam.y,1,1))

					if tl.form == RECT:
						self.cBox.left = tl.rect.right
						self.pos.x = self.cBox.x - self._cBoxOffsetH
						self.vel.x = 0
						self.acc.x = 0

					else:
						x, y = self.cBox.bottomleft
						tl = tls[y-1-4,x-1]
						pg.draw.rect(self._BCKGND, (255,0,0), (x-1-self._cam.x,y-1-4-self._cam.y,1,1))

						if tl.form == RECT:
							self.cBox.left = tl.rect.right
							self.pos.x = self.cBox.x - self._cBoxOffsetH
							self.vel.x = 0
							self.acc.x = 0


		obj.physic.ObjPhysic.updateY(self)

		pg.draw.rect(self._BCKGND, (0,0,255), self.cBox.move(-self._cam.x,-self._cam.y), 1)

		if self.vel.y != 0 or self.acc.y == V_ACC or self.acc.y == -V_ACC:
			for tls in obj.getGroup(TileCollision):
				if self.vel.y > 0:
					x, y = self.cBox.bottomright
					tl = tls[y,x-1]
					pg.draw.rect(self._BCKGND, (255,0,0), (x-1-self._cam.x,y-self._cam.y,1,1))

					if tl.form == RECT:
						self.cBox.bottom = tl.rect.top
						self.pos.y = self.cBox.y - self._cBoxOffsetV
						self.vel.y = 0
						self.acc.y = 0
						self._inGround = True

					else:
						x, y = self.cBox.bottomleft
						tl = tls[y,x]
						pg.draw.rect(self._BCKGND, (255,0,0), (x-self._cam.x,y-self._cam.y,1,1))

						if tl.form == RECT:
							self.cBox.bottom = tl.rect.top
							self.pos.y = self.cBox.y - self._cBoxOffsetV
							self.vel.y = 0
							self.acc.y = 0
							self._inGround = True

				elif self.vel.y < 0:
					x, y = self.cBox.topright
					tl = tls[y-1,x-1]
					pg.draw.rect(self._BCKGND, (255,0,0), (x-1-self._cam.x,y-1-self._cam.y,1,1))

					if tl.form == RECT:
						self.cBox.top = tl.rect.bottom
						self.pos.y = self.cBox.y - self._cBoxOffsetV
						self.vel.y = 0

					else:
						x, y = self.cBox.topleft
						tl = tls[y-1,x]
						pg.draw.rect(self._BCKGND, (255,0,0), (x-self._cam.x,y-1-self._cam.y,1,1))

						if tl.form == RECT:
							self.cBox.top = tl.rect.bottom
							self.pos.y = self.cBox.y - self._cBoxOffsetV
							self.vel.y = 0			


		self._cam.center = self.cBox.center

		if self._inGround:
			if self._facingRight:
				if self.vel.x == 0 and self.acc.x == 0:
					if self.anim != ANIMS["standRight"]:
						self.anim = ANIMS["standRight"]
				else:
					if self.anim != ANIMS["runRight"]:
						self.anim = ANIMS["runRight"]
			else:
				if self.vel.x == 0 and self.acc.x == 0:
					if self.anim != ANIMS["standLeft"]:
						self.anim = ANIMS["standLeft"]
				else:
					if self.anim != ANIMS["runLeft"]:
						self.anim = ANIMS["runLeft"]

		elif self.vel.y != 0 or self.acc.y == V_ACC or self.acc.y == -V_ACC: 
			if self._facingRight:
				if self.anim != ANIMS["jumpRight"]:
					self.anim = ANIMS["jumpRight"]
			else:
				if self.anim != ANIMS["jumpLeft"]:
					self.anim = ANIMS["jumpLeft"]


	def draw(self):
		obj.sprite.ObjAnim.draw(self)
		obj.physic.ObjPhysic.draw(self)
		obj.ObjDraw.draw(self)		


	def save(self):
		self._save(
			controlHash=hash(self._control),
			sprtShtHash=hash(self._sprtSht),
			camHash=hash(self._cam),
			x=self.cBox.x,
			y=self.cBox.y
		)

	def close(self):
		self.save()
		self._sprtSht.leave()


try:
	obj.getGroup(Player)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Player))




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

