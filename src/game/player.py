import obj
import pygame as pg
from random import randint
from game.cam import Cam
from game.image import SpriteSheet
from game.control import Control
from game.tile import TileCollision, RECT
from game.alive import ObjAlive
from game.stand import StandFriend
from game.interact import BreakBlock

ANIMS = {
	"standRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,DUR=16),
			obj.sprite.Frame(1,0,DUR=16),
			obj.sprite.Frame(2,0,DUR=16),
			obj.sprite.Frame(1,0,DUR=16),
		),
	),
	"standLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,True,DUR=16),
			obj.sprite.Frame(1,0,True,DUR=16),
			obj.sprite.Frame(2,0,True,DUR=16),
			obj.sprite.Frame(1,0,True,DUR=16),
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
			obj.sprite.Frame(8,1,DUR=4),
			obj.sprite.Frame(9,1,DUR=4)
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
			obj.sprite.Frame(8,1,True,DUR=4),
			obj.sprite.Frame(9,1,True,DUR=4),
		)
	),
	"jumpRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,2,DUR=1),
			obj.sprite.Frame(1,2,DUR=1),
		)
	),
	"stopJumpRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(2,2),
		),
		False
	),
	"fallRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(3,2,DUR=1),
			obj.sprite.Frame(4,2,DUR=1),
		)
	),
	"groundingRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,3,DUR=4),
			obj.sprite.Frame(1,3,DUR=4),
			obj.sprite.Frame(2,3,DUR=4),
			obj.sprite.Frame(3,3,DUR=4)
		),
		False
	),
	"jumpLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,2,True,DUR=1),
			obj.sprite.Frame(1,2,True,DUR=1)
		)
	),
	"stopJumpLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(2,2,True),
		),
		False
	),
	"fallLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(3,2,True,DUR=1),
			obj.sprite.Frame(4,2,True,DUR=1),
		)
	),
	"groundingLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,3,True,DUR=4),
			obj.sprite.Frame(1,3,True,DUR=4),
			obj.sprite.Frame(2,3,True,DUR=4),
			obj.sprite.Frame(3,3,True,DUR=4)
		),
		False
	)
}

C_BOX_W = 16
C_BOX_H = 32

C_BOX_W_OFFSET = 12
C_BOX_H_OFFSET = 8

IMG_W = 40
IMG_H = 40

MAX_H_VEL = 2
MAX_V_VEL = 2

MAX_H_WJ_VEL = 2
MAX_V_WJ_VEL = 2

H_ACC = 0.2
V_ACC = 0.2

JUMP_VEL = 5

HIT_OFFSET_H = 12
HIT_OFFSET_W = 8
HIT_BOX_W = 16
HIT_BOX_H = 32

HIT_INVUL_TIME = 64

life = 4
maxLife = 4
LIFE_REGEN_TIME = 256

STAND_OFFSET_H = 10
STAND_OFFSET_V = 34

ATTACK_COOLDOWN = 32
STAND_SPRITE_SHEET_HASH = 11


