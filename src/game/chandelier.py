import obj
from game.player import Player
from game.image import Surface, SpriteSheet
from game.cam import Cam
import pygame as pg

CH_ANIM = {
	"fire": obj.sprite.Animation(
		(
			obj.sprite.Frame(0,0,True,DUR=4),
			obj.sprite.Frame(1,0,True,DUR=4),
			obj.sprite.Frame(2,0,True,DUR=4),
		)
	)
}

class Chandelier(obj.ObjStaticR, obj.sprite.ObjAnim, obj.physic.ObjRelative):
	GRP_FILE = "game/data/chandeliers.json"
	DRAW_LAYER = 7

	def __init__(self, HASH, FATHR_HASH, sprtShtHash, camHash, x, y):
		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet, sprtShtHash, HASH)

		self._cam = obj.getGroup(Cam)[camHash]

		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		
		obj.sprite.ObjAnim.__init__(self, HASH, FATHR_HASH, self._sprtSht, 0, 0)
	
		obj.physic.ObjRelative.__init__(
			self, hash(self), FATHR_HASH, None, self._sprtSht.clip.w,
			self._sprtSht.clip.h, self._cam, pg.math.Vector2(x, y)
		)
	
		self.anim = CH_ANIM["fire"]

	def update(self):
		pass

	def draw(self):
		obj.sprite.ObjAnim.draw(self)
		obj.physic.ObjRelative.draw(self)
		obj.ObjDraw.draw(self)

	def close(self):
		self._sprtSht.leave()
		obj.Obj.close(self)

try:
	obj.getGroup(Chandelier)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Chandelier))