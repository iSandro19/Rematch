import obj
import pygame as pg
from game.image import Surface
from game.cam import Cam
from game.player import Player
import math as m

MAX_FRM = 64
AMP_ANIM = 3

class PowerUp(obj.ObjStaticRW, obj.physic.ObjRelative, obj.ObjUpdate):
	GRP_FILE = "game/data/power_ups.json"
	DRAW_LAYER = 10
	UPDT_POS = 2

	def __init__(self, HASH, FATHR_HASH, surfHash, camHash, x, y, name, obtained):

		if not obtained:
			try:
				self._surf = obj.getGroup(Surface)[surfHash]
				self._surf.watch()
			except obj.ObjNotFoundError:
				self._surf = obj.load(Surface, surfHash, HASH)

			self._cam = obj.getGroup(Cam)[camHash]


			obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
			obj.physic.ObjRelative.__init__(
				self,
				HASH,
				FATHR_HASH,
				self._surf.image,
				self._surf.image.get_width(),
				self._surf.image.get_height(),
				self._cam,
				pg.math.Vector2(x, y)
			)

			self._x = x
			self._y = y
			self._name = name
			self._obtained = obtained

			self.beat = True

			self._frmCnt = 0
			self.powerup_sound = pg.mixer.Sound('game/sounds/powerup.ogg')

	def update(self):
		for player in obj.getGroup(Player):
			if player.hitBox.colliderect((self.pos, (self.rect.w, self.rect.h))):
				player.setPowerUp(self._name)
				self._obtained = True
				self.powerup_sound.play()
				self.save()
				self.close()


	def draw(self):
		self.pos.y = self._y + round(AMP_ANIM*m.sin(self._frmCnt*m.pi*2/MAX_FRM))

		obj.physic.ObjRelative.draw(self)
		obj.ObjDraw.draw(self)

		if self._frmCnt < MAX_FRM:
			self._frmCnt += 1

		else:
			self._frmCnt = 0

	def save(self):
		self._save(
			surfHash=hash(self._surf),
			camHash=hash(self._cam),
			x=self._x,
			y=self._y,
			name=self._name,
			obtained=self._obtained
		)

	def close(self):
		self._surf.leave()
		obj.Obj.close(self)


	@property
	def active(self):
		return self._active

	@active.setter
	def active(self, value):
		self._active = value and self.beat


try:
	obj.getGroup(PowerUp)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(PowerUp))
