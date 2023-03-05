from obj.base import ObjDraw, ObjUpdate
import pygame as pg
from abc import abstractmethod


class ObjRelative(ObjDraw):
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, w, h, REF_POINT, pos):
		ObjDraw.__init__(self, HASH, FATHR_HASH, image, pg.Rect(0,0,w,h))
		self.REF_POINT = REF_POINT
		self.pos = pos

	def draw(self):
		self.rect.x = round(self.pos.x - self.REF_POINT.x)
		self.rect.y = round(self.pos.y - self.REF_POINT.y)

class ObjParallax(ObjDraw):
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, w, h, REF_POINT, pos, Z_OFFSET):
		ObjDraw.__init__(self, HASH, FATHR_HASH, image, pg.Rect(0,0,w,h))
		self.REF_POINT = REF_POINT
		self.pos = pos
		self.Z_OFFSET = Z_OFFSET

	def draw(self):
		self.rect.x = round(self.pos.x - self.REF_POINT.x*self.Z_OFFSET)
		self.rect.y = round(self.pos.y - self.REF_POINT.y*self.Z_OFFSET)

class ObjPhysic(ObjRelative, ObjUpdate):
	@abstractmethod
	def __init__(
		self,
		HASH,
		FATHR_HASH,
		img,
		imgW,
		imgH,
		REF_POINT,
		pos,
		cBoxOffsetH,
		cBoxOffsetV,
		cBoxW,
		cBoxH,
		acc,
		vel
	):
		ObjRelative.__init__(self, HASH, FATHR_HASH, img, imgW, imgH, REF_POINT, pos)
		ObjUpdate.__init__(self, HASH, FATHR_HASH)
		self._cBoxOffsetH = cBoxOffsetH
		self._cBoxOffsetV = cBoxOffsetV
		self.cBox = pg.Rect(pos.x+cBoxOffsetH, pos.y+cBoxOffsetV, cBoxW, cBoxH)
		self.acc = acc
		self.vel = vel

	def update(self):
		self.vel += self.acc
		self.pos += self.vel
		self.cBox.x = round(self.pos.x+self._cBoxOffsetH)
		self.cBox.y = round(self.pos.y+self._cBoxOffsetV)
		