class Player(obj.physic.ObjPhysic, obj.ObjStaticRW, obj.sprite.ObjAnim, ObjAlive): 
	GRP_FILE = "game/data/players.json"
	UPDT_POS = 1
	DRAW_LAYER = 9

	def __init__(
		self,
		HASH,
		FATHR_HASH,
		sprtShtHash,
		camHash,
		x,
		y,
		powerUps
	):

		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet, sprtShtHash, HASH)

		self._cam = obj.getGroup(Cam)[camHash]

		obj.state.ObjState.__init__(self, HASH, FATHR_HASH)
		ObjAlive.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			IMG_W,
			IMG_H,
			self._cam,
			pg.math.Vector2(x, y),
			life,
			maxLife,
			HIT_OFFSET_H,
			HIT_OFFSET_W,
			HIT_BOX_W,
			HIT_BOX_H
		)
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
		#self._inWall = False

		self.counter = 0
		self.dashing = False
		self.attackCnt = 0

		self.attackedCnt = 0
		self.regenCnt = 0

		self._ui = UI(0, self.life, self.maxLife)

		self.stand = None
		
		self.jump1_sound = pg.mixer.Sound('game/sounds/jump_1.ogg')
		self.jump2_sound = pg.mixer.Sound('game/sounds/jump_2.ogg')
		self.damage1_sound = pg.mixer.Sound('game/sounds/damage1.ogg')
		self.damage2_sound = pg.mixer.Sound('game/sounds/damage2.ogg')
		self.damage3_sound = pg.mixer.Sound('game/sounds/damage3.ogg')
		self.ataque_normal_sound = pg.mixer.Sound('game/sounds/ataque_normal.ogg')
		self.ataque_giratorio_sound = pg.mixer.Sound('game/sounds/ataque_giratorio.ogg')
		self.dash1_sound = pg.mixer.Sound('game/sounds/dash1.ogg')
		self.dash2_sound = pg.mixer.Sound('game/sounds/dash2.ogg')

		self.powerUps = powerUps
		self._x = x
		self._y = y

	def teleport(self, x, y):
		self.pos.x = x
		self.pos.y = y

		self.vel.x = 0
		self.vel.y = 0

		self.acc.x = 0
		self.acc.y = 0

		self._facingRight = True
		self.doubleJump = True
		self.anim = ANIMS["standRight"]

		self.counter = 0
		self.dashing = False
		self.attackCnt = 0

		self.attackedCnt = 0
		self.regenCnt = 0


	def attack(self, dmg):
		if not self.dashing and self.attackedCnt == 0:
			self.regenCnt = 0
			self.life -= dmg
			self.attackedCnt = HIT_INVUL_TIME
			self._ui.updateLife(self.life)

			rand = randint(1,3)

			if rand == 1:
				self.damage1_sound.play()
			elif rand==2:
				self.damage2_sound.play()
			else:
				self.damage3_sound.play()

	# Función para detectar si el jugador está en el suelo o no y actualizar su valor
	def isInGround(self):
		for tls in obj.getGroup(TileCollision):

			# Primero miramos a la derecha, si no hay nada a la izquierda y si no, pues no está en el suelo

			x, y = self.cBox.bottomright
			tl = tls[y,x-1]	# pygame, en los bottom, devuelve el punto externo (xd)

			if tl.form == RECT:		# Si no existe un tile abajo, la forma es void.
				#self._inGround = True
				return True

			x, y = self.cBox.bottomleft
			tl = tls[y,x]

			if tl.form == RECT:
				#self._inGround = True
				return True

		for bb in obj.getGroup(BreakBlock):
			if bb.hitBox.colliderect(self.cBox.move(0, 1)):
				return True

		return False
	
	def isInWall(self):
		for tls in obj.getGroup(TileCollision):
			# Colisión horizontal por la izquierda
			if not self._facingRight:
				xTL, yTL = self.cBox.topleft
				tlTL = tls[yTL,xTL-1]

				if tlTL.form == RECT:
					return True
					
				else:
					xCL, yCL = self.cBox.midleft
					tlCL = tls[yCL, xCL-1]

					if tlCL.form == RECT:
						return True
							

			# Colisión horizontal por la derecha
			else:
				xTR, yTR = self.cBox.topright
				tlTR = tls[yTR,xTR]

				if tlTR.form == RECT:
					return True
				else:
					xCR, yCR = self.cBox.midright
					tlCR = tls[yCR, xCR]

					if tlCR.form == RECT:
						return True

		for bb in obj.getGroup(BreakBlock):
			if (
				bb.hitBox.colliderect(
					self.cBox.move(
						-1 if self._facingRight else 1,
						0
					)
				)
			):
				return True

		return False


	def jump(self):
		if self.powerUps["peon"]:
			if self.isInGround():
				self._inGround = False
				self.acc.y = V_ACC
				self.vel.y = -JUMP_VEL
				self.jump1_sound.play()

			elif self.powerUps["alfil"] and self.isInWall() and self._facingRight:
				self.acc.y = V_ACC
				self.vel.y = -JUMP_VEL
				self.vel.x = -MAX_H_VEL*1.1
				self.jump1_sound.play()
			
			elif self.powerUps["alfil"] and self.isInWall() and (not self._facingRight):
				self.acc.y = V_ACC
				self.vel.y = -JUMP_VEL
				self.vel.x = MAX_H_VEL*1.1
				self.jump1_sound.play()
				
			elif self.powerUps["caballo"] and self.doubleJump:
				self.acc.y = V_ACC
				self.vel.y = -JUMP_VEL
				self.doubleJump = False
				self.jump2_sound.play()
		
			
	
	def fall(self):	
		if self.vel.y < 0:
			self.vel.y = 0


	def stopMove(self):
		# Condición necesaria para poder separarse de la pared si estar pulsando ningún botón, se le delega el frenado a las físicas
		if (not self.isInWall()):
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

	# Inicia la acción de dasheo e inicia el contador
	def dash(self):
		if self.powerUps["torre"]:
			if self.dashing == False:
				self.dashing = True
				self.counter = 30

				if self._facingRight:
					self.stand = StandFriend(hash(self), STAND_SPRITE_SHEET_HASH, "lanceRight", self.pos.x-STAND_OFFSET_H, self.pos.y-STAND_OFFSET_V)
				else:
					self.stand = StandFriend(hash(self), STAND_SPRITE_SHEET_HASH, "lanceLeft", self.pos.x-IMG_W+STAND_OFFSET_H, self.pos.y-STAND_OFFSET_V)


				rand = randint(1,2)

				if rand == 1:
					self.dash1_sound.play()
				else:
					self.dash2_sound.play()


	# Se puede dashear cada 30 fps y solo una vez mientras estés en el aire
	def dodash(self):
		if self.powerUps["torre"]:
			if self.counter > 0:
				# Aumentar velocidad
				if (self.vel.x > 0) & (self._facingRight) & (self.counter > 20):
					self.vel.x  += H_ACC*2.5
					self.vel.y = 0
				elif (self.vel.x < 0) & (not self._facingRight) & (self.counter > 20):
					self.vel.x  -= H_ACC*2.5
					self.vel.y = 0

				# Frenar el dash
				elif (self.counter > 15) & (self.vel.x > 2.2):
					self.vel.x -= H_ACC * 5
					self.vel.y = 0
				elif (self.counter > 15) & (self.vel.x < -2.2):
					self.vel.x += H_ACC * 5
					self.vel.y = 0

				# Durante este tiempo, la velocida vertical no varía
				
				# Asegurarse de seguir a la maxima velocidad usual
				elif (self.counter < 15) & (self.vel.x != 2.2) & (self.vel.x > 0):
					self.vel.x = 2.2
				elif (self.counter < 15) & (self.vel.x != -2.2) & (self.vel.x < 0):
					self.vel.x = -2.2

				self.counter -= 1

			elif self.isInGround() or self.isInWall(): 
				self.dashing = False
			
	def basic_attack(self):
		if self.powerUps["peon"]:
			if self.attackCnt == 0:
				if self._facingRight:
					self.stand = StandFriend(hash(self), STAND_SPRITE_SHEET_HASH, "basicRight", self.pos.x-STAND_OFFSET_H, self.pos.y-STAND_OFFSET_V)
				else:
					self.stand = StandFriend(hash(self), STAND_SPRITE_SHEET_HASH, "basicLeft", self.pos.x-IMG_W+STAND_OFFSET_H, self.pos.y-STAND_OFFSET_V)

				self.ataque_normal_sound.play()
				self.attackCnt = ATTACK_COOLDOWN

	def rotatory_attack(self):
		if self.powerUps["alfil"]:
			if self.attackCnt == 0:
				if self._facingRight:
					self.stand = StandFriend(hash(self), STAND_SPRITE_SHEET_HASH, "rotatoryRight", self.pos.x-STAND_OFFSET_H, self.pos.y-STAND_OFFSET_V)
				else:
					self.stand = StandFriend(hash(self), STAND_SPRITE_SHEET_HASH, "rotatoryLeft", self.pos.x-IMG_W+STAND_OFFSET_H, self.pos.y-STAND_OFFSET_V)

				self.attackCnt = ATTACK_COOLDOWN
				self.ataque_giratorio_sound.play()

	@property
	def active(self):
		return self._active

	@active.setter
	def active(self, value):
		if self.stand:
			self.stand.active = value

		self._active = value
	

	def update(self):
		if self.attackCnt != 0:
			self.attackCnt -= 1

		if self.life < self.maxLife:
			if self.regenCnt < LIFE_REGEN_TIME:
				self.regenCnt += 1
			else:
				self.regenCnt = 0
				self.life += 1
				self._ui.updateLife(self.life)


		# Controlar el dash
		if self.dashing: 
			self.dodash()

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


		for bb in obj.getGroup(BreakBlock):
			if self.vel.x < 0:
				if bb.hitBox.colliderect(self.cBox):
					cBox.left = bb.hitBox.right

			elif self.vel.x > 0:
				if bb.hitBox.colliderect(self.cBox):
					cBox.right = bb.hitBox.left

		self.cBox = cBox

		# Velocidad máxima de caída
		if self.vel.y > 6: self.vel.y = 6

		# Físicas en pared
		if self.isInWall() and (not self.isInGround()) and (self.vel.y > 0):
			self.vel.y = 1
			self.doubleJump = True

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


		for bb in obj.getGroup(BreakBlock):
			if self.vel.y < 0:
				if bb.hitBox.colliderect(self.cBox):
					cBox.top = bb.hitBox.bottom

			elif self.vel.y > 0:
				if bb.hitBox.colliderect(self.cBox):
					cBox.bottom = bb.hitBox.top

		self.cBox = cBox

		if self.isInGround():
			self.doubleJump = True

		self._cam.center = self.cBox.center
		self._cam.correctPos()

		if self.stand and self.dashing:
			if self.stand.active:
				if self._facingRight:
					self.stand.pos.x = self.pos.x-STAND_OFFSET_H
					self.stand.pos.y = self.pos.y-STAND_OFFSET_V

				else:
					self.stand.pos.x = self.pos.x-IMG_W+STAND_OFFSET_H
					self.stand.pos.y = self.pos.y-STAND_OFFSET_V
			else:
				self.stand = None


	def draw(self):
		if self.isInGround():
			if self._facingRight:
				if self.vel.x == 0 and self.acc.x == 0:
					if (
						self.anim == ANIMS["fallRight"] or 
						self.anim == ANIMS["stopJumpRight"]
					):
						self.anim = ANIMS["groundingRight"]

					elif (
						self.anim == ANIMS["groundingRight"] and self.done or
						self.anim == ANIMS["runRight"]
					):
						self.anim = ANIMS["standRight"]
				else:
					if self.anim != ANIMS["runRight"]:
						self.anim = ANIMS["runRight"]
			else:
				if self.vel.x == 0 and self.acc.x == 0:
					if (
						self.anim == ANIMS["fallLeft"] or 
						self.anim == ANIMS["stopJumpLeft"]
					):
						self.anim = ANIMS["groundingLeft"]

					if (
						self.anim == ANIMS["groundingLeft"] and self.done or
						self.anim == ANIMS["runLeft"]
					):
						self.anim = ANIMS["standLeft"]
				else:
					if self.anim != ANIMS["runLeft"]:
						self.anim = ANIMS["runLeft"]

		else:
			if self.vel.y < 0:
				if self._facingRight:
					if self.anim != ANIMS["jumpRight"]:
						self.anim = ANIMS["jumpRight"]
				else:
					if self.anim != ANIMS["jumpLeft"]:
						self.anim = ANIMS["jumpLeft"]

			elif self.vel.y > 2:
				if self._facingRight:
					if self.anim != ANIMS["fallRight"]:
						self.anim = ANIMS["fallRight"]
				else:
					if self.anim != ANIMS["fallLeft"]:
						self.anim = ANIMS["fallLeft"]

			else:
				if self._facingRight:
					if self.anim != ANIMS["stopJumpRight"]:
						self.anim = ANIMS["stopJumpRight"]
				else:
					if self.anim != ANIMS["stopJumpLeft"]:
						self.anim = ANIMS["stopJumpLeft"]

		obj.sprite.ObjAnim.draw(self)
		obj.physic.ObjPhysic.draw(self)

		if self.attackedCnt != 0:
			self.image.set_alpha(255 if self.attackedCnt%4 >= 2 else 0)
			self.attackedCnt -= 1

		obj.ObjDraw.draw(self)		


	def save(self):
		self._save(
			sprtShtHash=hash(self._sprtSht),
			camHash=hash(self._cam),
			x=self._x,
			y=self._y,
			powerUps=self.powerUps
		)

	def close(self):
		self.save()

		if self.stand and self.stand.active:
			self.stand.close()

		self._sprtSht.leave()
		self._ui.close()
		obj.Obj.close(self)

	def setPowerUp(self, name):
		self.powerUps[name] = True

