from obj.base import ObjDraw, ObjUpdate
import pygame as pg
from abc import abstractmethod


class ObjRelative(ObjDraw):
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, rect, REF_POINT, pos):
		ObjDraw.__init__(self, HASH, FATHR_HASH, image, rect)
		self.REF_POINT = REF_POINT
		self.pos = pos

	def draw(self):
		self.rect.x = self.pos.x - self.REF_POINT.x
		self.rect.y = self.pos.y - self.REF_POINT.y

		ObjDraw.draw(self)

class ObjParallax(ObjDraw):
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, rect, REF_POINT, pos, Z_OFFSET):
		ObjDraw.__init__(self, HASH, FATHR_HASH, image, rect)
		self.REF_POINT = REF_POINT
		self.pos = pos
		self.Z_OFFSET = Z_OFFSET

	def draw(self):
		self.rect.x = self.pos.x - self.REF_POINT.x*self.Z_OFFSET
		self.rect.y = self.pos.y - self.REF_POINT.y*self.Z_OFFSET

		ObjDraw.draw(self)

class ObjPhysic(ObjRelative, ObjUpdate):
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, rect, REF_POINT, pos, acc, vel):
		ObjRelative.__init__(self, HASH, FATHR_HASH, image, rect, REF_POINT, pos)
		ObjUpdate.__init__(self, HASH, FATHR_HASH)
		self.acc = acc
		self.vel = vel

	def update(self):
		self.vel += acc
		self.pos.move_ip(self.vel)
		