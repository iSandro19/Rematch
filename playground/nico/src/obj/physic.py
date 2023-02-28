from obj.base import ObjDraw, ObjUpdate
import pygame as pg
from abc import abstractmethod


class ObjRelative(ObjDraw):
	@abstractmethod
	def __init__(self, INST_ID, FATHR_ID, image, rect, REF_POINT, pos):
		ObjDraw.__init__(self, INST_ID, FATHR_ID, image, rect)
		self.REF_POINT = REF_POINT
		self.pos = pos

	def draw(self):
		self.rect.x = self.pos.x - self.REF_POINT.x
		self.rect.y = self.pos.y - self.REF_POINT.y

class ObjParallax(ObjRelative):
	@abstractmethod
	def __init__(self, INST_ID, FATHR_ID, image, rect, REF_POINT, pos, Z_OFFSET):
		ObjRelative.__init__(self, INST_ID, FATHR_ID, image, rect, REF_POINT, pos)
		self.Z_OFFSET = Z_OFFSET

	def draw(self):
		self.rect.x = self.pos.x - self.REF_POINT.x*self.Z_OFFSET
		self.rect.y = self.pos.y - self.REF_POINT.y*self.Z_OFFSET

class ObjPhysic(ObjRelative, ObjUpdate):
	@abstractmethod
	def __init__(self, INST_ID, FATHR_ID, image, rect, REF_POINT, pos, acc, vel):
		ObjRelative.__init__(self, INST_ID, FATHR_ID, image, rect, REF_POINT, pos)
		ObjUpdate.__init__(self, INST_ID, FATHR_ID)
		self.acc = acc
		self.vel = vel

	def update(self):
		self.vel += acc
		self.pos.move_ip(self.vel)
		