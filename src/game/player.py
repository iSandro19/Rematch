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
		#self._inGround = True
		self._facingRight = True
		self.doubleJump = True


	# Función para detectar si el jugador está en el suelo o no y actualizar su valor
	def isInGround(self):

		for tls in obj.getGroup(TileCollision):

			# Primero miramos a la derecha, si no hay nada a la izquierda y si no, pues no está en el suelo

			x, y = self.cBox.bottomright
			tl = tls[y,x-1]	# pygame, en los bottom, devuelve el punto externo (xd)

			if tl.form == RECT:		# Si no existe un tile abajo, la forma es void.
				#self._inGround = True
				return True

			else:

				x, y = self.cBox.bottomleft
				tl = tls[y,x]

				if tl.form == RECT:
					#self._inGround = True
					return True

				else:
					#self._inGround = False
					return False

			

	def jump(self):

		if self.isInGround():
			#self._inGround = False
			self.acc.y = V_ACC
			self.vel.y = -JUMP_VEL

		elif self.doubleJump:
			self.acc.y = V_ACC
			self.vel.y = -JUMP_VEL
			self.doubleJump = False


	
	def fall(self):	

		if self.vel.y < 0:
			self.vel.y = 0


	def stopMove(self):

		self.vel.x = 0
		self.acc.x = 0

	def moveLeft(self):

		self._facingRight = False

		self.acc.y = V_ACC

		if self.vel.x > -MAX_H_VEL:
			self.acc.x = -H_ACC
		else: 
			self.acc.x = 0
		

	def moveRight(self):

		self._facingRight = True

		self.acc.y = V_ACC

		if self.vel.x < MAX_H_VEL:
			self.acc.x = H_ACC
		else: 
			self.acc.x = 0


	def dash(self):
		a = 1

	def update(self):

		obj.physic.ObjPhysic.updateX(self)


		cBox = self.cBox
		
		for tls in obj.getGroup(TileCollision):
			
			# Colisión horizontal por la izquierda
			if self.vel.x < 0:
				xBL, yBL = self.cBox.bottomleft
				tlBL = tls[yBL-1,xBL-1]

				if tlBL.form == RECT:
					cBox.left = tlBL.rect.right
					self.vel.x = 0
					self.acc.x = 0
				else:

					xTL, yTL = self.cBox.topleft
					tlTL = tls[yTL,xTL-1]

					if tlTL.form == RECT:
						cBox.left = tlBL.rect.right
						self.vel.x = 0
						self.acc.x = 0
					else:

						xCL, yCL = self.cBox.midleft
						tlCL = tls[yCL, xCL-1]

						if tlCL.form == RECT:
							cBox.left = tlBL.rect.right
							self.vel.x = 0
							self.acc.x = 0

			# Colisión horizontal por la derecha
			elif self.vel.x > 0:

				xBR, yBR = self.cBox.bottomright
				tlBR = tls[yBR-1,xBR]

				if tlBR.form == RECT:
					cBox.right = tlBR.rect.left
					self.vel.x = 0
					self.acc.x = 0
				else:

					xTR, yTR = self.cBox.topright
					tlTR = tls[yTR,xTR]

					if tlTR.form == RECT:
						cBox.right = tlBR.rect.left
						self.vel.x = 0
						self.acc.x = 0
					else:

						xCR, yCR = self.cBox.midright
						tlCR = tls[yCR, xCR]

						if tlCR.form == RECT:
							cBox.right = tlBR.rect.left
							self.vel.x = 0
							self.acc.x = 0

		self.cBox = cBox

		obj.physic.ObjPhysic.updateY(self)

		cBox = self.cBox

		# Colisiones verticales

		for tls in obj.getGroup(TileCollision):
	
			if self.vel.y > 0:

				x, y = cBox.bottomright
				tl = tls[y,x-1]	# pygame, en los bottom, devuelve el punto externo (xd)

				if tl.form == RECT:		# Si no existe un tile abajo, la forma es void.
					cBox.bottom = tl.rect.top
					self.vel.y = 0
					self.acc.y = 0

				else:

					x, y = cBox.bottomleft
					tl = tls[y,x]

					if tl.form == RECT:
						cBox.bottom = tl.rect.top
						self.vel.y = 0
						self.acc.y = 0
			
			elif self.vel.y < 0:

				x, y = cBox.topright
				tl = tls[y-1,x-1]	

				if tl.form == RECT:
					cBox.top = tl.rect.bottom
					self.vel.y = 0

				else:

					x, y = cBox.topleft
					tl = tls[y-1,x]

					if tl.form == RECT:
						cBox.top = tl.rect.bottom
						self.vel.y = 0


		self.cBox = cBox

		if self.isInGround():
			self.doubleJump = True

		self._cam.center = self.cBox.center

		if self.isInGround():
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
		#self.save()
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

