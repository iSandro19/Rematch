import obj
import pygame as pg
from abc import abstractmethod

class ObjAlive(obj.physic.ObjRelative):

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
		life,
		maxLife,
		hitBoxOffsetH,
		hitBoxOffsetV,
		hitBoxW,
		hitBoxH
	):
		obj.physic.ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			img,
			imgW,
			imgH,
			REF_POINT,
			pos
		)
		self._life = life
		self._maxLife = maxLife

		self._hitBoxOffsetH = hitBoxOffsetH
		self._hitBoxOffsetV = hitBoxOffsetV
		self._hitBoxW = hitBoxW
		self._hitBoxH = hitBoxH

	@property
	def life(self):
		return self._life

	@life.setter
	def life(self, value):
		self._life = value

	@property
	def maxLife(self):
		return self._maxLife

	@property
	def hitBox(self):
		"""
		Se mantiene el offset con la collide box
		"""
		return pg.Rect(
			round(self.pos.x+self._hitBoxOffsetH),
			round(self.pos.y+self._hitBoxOffsetV),
			self._hitBoxW,
			self._hitBoxH
		)

	@abstractmethod
	def attack(self, dmg):
		pass
