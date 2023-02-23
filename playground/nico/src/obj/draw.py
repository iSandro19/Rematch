from obj.base import ObjDraw
import pygame as pg
from pygame.locals import *
from abc import abstractmethod


class ObjTile(ObjDraw):
	@abstractmethod
	def __init__(self, INST_ID):
		ObjDraw.__init__(self, INST_ID)

	@abstractmethod
	def update(self):
		pass

	def updateImage(self, row, col):
		self.image = self.SPRTS[row, col]


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

class SpriteSheet:
	def __init__(self, SHEET, w, h, colorkey=None):
		self.SHEET = SHEET
		self.SHEET.set_colorkey(colorkey)
		self._clip = pg.Rect(0, 0, w, h)

	def __getitem__(self, rowXcol)->pg.Surface:
		self._clip.x = rowXcol[1]*self._clip.w
		self._clip.y = rowXcol[0]*self._clip.h

		return self.SHEET.subsurface(self._clip)

class ObjAnim(ObjDraw):
	speed = 1.
	done = False

	@abstractmethod
	def __init__(self, INST_ID):
		ObjDraw.__init__(self, INST_ID)

	@abstractmethod
	def update(self):
		pass

	def startAnim(self, anim):
		self._anim = anim
		self._frameIt = iter(anim)
		self._steps = 0.
		self._frame = next(self._frameIt)
		self.done = False

	def updateImage(self):
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