try:
	obj.getGroup(Player)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Player))


LIFE_POINT_SPRITE_SHEET_HASH = 9

class LifePoint(obj.ObjDynamic, obj.sprite.ObjSprite):
	DRAW_LAYER = 20

	def __init__(self, FATHR_HASH, number):

		obj.ObjDynamic.__init__(self, FATHR_HASH)
		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[LIFE_POINT_SPRITE_SHEET_HASH]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet, LIFE_POINT_SPRITE_SHEET_HASH, hash(self))

		obj.sprite.ObjSprite.__init__(self, hash(self), FATHR_HASH, self._sprtSht, self._sprtSht.clip.w*(number-1), 0)

		self._number = number
		self.frame = obj.sprite.Frame(0,0)

		self.regen = False
		self.blinkCnt = 0


	def updateLife(self, life):
		if life < self._number:
			self.frame = obj.sprite.Frame(1,0)
			self.regen = life+1 == self._number
			self.blinkCnt = 16
		else:
			self.frame = obj.sprite.Frame(0,0)
			self.regen = False

	def draw(self):
		if self.regen:
			if self.blinkCnt != 0:
				self.frame = obj.sprite.Frame(0,0) if self.blinkCnt >= 8 else obj.sprite.Frame(1,0)
				self.blinkCnt -= 1
			else:
				self.blinkCnt = 16

		obj.sprite.ObjSprite.draw(self)

try:
	obj.getGroup(LifePoint)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(LifePoint))


def _newLifePoint(number):
	return LifePoint(0, number)

class UI(obj.ObjDynamic):
	def __init__(self, FATHR_HASH, life, maxLife):
		obj.ObjDynamic.__init__(self, FATHR_HASH)

		self._lifePoints = tuple(map(_newLifePoint, range(1, maxLife+1)))

		self.updateLife(life)

	def updateLife(self, life):
		for lp in self._lifePoints:
			lp.updateLife(life)

	def close(self):
		for lp in self._lifePoints:
			lp.close()

		obj.Obj.close(self)

try:
	obj.getGroup(UI)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(UI))
