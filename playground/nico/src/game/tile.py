import obj
from game.image import SpriteSheet
from game.cam import Cam
import pygame as pg
import csrmat

class TileMap(obj.ObjStaticR, obj.physic.ObjRelative):
	DRAW_LAYER = 0
	GRP_FILE = "game/data/tile_maps.json"
	
	def __init__(
		self,
		HASH,
		FATHR_HASH,
		camHash,
		sprtShtHash,
		rowOffset,
		colOffset,
		csrMat
		):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)

		self._cam = obj.getGroup(Cam)[camHash]
		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet,sprtShtHash, HASH)

		self._rowOffset = rowOffset
		self._colOffset = colOffset
		self._csrMat = csrmat.CSRMat(csrMat, ())


		obj.physic.ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			self._sprtSht.clip.copy(),
			self._cam,
			self._sprtSht.clip.copy()
		)

	def draw(self):

		


		esqSup = self._cam.y//self.rect.h - self.rowOffset
		esqInf = esqSup + self._cam.h//self.rect.h

		esqIzq = self._cam.x//self.rect.w - self.colOffset
		esqDer = esqIzq + self._cam.w//self.rect.w


		for row in range(esqSup, esqInf):
			for col, tile in self._csrMat[row]:
				self.pos.x = col*self.pos.w
				self.pos.y = row*self.pos.h
				obj.ObjRelative.draw(self)


try:
	obj.getGroup(TileMap)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(TileMap))
