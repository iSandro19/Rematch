from obj.base import ObjDraw, ObjUpdate
import pygame as pg
from pygame.locals import *
from abc import abstractmethod


class SpriteSheet:
	def __init__(self, SHEET, w, h, colorkey=None):
		self.SHEET = SHEET
		self.SHEET.set_colorkey(colorkey)
		self.clip = pg.Rect(0, 0, w, h)

	def __getitem__(self, rowXcol)->pg.Surface:
		self.clip.x = rowXcol[1]*self.clip.w
		self.clip.y = rowXcol[0]*self.clip.h

		return self.SHEET.subsurface(self.clip)

class ObjSprite(ObjDraw):
	@abstractmethod
	def __init__(self, INST_ID, SPRTS, row, col, x, y):
		self.SPRTS = SPRTS
		ObjDraw.__init__(
			self,
			INST_ID,
			SPRTS[row, col],
			pg.Rect(x, y, SPRTS.clip.w, SPRTS.clip.h)
		)


class Frame:
	def __init__(
		self,
		COL,
		ROW, 
		DUR = 0.,
		FLIP_X = False,
		FLIP_Y = False
	):
		self.COL = COL
		self.ROW = ROW
		self.DUR = DUR
		self.FLIP_X = FLIP_X
		self.FLIP_Y = FLIP_Y

class Animation(tuple):
	def __new__(
		cls,
		FRAMES,
		LOOP=True
	):
		return tuple.__new__(cls, tuple(FRAMES))

	def __init__(
		self,
		FRAMES,
		LOOP=True
	):
		self.LOOP = LOOP

class ObjAnim(ObjDraw, ObjUpdate):
	speed = 1.
	done = False

	@abstractmethod
	def __init__(self, INST_ID, SPRTS, x, y):
		self.SPRTS = SPRTS
		ObjDraw.__init__(
			self,
			INST_ID,
			None,
			pg.Rect(x, y, SPRTS.clip.w, SPRTS.clip.h)
		)

	def startAnim(self, anim):
		self._anim = anim
		self._frameIt = iter(anim)
		self._steps = 0.
		self._frame = next(self._frameIt)
		self.done = False

	def update(self):
		if not self.done:
			try:
				if self._steps < self._frame.DUR:
					self._steps += self.speed
				else:
					self._steps = 0.
					self._frame = next(self._frameIt)		
			except StopIteration:
				if self._anim.LOOP:
					self._frameIt = iter(self._anim)
					self._steps = 0.
					self._frame = next(self._frameIt)
				else:
					self.done = True

			self.image = self.SPRTS[self._frame.ROW, self._frame.COL]

			if self._frame.FLIP_X or self._frame.FLIP_Y:
				self.image = pg.transform.flip(
					self.image,
					self._frame.FLIP_X,
					self._frame.FLIP_Y
				)

class ObjRelative(ObjDraw, ObjUpdate):
	@abstractmethod
	def __init__(self, INST_ID, image, rect):
		ObjDraw.__init__(self, INST_ID, image, rect)

	def update(self):
		self.rect.x = self.pos.x - self.REF_POINT.x
		self.rect.y = self.pos.y - self.REF_POINT.y

class ObjParallax(ObjRelative):
	@abstractmethod
	def __init__(self, INST_ID, image, rect, Z_OFFSET):
		ObjRelative.__init__(self, INST_ID, image, rect)
		self.Z_OFFSET = Z_OFFSET

	def update(self):
		self.rect.x = self.pos.x - self.REF_POINT.x*self.Z_OFFSET
		self.rect.y = self.pos.y - self.REF_POINT.y*self.Z_OFFSET