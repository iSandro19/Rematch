import obj
import pygame as pg
from game.image import SpriteSheet
from game.cam import Cam
from game.enemy import Peon, Caballo, Alfil, Torre
from abc import abstractmethod
from game.interact import BreakBlock

CAM_HASH = 0

ANIMS = {
	"basicRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,DUR=2),
			obj.sprite.Frame(1,0,DUR=2),
			obj.sprite.Frame(2,0,DUR=8),
			obj.sprite.Frame(3,0,DUR=4),
			obj.sprite.Frame(4,0,DUR=4)
		),
		False
	),
	"basicLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,True,DUR=2),
			obj.sprite.Frame(1,0,True,DUR=2),
			obj.sprite.Frame(2,0,True,DUR=8),
			obj.sprite.Frame(3,0,True,DUR=4),
			obj.sprite.Frame(4,0,True,DUR=4)
		),
		False
	),
	"rotatoryRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,1,DUR=2),
			obj.sprite.Frame(1,1,DUR=2),
			obj.sprite.Frame(2,1,DUR=2),
			obj.sprite.Frame(3,1,DUR=2),
			obj.sprite.Frame(4,1,DUR=2),
			obj.sprite.Frame(1,1,DUR=2),
			obj.sprite.Frame(2,1,DUR=2),
			obj.sprite.Frame(3,1,DUR=2),
			obj.sprite.Frame(4,1,DUR=2),
			obj.sprite.Frame(5,1,DUR=2),
			obj.sprite.Frame(3,0,DUR=4),
			obj.sprite.Frame(4,0,DUR=4)
		),
		False
	),
	"rotatoryLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,1,True,DUR=2),
			obj.sprite.Frame(1,1,True,DUR=2),
			obj.sprite.Frame(2,1,True,DUR=2),
			obj.sprite.Frame(3,1,True,DUR=2),
			obj.sprite.Frame(4,1,True,DUR=2),
			obj.sprite.Frame(1,1,True,DUR=2),
			obj.sprite.Frame(2,1,True,DUR=2),
			obj.sprite.Frame(3,1,True,DUR=2),
			obj.sprite.Frame(4,1,True,DUR=2),
			obj.sprite.Frame(5,1,True,DUR=2),
			obj.sprite.Frame(3,0,True,DUR=4),
			obj.sprite.Frame(4,0,True,DUR=4)
		),
		False
	),
	"lanceRight": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,2,DUR=2),
			obj.sprite.Frame(1,2,DUR=2),
			obj.sprite.Frame(2,2,DUR=4),
			obj.sprite.Frame(3,2,DUR=4),
			obj.sprite.Frame(3,0,DUR=4),
			obj.sprite.Frame(4,0,DUR=4)
		),
		False
	),
	"lanceLeft": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,2,True,DUR=2),
			obj.sprite.Frame(1,2,True,DUR=2),
			obj.sprite.Frame(2,2,True,DUR=4),
			obj.sprite.Frame(3,2,True,DUR=4),
			obj.sprite.Frame(3,0,True,DUR=4),
			obj.sprite.Frame(4,0,True,DUR=4)
		),
		False
	)
}

HITBOX = {
	"basicRight": pg.Rect(40,40,33,33),
	"basicLeft": pg.Rect(7,40,33,33),
	"rotatoryRight": pg.Rect(27,30,49,49),
	"rotatoryLeft": pg.Rect(5,30,49,49),
	"lanceRight": pg.Rect(40,52,39,7),
	"lanceLeft": pg.Rect(1,52,39,7)
}

DMG = {
	"basicRight": 1,
	"basicLeft": 1,
	"rotatoryRight": 1,
	"rotatoryLeft": 1,
	"lanceRight": 2,
	"lanceLeft": 2

}

class Stand(obj.ObjDynamic, obj.sprite.ObjAnim, obj.physic.ObjRelative, obj.ObjUpdate):
	UPDT_POS = 2
	DRAW_LAYER = 8

	def __init__(self, FATHR_HASH, sprtShtHash, attack, x, y):
		obj.ObjDynamic.__init__(self, FATHR_HASH)

		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet, sprtShtHash, hash(self))

		self._cam = obj.getGroup(Cam)[CAM_HASH]

		
		obj.sprite.ObjAnim.__init__(self, hash(self), FATHR_HASH, self._sprtSht, 0, 0)
		obj.physic.ObjRelative.__init__(
			self, hash(self), FATHR_HASH, None, self._sprtSht.clip.w,
			self._sprtSht.clip.h, self._cam, pg.math.Vector2(x, y)
		)

		self.anim = ANIMS[attack]
		self.attack = attack
		self.frmCnt = 0
		self.alpha = 255

	@abstractmethod
	def doAttack(self):
		pass

	def update(self):
		if not self.done:
			if   self.attack == "basicRight":
				if 2 <= self.frmCnt < 14:
					self.doAttack()

			elif self.attack == "basicLeft":
				if 2 <= self.frmCnt < 14:
					self.doAttack()

			elif self.attack == "rotatoryRight":
				if 2 <= self.frmCnt < 29:
					self.doAttack()

			elif self.attack == "rotatoryLeft":
				if 2 <= self.frmCnt < 29:
					self.doAttack()
				
			elif self.attack == "lanceRight":
				if 2 <= self.frmCnt < 14:
					self.doAttack()
				
			elif self.attack == "lanceLeft":
				if 2 <= self.frmCnt < 14:
					self.doAttack()

			self.frmCnt += 1
		else:
			if self.alpha != 0:
				self.alpha -= 5
			else:
				self.close()


	def draw(self):
		obj.sprite.ObjAnim.draw(self)
		obj.physic.ObjRelative.draw(self)
		self.image.set_alpha(self.alpha)
		obj.ObjDraw.draw(self)

	def close(self):
		try:
			self._sprtSht.leave()
		except ObjNotFoundError:
			pass
		obj.Obj.close(self)


enemyTypes = (Peon, Caballo, Alfil, Torre, "BasicBoss", BreakBlock, "FinalBoss")

class StandFriend(Stand):
	def doAttack(self):
		hitBox = HITBOX[self.attack].move(self.pos)

		for enemyType in enemyTypes:
			for enemy in obj.getGroup(enemyType):
				if enemy.hitBox.colliderect(hitBox):
					enemy.attack(DMG[self.attack])

try:
	obj.getGroup(StandFriend)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(StandFriend))


class StandEnemy(Stand):
	def doAttack(self):
		hitBox = HITBOX[self.attack].move(self.pos)

		for player in obj.getGroup("Player"):
			if player.hitBox.colliderect(hitBox):
				player.attack(DMG[self.attack])

try:
	obj.getGroup(StandEnemy)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(StandEnemy))
