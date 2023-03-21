import obj
from game.player import Player
from game.image import Surface
from game.cam import Cam
import pygame as pg


class CollideTP(obj.ObjStaticR, obj.ObjUpdate):
	GRP_FILE = "game/data/collide_tps.json"
	UPDT_POS = 0

	def __init__(self, HASH, FATHR_HASH, triggerRect, destX, destY):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)

		self._triggerRect = triggerRect
		self._destX = destX
		self._destY = destY


	def update(self):
		for player in obj.getGroup("Player"):
			if player.hitBox.colliderect(self._triggerRect):
				player.teleport(self._destX, self._destY)

try:
	obj.getGroup(CollideTP)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(CollideTP))


SMALL_DOOR_SURF_HASH = 12

class SmallDoor(obj.ObjStaticR, obj.physic.ObjRelative):
	GRP_FILE = "game/data/small_doors.json"
	DRAW_LAYER = 7

	def __init__(self, HASH, FATHR_HASH, camHash, srcX, srcY, destX, destY):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)

		try:
			self._surf = obj.getGroup(Surface)[SMALL_DOOR_SURF_HASH]
			self._surf.watch()
		except obj.ObjNotFoundError:
			self._surf = obj.load(Surface, SMALL_DOOR_SURF_HASH, hash(self))

		self._cam = obj.getGroup(Cam)[camHash]

		_, _, w, h = self._surf.image.get_rect()

		obj.physic.ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			self._surf.image,
			w,
			h,
			self._cam,
			pg.math.Vector2(srcX, srcY)
		)
		self._destX = destX
		self._destY = destY

	def doTPifInDoor(self):
		for player in obj.getGroup("Player"):
			if player.hitBox.colliderect([self.pos.x, self.pos.y, self.rect.w, self.rect.h]):
				player.teleport(self._destX, self._destY)

	def draw(self):
		obj.physic.ObjRelative.draw(self)
		obj.ObjDraw.draw(self)

	def close(self):
		self._surf.leave()
		obj.Obj.close(self)

try:
	obj.getGroup(SmallDoor)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(SmallDoor))
