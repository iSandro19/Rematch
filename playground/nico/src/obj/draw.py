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


class Frame:
	def __init__(
		self,
		COL,
		ROW, 
		FLIP_X = False,
		FLIP_Y = False,
		DUR = 0.
	):
		self.COL = COL
		self.ROW = ROW
		self.DUR = DUR
		self.FLIP_X = FLIP_X
		self.FLIP_Y = FLIP_Y

class ObjSprite(ObjDraw):
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, SPRTS, x, y):
		self.SPRTS = SPRTS
		
		ObjDraw.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			pg.Rect(x, y, SPRTS.clip.w, SPRTS.clip.h)
		)

	def setFrame(self, frame):
		self.image = self.SPRTS[frm.ROW, frm.COL]

		if frame.FLIP_X or frame.FLIP_Y:
			self.image = pg.transform.flip(
				self.image,
				frame.FLIP_X,
				frame.FLIP_Y
			)


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

class ObjAnim(ObjDraw):
	speed = 1.
	done = False

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, SPRTS, x, y):
		self.SPRTS = SPRTS
		ObjDraw.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			pg.Rect(x, y, SPRTS.clip.w, SPRTS.clip.h)
		)

	def setAnim(self, anim):
		self._anim = anim
		self._frameIt = iter(anim)
		self._steps = 0.
		self._frame = next(self._frameIt)
		self.done = False

	def draw(self):
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

		ObjDraw.draw(self)
